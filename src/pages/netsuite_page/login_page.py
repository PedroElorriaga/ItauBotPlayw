from src.pages.base_page import BasePage


class LoginPageNetsuite(BasePage):
    def __init__(self, page, base_url: str = None):
        super().__init__(page, base_url)

    async def goto_login(self):
        await self.open_url()
        await self.page.wait_for_timeout(5000)
