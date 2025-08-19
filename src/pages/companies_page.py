from src.pages.base_page import BasePage
from src.config.settings import ItauConfigs
from typing import List


class CompaniesPage(BasePage):
    def __init__(self, page, base_url=None, companies_to_execute: List[str] = []):
        super().__init__(page, base_url)
        self.companies_to_execute = companies_to_execute

    async def get_accounts(self):
        await self.page.get_by_role("button", name="Trocar de conta").click()
        await self.page.get_by_role("radio", name="Múltiplas contas").click()
        await self.page.wait_for_timeout(6000)
