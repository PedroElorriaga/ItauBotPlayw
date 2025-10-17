from src.pages.base_page import BasePage
from src.utils.common_utils import convert_int_to_brl_currency
from src.services.system_messages import SystemMessages


class SearchPage(BasePage):
    def __init__(self, page, base_url=None):
        super().__init__(page, base_url)

    async def __goto_search_page(self):
        await self.open_url()

    async def search_receipt(self, file: str) -> bool:
        await self.__goto_search_page()

        file_splited = file.split('_ _')
        file_infos = {
            # TRANSFORMA A DATA EM DD/MM/YYYY
            'receipt_date': file_splited[0].replace('.', '/'),
            'receipt_name_beneficiary': file_splited[1],
            'receipt_cnpj_beneficiary': file_splited[2],
            # REMOVE O R$- NOME DO ARQUIVO
            'receipt_value': file_splited[3].split('R$-')[1],
            # REMOVE O .PDF NOME DO ARQUIVO
            'receipt_cnpj': file_splited[4].split('.pdf')[0]
        }

        return await self.__insert_infos_to_search(file_infos)

    async def __insert_infos_to_search(self, file_infos: dict) -> bool:
        SystemMessages().log(
            f'Procurando fornecedor {file_infos["receipt_name_beneficiary"]}...')

        await self.page.get_by_role("textbox", name="De").fill(file_infos['receipt_date'])
        await self.page.get_by_role("textbox", name="Até").fill(file_infos['receipt_date'])

        await self.page.get_by_role("combobox", name="Valor Parcela").click()
        await self.page.wait_for_timeout(1500)
        await self.page.get_by_text("entre", exact=True).click()

        receipt_value_int = int(file_infos['receipt_value'].replace(
            '.', '').replace(',', ''))

        receipt_value_str_less = convert_int_to_brl_currency(
            receipt_value_int - 3)
        receipt_value_str_more = convert_int_to_brl_currency(
            receipt_value_int + 3)

        await self.page.get_by_role("cell", name="De Para", exact=True).get_by_label("De").fill(receipt_value_str_less)
        await self.page.get_by_role("textbox", name="Para").fill(receipt_value_str_more)

        await self.page.locator(
            "textarea[name=\"CUSTRECORD_SIT_PARCELA_L_FORNECEDOR_display\"]"
        ).fill(file_infos['receipt_name_beneficiary'])
        await self.page.locator("#div__body").click()
        await self.page.wait_for_timeout(2000)
        textarea_value = await self.page.locator("textarea[name=\"CUSTRECORD_SIT_PARCELA_L_FORNECEDOR_display\"]").input_value()

        if textarea_value.strip() == file_infos['receipt_name_beneficiary']:
            SystemMessages().error(
                f'Fornecedor {file_infos["receipt_name_beneficiary"]} não encontrado')
            return False

        await self.page.locator("#submitter").click()

        SystemMessages().success('Fornecedor Encontrado!')

        await self.page.wait_for_timeout(3000)
        return True
