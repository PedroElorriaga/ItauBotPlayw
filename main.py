from src.pages.login_page import LoginPage
from src.pages.companies_page import CompaniesPage
from src.config.settings import PlaywrightsConfigs, ItauConfigs
import asyncio


async def do_itau_tasks():
    async with PlaywrightsConfigs() as context:
        page = await context.new_page()
        companies = ItauConfigs.COMPANIES_TO_EXECUTE
        login_itau = LoginPage(page, 'https://www.itau.com.br/itaubba-pt')
        await login_itau.goto_login()

        companies_itau = CompaniesPage(page, companies_to_execute=companies)
        await companies_itau.get_accounts()


if __name__ == '__main__':
    asyncio.run(do_itau_tasks())
