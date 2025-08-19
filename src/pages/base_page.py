from playwright.async_api import BrowserContext


class BasePage:
    def __init__(self, page: BrowserContext, base_url: str):
        self.page = page
        self.base_url = base_url

    async def open_url(self):
        await self.page.goto(self.base_url)
