from src.pages.base_page import BasePage
from src.utils.common_utils import access_download_dir, check_if_data_dont_have_special_character, SystemMessages
from src.utils.errors_utils import LocatorTimeoutPlaywright


class DownloadPage(BasePage):
    def __init__(self, page, date_begin: str, date_end: str, base_url=None):
        super().__init__(page, base_url)
        self.__date_begin = date_begin
        self.__date_end = date_end
        self.payment_receipts = []

    async def search_payments(self):
        self.iframe_page = self.page.locator('iframe.iframe-nf2')
        chat_itau_element = self.iframe_page.content_frame.locator(
            '#floatAjudaMovel')
        await chat_itau_element.evaluate("""
            () => {
                const btn = document.querySelector('#floatAjudaMovel');
                if (btn) btn.style.pointerEvents = 'none';
            }
        """)
        await self.iframe_page.content_frame.get_by_role("combobox", name="data").click()
        await self.iframe_page.content_frame.get_by_text("Outra data ou período").click()
        await self.__insert_date_interval()
        await self.iframe_page.content_frame.get_by_role("button", name="buscar").click()
        try:
            # VERIFICA SE EXISTE ALGUM COMPROVANTE, SE NÃO, LANÇA EXCEPTION
            locator = self.iframe_page.content_frame.get_by_text(
                "nenhum pagamento encontrado")
            await locator.wait_for(timeout=2500)
            return SystemMessages().error('Nenhum pagamento encontrado!')
        except LocatorTimeoutPlaywright.TimeoutError:
            try:
                # VERIFICA SE EXISTE O TUTORIAL, SE NÃO, LANÇA EXCEPTION
                await self.iframe_page.content_frame.get_by_role("button", name="Fechar tutorial").click(timeout=2500)
            except LocatorTimeoutPlaywright.TimeoutError:
                pass
        payments_receipt_trs = await self.iframe_page.content_frame.locator('#new-table tbody tr').all()
        SystemMessages().log('Baixando comprovantes...')

        for tr in payments_receipt_trs:
            payment_receipt_spans = await tr.locator('span').all()
            payment_receipt_status = await payment_receipt_spans[6].inner_text()

            if payment_receipt_status == 'Efetuado':
                payment_receipt = {
                    'receipt_date': await payment_receipt_spans[4].inner_text(),
                    'receipt_company': await payment_receipt_spans[0].inner_text(),
                    'receipt_value': await payment_receipt_spans[5].inner_text()
                }
                self.payment_receipts.append(payment_receipt)
                await payment_receipt_spans[7].click()

                async with self.page.expect_download() as download_info:
                    await self.iframe_page.content_frame.get_by_text("salvar_outline salvar em PDF").click()

                download = await download_info.value
                filename = (f'{payment_receipt["receipt_date"].replace("/", ".")}'
                            f'_{payment_receipt["receipt_company"]}'
                            f'_R$-{payment_receipt["receipt_value"]}.pdf')

                await download.save_as(access_download_dir(check_if_data_dont_have_special_character(filename)))
                await self.iframe_page.content_frame.get_by_role("button", name="fechar").click()
                await self.page.wait_for_timeout(1000)

        SystemMessages().success('Comprovantes baixados com sucesso!')

    async def __insert_date_interval(self):
        await self.iframe_page.content_frame.get_by_role("textbox", name="data inicial").click()
        await self.page.wait_for_timeout(1500)
        await self.page.keyboard.press("ControlOrMeta+A")
        await self.page.keyboard.press("Delete")
        await self.iframe_page.content_frame.get_by_role("textbox", name="data inicial").fill(self.__date_begin)
        await self.iframe_page.content_frame.get_by_role("textbox", name="data final (opcional)").click()
        await self.page.wait_for_timeout(1500)
        await self.iframe_page.content_frame.get_by_role("textbox", name="data final (opcional)").fill(self.__date_end)
        await self.page.wait_for_timeout(1000)
