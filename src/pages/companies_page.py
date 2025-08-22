from src.pages.base_page import BasePage
from typing import List


class CompaniesPage(BasePage):
    def __init__(self, page, base_url=None, companies_to_execute: List[str] = []):
        super().__init__(page, base_url)
        self.companies_to_execute = companies_to_execute

    async def get_accounts(self):
        await self.page.get_by_role("button", name="Trocar de conta").click()
        await self.page.get_by_role("radio", name="Múltiplas contas").click()

        change_account_shadow_root = self.page.locator('mf-lista-contas')
        first_account_from_tr = change_account_shadow_root.locator(
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
        accounts_from_tr = await change_account_shadow_root.locator('ul#list-accounts-container li').all()
        accounts = []
        index = 1

        for account in accounts_from_tr:
            account_span = await account.locator('button.switch-account span').all()

            name = await account_span[0].inner_text()
            agency = await account_span[1].inner_text()
            number = await account_span[2].inner_text()
            cnpj = await account_span[3].inner_text()

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

        return accounts
