from src.pages.base_page import BasePage
from src.utils.common_utils import access_download_dir, SystemMessages


class UploadPage(BasePage):
    def __init__(self, page, base_url=None):
        super().__init__(page, base_url)

    async def upload_file(self, file: str):
        SystemMessages().log('Enviando comprovantes...')

        total_element_text = await self.page.locator('#uir-total-count').inner_text()
        if total_element_text.split(':')[1].strip() == '0':
            SystemMessages().error('Nenhum comprovante encontrado')
            return

        await self.page.get_by_role("link", name="Fatura #").click()
        await self.page.locator("#main_form").get_by_role("listitem").filter(has_text="arquivo Nova nota Status").get_by_role("link").click()

        # PAGINA NO CONTEXTO DO POPUP
        async with self.page.expect_popup() as pageup:
            await self.page.get_by_role("button", name="arquivo").click()

        page_popup = await pageup.value
        await page_popup.get_by_role("textbox", name="Nome do arquivo").fill(file)
        await page_popup.set_input_files('input[type="file"]', access_download_dir(file))
        await page_popup.wait_for_timeout(1500)
        await page_popup.get_by_role("button", name="Salvar").click()
        await page_popup.close()
