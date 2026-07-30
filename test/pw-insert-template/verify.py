import asyncio
from playwright.async_api import async_playwright

URL = 'file:///Users/kylon_luo/Nova/nova-nimbus/public/private/alienfizzle/spec-manual.html'

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(URL)
        await page.wait_for_selector('#btn-toggle-edit')

        # T2 (first, in read-only): 下拉隐藏
        wrap_hidden_ro = await page.evaluate("() => document.getElementById('spec-tpl-wrap').hidden")
        print(f"[T2] read-only tpl-wrap hidden={wrap_hidden_ro}")
        assert wrap_hidden_ro is True, "FAIL 只读模式下拉未隐藏"
        print("[T2] PASS")

        # 进入编辑模式
        await page.click('#btn-toggle-edit')
        await asyncio.sleep(0.3)

        # T1: 下拉可见
        wrap_hidden_ed = await page.evaluate("() => document.getElementById('spec-tpl-wrap').hidden")
        wrap_visible = await page.is_visible('#btn-tpl-menu')
        print(f"[T1] editing tpl-wrap hidden={wrap_hidden_ed}, btn visible={wrap_visible}")
        assert wrap_hidden_ed is False, "FAIL 编辑模式下拉未显示"
        assert wrap_visible, "FAIL 插入模板按钮不可见"
        btn_text = await page.text_content('#btn-tpl-menu')
        assert '插入模板' in btn_text, f"FAIL 按钮文本异常: {btn_text}"
        print("[T1] PASS")

        # T3: 点开下拉 → 8 项可见
        await page.click('#btn-tpl-menu')
        await asyncio.sleep(0.2)
        menu_hidden = await page.evaluate("() => document.getElementById('spec-tpl-menu').hidden")
        assert menu_hidden is False, "FAIL 菜单没打开"
        items = await page.evaluate("""() => {
            const arr = Array.from(document.querySelectorAll('#spec-tpl-menu .spec-tpl-item'));
            return arr.map(b => ({tpl: b.dataset.tpl, label: b.getAttribute('aria-label'), text: b.textContent.trim()}));
        }""")
        print(f"[T3] items count = {len(items)}")
        for it in items:
            print(f"      - {it}")
        assert len(items) == 8, f"FAIL 模板项数量应为 8, got {len(items)}"
        expected_keys = {'skill','mastery','gate','enemy','line','chapter','subchapter','callout'}
        got_keys = {it['tpl'] for it in items}
        assert got_keys == expected_keys, f"FAIL 模板 key 不匹配: {got_keys}"
        for it in items:
            assert it['label'], f"FAIL 缺 aria-label: {it}"
            assert it['text'], f"FAIL 缺 text: {it}"
        print("[T3] PASS")

        # T4: 点"新技能卡" → main 新增 <div class="callout"> 含 [卡名]
        # 先记录当前 callout 数
        before = await page.evaluate("() => document.querySelectorAll('main .callout').length")
        # 把光标放到 main 里某段
        await page.evaluate("""() => {
            const main = document.querySelector('main');
            const p = main.querySelector('p') || main.firstElementChild;
            const range = document.createRange();
            range.selectNodeContents(p);
            range.collapse(false);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        }""")
        await page.click('[data-tpl="skill"]')
        await asyncio.sleep(0.3)
        after = await page.evaluate("() => document.querySelectorAll('main .callout').length")
        has_placeholder = await page.evaluate("""() => {
            const cs = document.querySelectorAll('main .callout');
            for (const c of cs) { if (c.textContent.includes('[卡名]')) return true; }
            return false;
        }""")
        print(f"[T4] callout before={before} after={after} has [卡名]={has_placeholder}")
        assert after > before, f"FAIL callout 数未增加"
        assert has_placeholder, "FAIL 新 callout 未含 [卡名] 占位符"
        await page.screenshot(path='/tmp/insert-template-verify.png', full_page=False)
        print("[T4] screenshot saved to /tmp/insert-template-verify.png")
        print("[T4] PASS")

        await browser.close()
        print("\n=== ALL 4/4 PASS ===")

asyncio.run(run())
