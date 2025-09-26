from src.pages.itau_page.login_page import LoginPageItau
from src.pages.itau_page.companies_page import CompaniesPage
from src.pages.itau_page.download_page import DownloadPage
from src.pages.netsuite_page.login_page import LoginPageNetsuite
from src.pages.netsuite_page.search_page import SearchPage
from src.pages.netsuite_page.upload_page import UploadPage
from src.config.settings import PlaywrightsConfigs, ItauConfigs, NetsuiteConfigs
from src.utils.common_utils import *
from src.models.duckdb.connection import DuckConnection
import asyncio


async def connect_duckdb():
    try:
        from src.utils.errors_utils import ConnectionFailedDuckDb
        duckdb = DuckConnection(access_dir(
            'docs\database', 'companies.duckdb'))
        SystemMessages().success('Feito conexão com a base de dados...')
        return duckdb
    except ConnectionFailedDuckDb.IOException:
        SystemMessages().error(
            'Ocorreu algum erro ao tentar se conectar com a base de dados :(')
        raise ConnectionFailedDuckDb(
            'Failed to connect in DuckDB engine')


async def do_itau_tasks():
    async with PlaywrightsConfigs() as context:
        duckdb_connection = await connect_duckdb()

        companies_from_progress_table = tuple_list_to_str_list(
            duckdb_connection.search_all_companies())

        companies_pending_status = [
            company.replace(' - pending', '').replace(' - error', '')
            for company in companies_from_progress_table if 'pending' in company or 'error' in company]

        if len([company for company in companies_from_progress_table if 'done' in company]) > 0:
            if len(companies_pending_status) == 0:
                return SystemMessages().success('Tarefas do Itau foram executadas com sucesso!')

        companies_to_execute = companies_pending_status if len(
            companies_from_progress_table) > 0 else ItauConfigs.COMPANIES_TO_EXECUTE

        page = await context.new_page()
        login_itau = LoginPageItau(
            page, ItauConfigs.OPERATOR_ITAU, ItauConfigs.PASSWORD_ITAU, 'https://www.itau.com.br/itaubba-pt',)
        await login_itau.goto_login()

        companies_itau = CompaniesPage(
            page, companies_to_execute=companies_to_execute)
        accounts = await companies_itau.get_accounts()
        duckdb_connection.insert_companies_if_not_exists(accounts)

        for account in accounts:
            try:
                SystemMessages().log(
                    f'Trocando conta para {account["name"]} - {account["number"]}...')

                if account['index'] == 0:
                    SystemMessages().log(
                        f'Conta trocada para {account["name"]} - {account["cnpj"]} - {account["number"]}')
                else:
                    await retry.run(companies_itau.change_account, account)

                await retry.run(companies_itau.goto_download_company_page)
                download_itau = DownloadPage(
                    page, date_begin=ItauConfigs.DATE_BEGIN, date_end=ItauConfigs.DATE_END, cnpj_company=account['cnpj'])
                await retry.run(download_itau.search_payments)

                duckdb_connection.update_company_status(account, 'done')
            except:
                duckdb_connection.update_company_status(account, 'error')

        SystemMessages().success('Tarefas do Itau foram executadas com sucesso!')


async def do_netsuite_tasks():
    async with PlaywrightsConfigs() as context:
        duckdb_connection = await connect_duckdb()

        files = get_all_files_in_download_dir()
        if files:
            page = await context.new_page()
            login_netsuite = LoginPageNetsuite(
                page, NetsuiteConfigs.USER_NETSUITE, NetsuiteConfigs.PASSWORD_NETSUITE,
                NetsuiteConfigs.ANSWERS, 'https://system.netsuite.com/pages/customerlogin.jsp')
            await login_netsuite.goto_login()

            search_netsuite = SearchPage(
                page, 'https://6391568.app.netsuite.com/app/common/search/search.nl?searchtype=Custom&rectype=286&%E2%80%A6%20NetSuite%20Login')

            for file in files:
                is_supplier_exists = await search_netsuite.search_receipt(file)

                if is_supplier_exists:
                    upload_page = UploadPage(page)
                    await upload_page.upload_file(file)

                delete_file_from_path(access_dir('docs\downloads', file))

        SystemMessages().success('Tarefas do NetSuite foram executadas com sucesso!')

        # if not get_all_files_in_download_dir():
        #     duckdb_connection.drop_progress_table()

if __name__ == '__main__':
    retry = RetryExecuter()
    asyncio.run(retry.run(do_itau_tasks))
    asyncio.run(retry.run(do_netsuite_tasks))
