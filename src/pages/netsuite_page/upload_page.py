from src.pages.base_page import BasePage


class UploadPage(BasePage):
    def __init__(self, page, base_url=None):
        super().__init__(page, base_url)

    async def goto_search_page(self):
        await self.open_url()
        await self.page.wait_for_timeout(3000)
