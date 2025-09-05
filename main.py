from src.pages.login_page import LoginPage
from src.pages.companies_page import CompaniesPage
from src.pages.download_page import DownloadPage
from src.config.settings import PlaywrightsConfigs, ItauConfigs
from src.utils.common_utils import tuple_list_to_str_list, SystemMessages
from src.models.duckdb.connection import DuckConnection
import asyncio


async def connect_duckdb():
    try:
        from src.utils.errors_utils import ConnectionFailedDuckDb
        duckdb = DuckConnection(
            'docs/database/companies.duckdb')
        SystemMessages().success('Feito conexão com a base de dados...')
        return duckdb
    except ConnectionFailedDuckDb.IOException:
        raise ConnectionFailedDuckDb(
            'Failed to connect in DuckDb - please check if there is any connections opened')


async def do_itau_tasks():
    async with PlaywrightsConfigs() as context:
        duckdb_connection = await connect_duckdb()

        companies_from_progress_table = tuple_list_to_str_list(
            duckdb_connection.search_all_companies())

        companies_pending_status = [
            company.replace(' - pending', '') for company in companies_from_progress_table if 'pending' in company]

        if len([company for company in companies_from_progress_table if 'done' in company]) > 0:
            if len(companies_pending_status) == 0:
                return SystemMessages().success('Tarefas do Itau foram executadas com sucesso!')

        companies_to_execute = companies_pending_status if len(
            companies_from_progress_table) > 0 else ItauConfigs.COMPANIES_TO_EXECUTE

        page = await context.new_page()
        login_itau = LoginPage(
            page, ItauConfigs.OPERATOR_ITAU, 'https://www.itau.com.br/itaubba-pt',)
        await login_itau.goto_login()

        companies_itau = CompaniesPage(
            page, companies_to_execute=companies_to_execute)
        accounts = await companies_itau.get_accounts()
        duckdb_connection.insert_companies_if_not_exists(accounts)

        for account in accounts:
            SystemMessages().log(
                f'Trocando conta para {account["name"]} - {account["number"]}...')

            if account['index'] == 0:
                SystemMessages().log(
                    f'Conta trocada para {account["name"]} - {account["cnpj"]} - {account["number"]}')
            else:
                await companies_itau.change_account(account)

            await companies_itau.goto_download_company_page()
            download_itau = DownloadPage(
                page, date_begin=ItauConfigs.DATE_BEGIN, date_end=ItauConfigs.DATE_END)
            await download_itau.search_payments()

            duckdb_connection.update_company_status(account, 'done')

        SystemMessages().success('Tarefas do Itau foram executadas com sucesso!')

if __name__ == '__main__':
    tentativas_mvp = 3

    while tentativas_mvp > 0:
        try:
            asyncio.run(do_itau_tasks())
            break
        except Exception as err:
            SystemMessages().error(err)
            tentativas_mvp -= 1
