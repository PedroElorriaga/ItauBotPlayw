from src.pages.login_page import LoginPage
from src.pages.companies_page import CompaniesPage
from src.config.settings import PlaywrightsConfigs, ItauConfigs
from src.models.duckdb.connection import DuckConnection
import asyncio


async def connect_duckdb():
    try:
        from src.utils.errors_utils import ConnectionFailedDuckDb
        duckdb = DuckConnection(
            'docs/database/companies.duckdb')
        return duckdb
    except ConnectionFailedDuckDb.IOException:
        raise ConnectionFailedDuckDb(
            'Failed to connect in DuckDb - please check if there is any connections opened')


async def do_itau_tasks():
    async with PlaywrightsConfigs() as context:
        duckdb_connection = await connect_duckdb()

        companies_from_progress_table = duckdb_connection.search_companies_status_pending()
        print(companies_from_progress_table)
        page = await context.new_page()
        companies_to_execute = companies_from_progress_table if len(
            companies_from_progress_table) > 0 else ItauConfigs.COMPANIES_TO_EXECUTE

        login_itau = LoginPage(page, 'https://www.itau.com.br/itaubba-pt')
        await login_itau.goto_login()

        companies_itau = CompaniesPage(
            page, companies_to_execute=companies_to_execute)
        accounts = await companies_itau.get_accounts()
        print(accounts)

        duckdb_connection.insert_companies_if_not_exists(accounts)


if __name__ == '__main__':
    asyncio.run(do_itau_tasks())
