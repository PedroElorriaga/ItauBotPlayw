from src.pages.itau_page.login_page import LoginPageItau
from src.pages.itau_page.companies_page import CompaniesPage
from src.pages.itau_page.download_page import DownloadPage
from src.pages.netsuite_page.login_page import LoginPageNetsuite
from src.pages.netsuite_page.search_page import SearchPage
from src.pages.netsuite_page.upload_page import UploadPage
from src.config.settings import PlaywrightsConfigs, ItauConfigs, NetsuiteConfigs
from src.utils.common_utils import *
from src.services.system_messages import SystemMessages
from src.services.retry_executer import RetryExecuter
from src.models.duckdb.settings.connection import DuckConnection
from src.models.duckdb.repository.progress_repository import ProgressRepository
from tqdm.asyncio import tqdm
import asyncio


async def do_itau_tasks():
    async with PlaywrightsConfigs() as context:
        companies_from_progress_table = tuple_list_to_str_list(
            progress_repository.search_all_companies())

        companies_pending_status = [
            company.replace(' - pending', '').replace(' - error', '')
            for company in companies_from_progress_table if 'pending' in company or 'error' in company]

        if len([company for company in companies_from_progress_table if 'done' in company]) > 0:
            if len(companies_pending_status) == 0:
                return SystemMessages().success('Todas tarefas do Itau ja foram executadas')

        companies_to_execute = companies_pending_status if len(
            companies_from_progress_table) > 0 else ItauConfigs.COMPANIES_TO_EXECUTE

        page = await context.new_page()
        login_itau = LoginPageItau(
            page, ItauConfigs.OPERATOR_ITAU, ItauConfigs.PASSWORD_ITAU, 'https://www.itau.com.br/itaubba-pt',)
        await login_itau.goto_login()

        companies_itau = CompaniesPage(
            page, companies_to_execute=companies_to_execute)
        accounts = await companies_itau.get_accounts()
        progress_repository.insert_companies_if_not_exists(accounts)

        if len(accounts) == 0:
            SystemMessages().error(
                'Nenhuma empresa nos parametros informados foi encontrada, verifique as informações enviadas')
            return

        async for i, account in tqdm(enumerate(accounts, start=1), total=len(accounts), desc='Contas processadas'):
            try:
                SystemMessages().log(
                    f'Trocando conta para {account["name"]} - {account["number"]}...')

                if account['index'] != 0:
                    await retry.run(companies_itau.change_account, account)

                await retry.run(companies_itau.goto_download_company_page)
                download_itau = DownloadPage(
                    page, date_begin=ItauConfigs.DATE_BEGIN, date_end=ItauConfigs.DATE_END, cnpj_company=account['cnpj'])
                await retry.run(download_itau.search_payments)

                progress_repository.update_company_status(account, 'done')
            except:
                progress_repository.update_company_status(account, 'error')

        SystemMessages().success('✅ Tarefas do Itau foram executadas com sucesso!')


async def do_netsuite_tasks():
    async with PlaywrightsConfigs() as context:
        files = get_all_files_in_download_dir()
        if files:
            page = await context.new_page()
            login_netsuite = LoginPageNetsuite(
                page, NetsuiteConfigs.USER_NETSUITE, NetsuiteConfigs.PASSWORD_NETSUITE,
                NetsuiteConfigs.ANSWERS, 'https://system.netsuite.com/pages/customerlogin.jsp')
            await login_netsuite.goto_login()

            search_netsuite = SearchPage(
                page, 'https://6391568.app.netsuite.com/app/common/search/search.nl?searchtype=Custom&rectype=286&%E2%80%A6%20NetSuite%20Login')

            async for i, file in tqdm(enumerate(files, start=1), total=len(files), desc='Comprovantes processados'):
                is_supplier_exists = await search_netsuite.search_receipt(file)

                if is_supplier_exists:
                    upload_page = UploadPage(page)
                    await upload_page.upload_file(file)

                delete_file_from_path(access_dir('docs\downloads', file))
        else:
            SystemMessages().success('Nenhuma tarefa do NetSuite foi encontrada')
            return

        SystemMessages().success('✅ Tarefas do NetSuite foram executadas com sucesso!')

        if not get_all_files_in_download_dir():
            progress_repository.drop_progress_table()

if __name__ == '__main__':
    check_playwright_install()

    retry = RetryExecuter()
    connection = DuckConnection(access_dir(
        'docs\database', 'companies.duckdb')).connect()
    progress_repository = ProgressRepository(connection)

    asyncio.run(retry.run(do_itau_tasks))
    asyncio.run(retry.run(do_netsuite_tasks))
