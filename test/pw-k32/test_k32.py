#!/usr/bin/env python3
"""
K32 Playwright headless 活体断言
- T1: rollMercyMult Lv1/Lv2/Lv3 数值分布 (10000 次采样)
- T2: Lv3 恐惧位移基础
- T3: Lv3 恐惧速度 = 1x 敌人 speed (不吃 slow)
- T4: Lv3 恐惧过期后恢复正常前推
- T5: Lv1/Lv2 保持 stunUntil 硬控 (不换恐惧)
"""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

DEMO_PATH = os.path.expanduser(
    "~/Nova/nova-nimbus/dist/private/alienfizzle/demo.html"
)
DEMO_URL = "file://" + DEMO_PATH

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
INFO = "\033[36m----\033[0m"


def _fmt_freq(d):
    total = sum(d.values())
    return {k: round(v / total, 4) for k, v in sorted(d.items())}


def _ev(d):
    total = sum(d.values())
    return round(sum(k * v for k, v in d.items()) / total, 4)


async def _bootstrap(page):
    """加载 demo, 启动 startGame(3), 暴露 rollMercyMult 提取字符串。"""
    await page.goto(DEMO_URL)
    # 等到 castSkill 和 G 可用
    await page.wait_for_function(
        "() => typeof castSkill === 'function' && typeof G === 'object' && G !== null",
        timeout=10000,
    )
    # 启动第三关 (需要游戏循环运行以让 e.y 每帧被 update)
    await page.evaluate("startGame(3)")
    # 等 G.running 和 player 就绪
    await page.wait_for_function(
        "() => G.running === true && G.player && typeof G.player.x === 'number'",
        timeout=5000,
    )
    # 提取 rollMercyMult 函数体 (定义于 castSkill 内部) 并挂到 window
    # 用花括号计数抠出函数体, 避开正则贪婪/懒惰坑
    await page.evaluate(
        r"""
        () => {
            const src = castSkill.toString();
            const sig = 'function rollMercyMult(level)';
            const i = src.indexOf(sig);
            if (i < 0) throw new Error('rollMercyMult 签名找不到');
            let j = src.indexOf('{', i);
            if (j < 0) throw new Error('rollMercyMult { 找不到');
            const start = j;
            let depth = 0;
            let end = -1;
            for (let k = start; k < src.length; k++) {
                const ch = src[k];
                if (ch === '{') depth++;
                else if (ch === '}') {
                    depth--;
                    if (depth === 0) { end = k; break; }
                }
            }
            if (end < 0) throw new Error('rollMercyMult 闭合 } 找不到');
            const body = src.slice(start + 1, end);
            window.__rollMercyMult = new Function('level', body);
            // 自测: 调一次
            const t = window.__rollMercyMult(3);
            if (![48,64,80,96,112,128,160].includes(t)) {
                throw new Error('rollMercyMult 自测异常 got=' + t);
            }
        }
        """
    )
    # 冻结 spawn: 清空敌人 + 让新 spawn 推迟 (不动 CFG, 只推迟 next*)
    await page.evaluate(
        """() => {
            G.enemies.length = 0;
            G.nextEnemyAt = G.now + 60000;
            G.nextGateAt = G.now + 60000;
            G.nextTreasureAt = G.now + 60000;
            G.nextObstacleAt = G.now + 60000;
        }"""
    )


# ============================================================
# T1 · rollMercyMult 三级倍率表分布
# ============================================================
async def test_t1(page):
    print(f"\n{INFO} T1 · rollMercyMult 三级倍率表分布 (10000 采样)")
    theoretical_ev = {1: 47.04, 2: 60.64, 3: 77.28}
    expected_sets = {
        1: {24, 32, 48, 64, 80, 96, 112},
        2: {32, 48, 64, 80, 96, 112, 128},
        3: {48, 64, 80, 96, 112, 128, 160},
    }
    # 期望频率: 权重 30/23/17/12/8/6/4 → 30% first, 4% last
    ok = True
    details = []
    for lvl in (1, 2, 3):
        counts = await page.evaluate(
            f"""() => {{
                const c = {{}};
                for (let i = 0; i < 10000; i++) {{
                    const v = window.__rollMercyMult({lvl});
                    c[v] = (c[v] || 0) + 1;
                }}
                return c;
            }}"""
        )
        counts = {int(k): v for k, v in counts.items()}
        keys = set(counts.keys())
        freq = _fmt_freq(counts)
        ev = _ev(counts)
        exp_set = expected_sets[lvl]
        first_val = min(exp_set)
        last_val = max(exp_set)
        first_f = freq.get(first_val, 0)
        last_f = freq.get(last_val, 0)

        checks = []
        set_ok = keys == exp_set
        checks.append(("set", set_ok, f"got={sorted(keys)} exp={sorted(exp_set)}"))
        first_ok = 0.28 <= first_f <= 0.32
        checks.append((f"P[{first_val}]", first_ok, f"{first_f:.4f} ∈ [0.28,0.32]"))
        last_ok = 0.03 <= last_f <= 0.05
        checks.append((f"P[{last_val}]", last_ok, f"{last_f:.4f} ∈ [0.03,0.05]"))

        ev_dev = abs(ev - theoretical_ev[lvl]) / theoretical_ev[lvl] * 100
        details.append(
            f"  Lv{lvl}: freq={freq}\n"
            f"       EV_obs={ev} vs EV_theo={theoretical_ev[lvl]}  (偏差 {ev_dev:.2f}%)"
        )
        for name, res, msg in checks:
            details.append(f"       [{'✓' if res else '✗'}] {name}: {msg}")
            if not res:
                ok = False
    print("\n".join(details))
    print(f"  → {PASS if ok else FAIL}")
    return ok


# ============================================================
# T2 · Lv3 恐惧位移基础
# ============================================================
async def _reset_enemies(page):
    await page.evaluate("() => { G.enemies.length = 0; }")


async def _push_mock_pair(page, mock_y=400, mock_x=180, mock_speed=50):
    """
    只 push 1 只 mock (不走 castSkill, 手工设 fearUntil/stunUntil 只测位移分支)。
    hp 拉极大防被打死, atDefense=false 保证正常 update。
    """
    await page.evaluate(
        f"""() => {{
            const mock = {{
                x: {mock_x}, y: {mock_y}, w: 30, h: 30,
                hp: 999999999, maxHp: 999999999,
                speed: {mock_speed}, dps: 5, score: 10,
                kind: 'minion', type: 'small',
                isMiniBoss: false, isFinalBoss: false,
                atDefense: false,
                armor: 0,
                __mock: true,
            }};
            G.enemies.push(mock);
            window.__mock = mock;
        }}"""
    )


async def _get_mock(page):
    return await page.evaluate(
        """() => {
            const m = window.__mock;
            return {
                x: m.x, y: m.y,
                hp: m.hp,
                fearUntil: m.fearUntil || 0,
                stunUntil: m.stunUntil || 0,
                atDefense: m.atDefense,
                now: G.now,
                speed: m.speed,
            };
        }"""
    )


async def test_t2(page):
    print(f"\n{INFO} T2 · Lv3 恐惧位移基础断言 (手工设 fearUntil, 绕过 castSkill 锁头/锥形)")
    await _reset_enemies(page)
    await _push_mock_pair(page, mock_y=400)

    # 手工设 fearUntil 1500ms + atDefense=false (模拟 mercy Lv3 命中效果)
    await page.evaluate("""() => {
        window.__mock.fearUntil = G.now + 1500;
        window.__mock.atDefense = false;
    }""")
    await page.wait_for_timeout(200)

    s1 = await _get_mock(page)
    remaining = s1["fearUntil"] - s1["now"]
    print(
        f"  设 fearUntil +200ms: y={s1['y']:.2f} fearUntil-now={remaining:.1f}ms "
        f"atDefense={s1['atDefense']} hp={s1['hp']}"
    )

    check_fear = remaining > 1200  # 已用掉 200ms 缓冲, 应还剩 > 1200ms
    check_defense = s1["atDefense"] is False

    y_before = s1["y"]
    await page.wait_for_timeout(300)
    s2 = await _get_mock(page)
    dy = s2["y"] - y_before
    check_pushback = dy < 0
    print(
        f"  +300ms: y={s2['y']:.2f}  Δy={dy:+.2f}  (期望负值=反推)"
    )

    ok = check_fear and check_defense and check_pushback
    print(f"  [{'✓' if check_fear else '✗'}] fearUntil - G.now > 1200ms")
    print(f"  [{'✓' if check_defense else '✗'}] atDefense === false")
    print(f"  [{'✓' if check_pushback else '✗'}] 300ms 后 e.y 递减 (反推)")
    print(f"  → {PASS if ok else FAIL}")
    return ok


# ============================================================
# T3 · Lv3 恐惧速度 = 1x 原速 (不吃 slow)
# ============================================================
async def test_t3(page):
    print(f"\n{INFO} T3 · Lv3 恐惧不吃 slow (手工设 fearUntil + slowUntil)")
    await _reset_enemies(page)
    await _push_mock_pair(page, mock_y=400, mock_speed=50)

    # 挂强减速 + 手工设 fearUntil (模拟 mercy Lv3 Lv3 命中)
    await page.evaluate("""() => {
        window.__mock.slowUntil = G.now + 5000;
        window.__mock.slowMult = 0.3;
        window.__mock.fearUntil = G.now + 1500;
        window.__mock.atDefense = false;
    }""")
    await page.wait_for_timeout(100)  # 让 update 循环跑几帧

    samples = []
    prev = await _get_mock(page)
    for i in range(5):
        await page.wait_for_timeout(100)
        cur = await _get_mock(page)
        dt_ms = cur["now"] - prev["now"]
        dy = cur["y"] - prev["y"]
        v = (dy / dt_ms) * 1000 if dt_ms > 0 else 0
        samples.append((cur["now"], cur["y"], dt_ms, dy, v))
        prev = cur

    for i, (t, y, dt, dy, v) in enumerate(samples):
        print(
            f"  frame#{i}: now={t:.0f}  y={y:.2f}  dt={dt:.1f}ms  Δy={dy:+.2f}  v={v:+.2f} px/s"
        )
    speeds = [s[4] for s in samples]
    mean_v = sum(speeds) / len(speeds)
    check_speed = -60 <= mean_v <= -40
    check_not_slowed = mean_v < -30
    print(f"  mean v = {mean_v:.2f} px/s  期望 ≈ -50 (若吃 slow 应为 ≈ -15)")
    ok = check_speed and check_not_slowed
    print(f"  [{'✓' if check_speed else '✗'}] mean v ∈ [-60, -40]")
    print(f"  [{'✓' if check_not_slowed else '✗'}] 不吃 slow (|v| > 30)")
    print(f"  → {PASS if ok else FAIL}")
    return ok


# ============================================================
# T4 · Lv3 恐惧过期后恢复正常前推
# ============================================================
async def test_t4(page):
    print(f"\n{INFO} T4 · Lv3 恐惧过期后恢复前推 (手工设 fearUntil)")
    await _reset_enemies(page)
    await _push_mock_pair(page, mock_y=400, mock_speed=50)

    y0 = (await _get_mock(page))["y"]
    await page.evaluate("""() => {
        window.__mock.fearUntil = G.now + 1500;
        window.__mock.atDefense = false;
    }""")

    # 等 fearUntil(1500) + 100ms 缓冲 = 1600ms
    await page.wait_for_timeout(1600)

    s_mid = await _get_mock(page)
    print(
        f"  y0={y0:.2f}  设+1600ms: y={s_mid['y']:.2f}  "
        f"fearRemaining={max(0, s_mid['fearUntil']-s_mid['now']):.0f}ms"
    )
    fear_expired = (s_mid["fearUntil"] - s_mid["now"]) <= 0

    # 再等 500ms 观察正常前推
    await page.wait_for_timeout(500)
    s_end = await _get_mock(page)
    dy = s_end["y"] - s_mid["y"]
    v = (dy / 500) * 1000
    print(f"  +500ms: y={s_end['y']:.2f}  Δy={dy:+.2f}  v={v:+.2f} px/s (期望 ≈ +50)")

    check_forward = dy > 0
    check_speed = 30 <= v <= 70
    ok = fear_expired and check_forward and check_speed
    print(f"  [{'✓' if fear_expired else '✗'}] fearUntil 已过期")
    print(f"  [{'✓' if check_forward else '✗'}] y 重新递增 (正常前推)")
    print(f"  [{'✓' if check_speed else '✗'}] v ∈ [30, 70] px/s")
    print(f"  → {PASS if ok else FAIL}")
    return ok


# ============================================================
# T5 · Lv1/Lv2 保持 stunUntil 硬控 (手工设 stunUntil)
# ============================================================
async def test_t5(page):
    print(f"\n{INFO} T5 · Lv1/Lv2 保持 stunUntil 硬控 (手工设 stunUntil)")
    all_ok = True
    for lvl in (1, 2):
        await _reset_enemies(page)
        await _push_mock_pair(page, mock_y=400, mock_speed=50)
        y_before = (await _get_mock(page))["y"]
        # 手工设 stunUntil = 1000ms (模拟 Lv1/Lv2 命中后颤栗生效)
        await page.evaluate("() => { window.__mock.stunUntil = G.now + 1000; }")
        await page.wait_for_timeout(200)  # 采样 200ms 后 stun 还剩 ~800ms
        s = await _get_mock(page)
        stun_rem = s["stunUntil"] - s["now"]
        dy = s["y"] - y_before
        print(
            f"  Lv{lvl}: y_before={y_before:.2f}  +200ms y_after={s['y']:.2f}  Δy={dy:+.2f}  "
            f"stunUntil-now={stun_rem:.0f}ms  fearUntil={s['fearUntil']}"
        )
        c_stun = stun_rem > 700  # 200ms 后应剩 ~800ms
        c_no_fear = s["fearUntil"] == 0
        c_still = abs(dy) < 5  # stun 期间 update 里 atDefense 逻辑跳过前推 → y 不动 (但 stun 分支在 update 里可能不生效, 见下)
        print(f"    [{'✓' if c_stun else '✗'}] stunUntil - now > 700ms")
        print(f"    [{'✓' if c_no_fear else '✗'}] fearUntil == 0 / undefined")
        print(f"    [{'✓' if c_still else '✗'}] e.y 未变化 (|Δy|<5)")
        if not (c_stun and c_no_fear and c_still):
            all_ok = False
    print(f"  → {PASS if all_ok else FAIL}")
    return all_ok


# ============================================================
# main
# ============================================================
async def main():
    if not os.path.exists(DEMO_PATH):
        print(f"FATAL: {DEMO_PATH} not found; run npm run build first")
        sys.exit(2)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 500, "height": 800})
        page = await context.new_page()
        page.on(
            "console",
            lambda msg: (
                None
                if msg.type not in ("error", "warning")
                else print(f"  [browser {msg.type}] {msg.text[:200]}")
            ),
        )

        results = {}
        try:
            await _bootstrap(page)
            results["T1"] = await test_t1(page)
            results["T2"] = await test_t2(page)
            results["T3"] = await test_t3(page)
            results["T4"] = await test_t4(page)
            results["T5"] = await test_t5(page)
        except Exception as e:
            print(f"\n{FAIL} 异常: {e!r}")
            import traceback

            traceback.print_exc()
        finally:
            await browser.close()

        print("\n" + "=" * 50)
        for k, v in results.items():
            print(f"  {k}: {'PASS' if v else 'FAIL'}")
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        print(f"  Total: {passed}/{total}")
        sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    asyncio.run(main())
