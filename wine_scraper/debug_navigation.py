import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.weingut-johannishof.de/"
    print(f"Attempting to navigate to {url} and wait for 30 seconds...")
    
    browser = None
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url, wait_until="networkidle", timeout=60000)
        print("Navigation successful. Page title:", await page.title())
        
        print("Waiting for 30 seconds...")
        await asyncio.sleep(30)
        
        print("✅ Test complete. The browser did not crash.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if browser:
            await browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
