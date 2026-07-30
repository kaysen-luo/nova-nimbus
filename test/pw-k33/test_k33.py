#!/usr/bin/env python3
"""
K33 AUX 䱇恨 (rankedBoboTargets / classifyEnemyTier) Playwright headless 断言
6 项:
  T1 classifyEnemyTier 2 阶 (atDefense→0, 其他→1, 不看 boss)
  T2 P1 (atDefense) 内部血量少优先
  T3 P2 (未 atDefense) 内部 y 降序 (靠近防线优先)
  T4 P2 y 相等时 hp 升序兑底
  T5 P1 优先于 P2 全部 (不分类型)
  T6 P1 boss 与 minion 同时 atDefense 时 boss 不优先
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

DEMO_URL = "file://" + os.path.expanduser(
    "~/Nova/nova-nimbus/dist/private/alienfizzle/demo.html"
)

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
END = "\033[0m"
PASS = f"{GREEN}PASS{END}"
FAIL = f"{RED}FAIL{END}"


async def _boot(page):
    await page.goto(DEMO_URL)
    # 等 classifyEnemyTier 与 rankedBoboTargets (作为全局 function 声明)
    await page.wait_for_function(
        "() => typeof classifyEnemyTier === 'function' "
        "&& typeof rankedBoboTargets === 'function' "
        "&& typeof G === 'object' && G !== null",
        timeout=10000,
    )
    # 暴露到 window (确认可读)
    typeofs = await page.evaluate(
        """() => {
            window.classifyEnemyTier = classifyEnemyTier;
            window.rankedBoboTargets = rankedBoboTargets;
            return {
                cet: typeof window.classifyEnemyTier,
                rbt: typeof window.rankedBoboTargets,
            };
        }"""
    )
    assert typeofs == {"cet": "function", "rbt": "function"}, typeofs


async def _reset_enemies(page):
    """把 G.enemies 清空 (若 startGame 未跑, G.enemies 也可能是空数组或 undefined)。"""
    await page.evaluate(
        """() => {
            if (!Array.isArray(G.enemies)) G.enemies = [];
            G.enemies.length = 0;
        }"""
    )


async def test_t1(page):
    print(f"\n{CYAN}[T1]{END} classifyEnemyTier 2 阶")
    r = await page.evaluate(
        """() => ({
            atDef:        classifyEnemyTier({atDefense:true}),
            boss:         classifyEnemyTier({atDefense:false, isFinalBoss:true}),
            elite:        classifyEnemyTier({atDefense:false, type:'elite'}),
            minion:       classifyEnemyTier({atDefense:false, type:'minion'}),
        })"""
    )
    print(f"     结果: {r}")
    ok = r["atDef"] == 0 and r["boss"] == 1 and r["elite"] == 1 and r["minion"] == 1
    print(f"  {PASS if ok else FAIL}")
    return ok


async def test_t2(page):
    print(f"\n{CYAN}[T2]{END} P1(atDefense) 内部血量少优先 (不分类型)")
    await _reset_enemies(page)
    r = await page.evaluate(
        """() => {
            G.enemies.push({id:'minion', type:'minion', hp:100, atDefense:true, x:200, y:600});
            G.enemies.push({id:'miniBoss', type:'miniBoss', hp:500, atDefense:true, x:200, y:600});
            G.enemies.push({id:'elite', type:'elite', hp:300, atDefense:true, x:200, y:600});
            const list = rankedBoboTargets({x:180, y:700}, G.enemies, {ignoreRange:true});
            return list.map(e => ({id:e.id, hp:e.hp, y:e.y, atDef:e.atDefense}));
        }"""
    )
    print(f"     排序: {r}")
    ok = bool(r) and r[0]["id"] == "minion"
    print(f"  {PASS if ok else FAIL}")
    return ok


async def test_t3(page):
    print(f"\n{CYAN}[T3]{END} P2(未 atDefense) 内部 y 降序 (最靠近防线优先)")
    await _reset_enemies(page)
    r = await page.evaluate(
        """() => {
            G.enemies.push({id:'far',  hp:100, atDefense:false, x:200, y:200});
            G.enemies.push({id:'mid',  hp:100, atDefense:false, x:200, y:500});
            G.enemies.push({id:'near', hp:100, atDefense:false, x:200, y:700});
            const list = rankedBoboTargets({x:180, y:700}, G.enemies, {ignoreRange:true});
            return list.map(e => ({id:e.id, y:e.y}));
        }"""
    )
    print(f"     排序: {r}")
    ok = bool(r) and r[0]["y"] == 700
    print(f"  {PASS if ok else FAIL}")
    return ok


async def test_t4(page):
    print(f"\n{CYAN}[T4]{END} P2 y 相等时 hp 升序兑底")
    await _reset_enemies(page)
    r = await page.evaluate(
        """() => {
            G.enemies.push({id:'A', hp:500, atDefense:false, x:200, y:500});
            G.enemies.push({id:'B', hp:100, atDefense:false, x:200, y:500});
            G.enemies.push({id:'C', hp:300, atDefense:false, x:200, y:500});
            const list = rankedBoboTargets({x:180, y:700}, G.enemies, {ignoreRange:true});
            return list.map(e => ({id:e.id, hp:e.hp, y:e.y}));
        }"""
    )
    print(f"     排序: {r}")
    ok = bool(r) and r[0]["hp"] == 100
    print(f"  {PASS if ok else FAIL}")
    return ok


async def test_t5(page):
    print(f"\n{CYAN}[T5]{END} P1 优先于 P2 全部 (不分类型)")
    await _reset_enemies(page)
    r = await page.evaluate(
        """() => {
            G.enemies.push({id:'P1-minion-1hp', type:'minion', hp:1, atDefense:true, x:200, y:400});
            G.enemies.push({id:'P2-miniBoss',   type:'miniBoss', hp:9999, atDefense:false, x:200, y:700});
            G.enemies.push({id:'P2-elite',      type:'elite', hp:500, atDefense:false, x:200, y:600});
            G.enemies.push({id:'P2-minion',     type:'minion', hp:100, atDefense:false, x:200, y:500});
            const list = rankedBoboTargets({x:180, y:700}, G.enemies, {ignoreRange:true});
            return list.map(e => ({id:e.id, hp:e.hp, y:e.y, atDef:e.atDefense}));
        }"""
    )
    print(f"     排序: {r}")
    ok = bool(r) and r[0]["id"] == "P1-minion-1hp"
    print(f"  {PASS if ok else FAIL}")
    return ok


async def test_t6(page):
    print(f"\n{CYAN}[T6]{END} P1 内部 boss 不优先 (K 规则不分类型, 只看 hp)")
    await _reset_enemies(page)
    r = await page.evaluate(
        """() => {
            G.enemies.push({id:'miniBoss', type:'miniBoss', hp:500, atDefense:true, x:200, y:600});
            G.enemies.push({id:'minion',   type:'minion',   hp:100, atDefense:true, x:200, y:600});
            const list = rankedBoboTargets({x:180, y:700}, G.enemies, {ignoreRange:true});
            return list.map(e => ({id:e.id, hp:e.hp, atDef:e.atDefense}));
        }"""
    )
    print(f"     排序: {r}")
    ok = bool(r) and r[0]["id"] == "minion"
    print(f"  {PASS if ok else FAIL}")
    return ok


async def main():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context()
            page = await context.new_page()
            await _boot(page)
            for name, fn in [
                ("T1", test_t1), ("T2", test_t2), ("T3", test_t3),
                ("T4", test_t4), ("T5", test_t5), ("T6", test_t6),
            ]:
                try:
                    results[name] = await fn(page)
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    results[name] = False
        finally:
            await browser.close()

    print("\n" + "=" * 40)
    for k, v in results.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"  Total: {passed}/{total}")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    asyncio.run(main())
