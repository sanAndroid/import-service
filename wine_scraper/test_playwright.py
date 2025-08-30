import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("Navigating to https://www.weingut-knewitz.de/...")
            await page.goto("https://www.weingut-knewitz.de/", timeout=60000)
            print("Navigation successful!")
            print(await page.title())
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())