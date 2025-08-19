from src.pages.login_page import LoginPage
from src.config.settings import PlaywrightsConfigs
import asyncio


async def run_tasks():
    async with PlaywrightsConfigs() as context:
        page = await context.new_page()
        login_itau = LoginPage(page, 'https://www.itau.com.br/itaubba-pt')
        await login_itau.goto_login()


if __name__ == '__main__':
    asyncio.run(run_tasks())
