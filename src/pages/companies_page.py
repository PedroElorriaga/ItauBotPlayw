from src.pages.base_page import BasePage
from typing import List
from src.utils.common_utils import SystemMessages
from src.utils.errors_utils import LocatorTimeoutPlaywright


class CompaniesPage(BasePage):
    def __init__(self, page, base_url=None, companies_to_execute: List[str] = []):
        super().__init__(page, base_url)
        self.companies_to_execute = companies_to_execute

    async def get_accounts(self):
        await self.page.get_by_role("button", name="Trocar de conta").click()
        await self.page.get_by_role("radio", name="Múltiplas contas").click()

        self.iframe_page = self.page.locator('mf-lista-contas')

        first_account_from_tr = self.iframe_page.locator(
            'ul.ids-list li')
        first_account_spans = await first_account_from_tr.locator('span').all()
        default_account = {
            'index': 0,
            'name': await first_account_spans[0].inner_text(),
            'agency': await first_account_spans[1].inner_text(),
            'number': await first_account_spans[2].inner_text(),
            'cnpj': await first_account_spans[3].inner_text()
        }

        await self.page.get_by_role("radio", name="Conta", exact=True).click()
        accounts_from_trs = await self.iframe_page.locator('ul#list-accounts-container li').all()
        accounts = []
        index = 1

        for account in accounts_from_trs:
            account_spans = await account.locator('button.switch-account span').all()

            name = await account_spans[0].inner_text()
            agency = await account_spans[1].inner_text()
            number = await account_spans[2].inner_text()
            cnpj = await account_spans[3].inner_text()

            account_company = f'{name} - {cnpj}'
            is_account_company_included = account_company in self.companies_to_execute
            can_execute_company = True if len(
                self.companies_to_execute) == 0 else is_account_company_included
            """ 
            can_execute_company -> SEMPRE RETORNA VERDADEIRO SE A LISTA companies_to_execute
            FOR VAZIA, SE A LISTA NÃO FOR VAZIA ELA IRÁ RETORNAR O
            VALOR DA VARIAVEL is_account_company_included (TRUE OU FALSE)

            ESSA LÓGICA PERMITE QUE TODAS AS EMPRESAS QUE POSSAM SER EXECUTADAS SEJAM
            ADICIONADAS A LISTA accounts, CASO A LISTA DE companies_to_execute FOR VAZIA
            E EXECUTA APENAS AS EMPRESAS QUE ESTÃO NA LISTA DE companies_to_execute CASO 
            ELA NÃO SEJA VAZIA
            """
            if can_execute_company:
                accounts.append({
                    'index': index,
                    'name': name,
                    'agency': agency,
                    'number': number,
                    'cnpj': cnpj
                })
                index += 1

        if len(self.companies_to_execute) > 0:
            if default_account['name'] == self.companies_to_execute[0].split('-')[0].strip():
                accounts.insert(0, default_account)
        else:
            accounts.insert(0, default_account)

        await self.iframe_page.get_by_role("button", name="fechar").click()

        return accounts

    async def change_account(self, account: dict):
        await self.page.get_by_role("button", name="Trocar de conta").click()
        self.iframe_page = self.page.locator('mf-lista-contas')
        accounts_from_trs = await self.iframe_page.locator('ul#list-accounts-container li').all()

        for tr in accounts_from_trs:
            account_spans = await tr.locator('button.switch-account span').all()

            name = await account_spans[0].inner_text()
            cnpj = await account_spans[3].inner_text()

            if name == account['name'] and cnpj == account['cnpj']:
                await account_spans[0].click()
                await self.page.wait_for_selector('dialog.ids-alert--success')
                SystemMessages().log(
                    f'Conta trocada para {name} - {cnpj}')
                return

    async def goto_download_company_page(self):
        try:
            await self.page.get_by_role("menuitem", name="Contas a pagar botão", exact=True).click()
            await self.page.wait_for_timeout(1000)
            await self.page.get_by_role("menuitem", name="Ir para Contas a pagar botão").click(timeout=4500)
            await self.page.wait_for_timeout(1500)
        except LocatorTimeoutPlaywright.TimeoutError:
            await self.page.get_by_role("tab", name="Fechar guia - consultar").click()
            await self.page.wait_for_timeout(2500)
            return await self.goto_download_company_page()
        except Exception as err:
            SystemMessages().error('Algum erro inesperado aconteceu :(')
            raise Exception(err)

        self.iframe_page = self.page.locator('iframe.iframe-nf2')
        await self.iframe_page.content_frame.get_by_role("link", name="Consultar pagamentos,").click()
