import asyncio
from playwright.async_api import async_playwright

URL = 'file:///Users/kylon_luo/Nova/nova-nimbus/dist/private/alienfizzle/spec-manual.html'

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(URL)
        await page.wait_for_selector('.sidebar')

        # T1: sidebar 位置和宽度
        rect = await page.evaluate("() => { const r = document.querySelector('.sidebar').getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height}; }")
        print(f"[T1] sidebar rect: {rect}")
        assert rect['x'] < 5, f"FAIL sidebar 未贴左, x={rect['x']}"
        assert 270 <= rect['w'] <= 290, f"FAIL sidebar 宽度异常 w={rect['w']}"
        assert rect['h'] >= 800, f"FAIL sidebar 高度异常 h={rect['h']}"
        print("[T1] PASS")

        # T2: main 起始位置
        main_rect = await page.evaluate("() => { const r = document.querySelector('main').getBoundingClientRect(); return {x: r.x, w: r.width}; }")
        print(f"[T2] main rect: {main_rect}")
        assert main_rect['x'] >= 275, f"FAIL main 未在 sidebar 右侧 x={main_rect['x']}"
        assert main_rect['w'] >= 900, f"FAIL main 宽度被挤 w={main_rect['w']}"
        print("[T2] PASS")

        # T3: 滚动后 sidebar 仍在原位
        await page.evaluate("window.scrollTo(0, 1000)")
        await asyncio.sleep(0.5)
        rect2 = await page.evaluate("() => { const r = document.querySelector('.sidebar').getBoundingClientRect(); return {x: r.x, y: r.y}; }")
        print(f"[T3] sidebar after scroll: {rect2}")
        assert rect2['y'] < 5, f"FAIL 滚动后 sidebar 没跟随, y={rect2['y']}"
        print("[T3] PASS")

        # T4: 截图存档
        await page.screenshot(path='/tmp/spec-manual-layout-fix.png', full_page=False)
        print("[T4] screenshot saved to /tmp/spec-manual-layout-fix.png")
        print("[T4] PASS")

        await browser.close()
        print("ALL 4/4 PASS")

asyncio.run(run())
