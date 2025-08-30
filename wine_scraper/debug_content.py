import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.weingut-johannishof.de/products/2022-terra-nostra-riesling-trocken-vdp-gutswein-kopie"
    print(f"Attempting to fetch content from {url}")
    
    browser = None
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url, wait_until="networkidle", timeout=60000)
        content = await page.content()
        
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("✅ Content saved to debug_page.html")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if browser:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
