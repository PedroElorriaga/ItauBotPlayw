from playwright.async_api import BrowserContext


class BasePage:
    def __init__(self, page: BrowserContext, base_url: str = None):
        self.page = page
        self.iframe_page = None
        self.base_url = base_url

    async def open_url(self):
        await self.page.goto(self.base_url)
        await self.page.bring_to_front()
