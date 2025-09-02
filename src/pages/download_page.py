from src.pages.base_page import BasePage
from src.utils.common_utils import SystemMessages
from src.utils.errors_utils import LocatorTimeoutPlaywright
from playwright.sync_api import expect


class DownloadPage(BasePage):
    def __init__(self, page, date_begin: str, date_end: str, base_url=None):
        super().__init__(page, base_url)
        self.__date_begin = date_begin
        self.__date_end = date_end

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
        await self.page.wait_for_timeout(30000)
        await self.iframe_page.content_frame.get_by_role("combobox", name="data").click()
        await self.iframe_page.content_frame.get_by_text("Outra data ou período").click()
        await self.__insert_date_interval()
        await self.iframe_page.content_frame.get_by_role("button", name="buscar").click()
        try:
            # VERIFICA SE EXISTE ALGUM COMPROVANTE, SE NÃO, LANÇA EXCEPTION
            locator = self.iframe_page.content_frame.get_by_text(
                "nenhum pagamento encontrado")
            await locator.wait_for(timeout=2500)
        except LocatorTimeoutPlaywright.TimeoutError:
            # VERIFICA SE EXISTE O TUTORIAL, SE NÃO, LANÇA EXCEPTION
            await self.iframe_page.content_frame.get_by_role("button", name="Fechar tutorial").click(timeout=2500)

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
