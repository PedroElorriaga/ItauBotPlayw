from src.pages.base_page import BasePage
from src.utils.common_utils import access_dir
from src.services.system_messages import SystemMessages


class UploadPage(BasePage):
    def __init__(self, page, base_url=None):
        super().__init__(page, base_url)

    async def upload_file(self, file: str):
        total_element_text = await self.page.locator('#uir-total-count').inner_text()
        if total_element_text.split(':')[1].strip() == '0':
            SystemMessages().error('Nenhum comprovante encontrado')
            return

        try:
            # VERIFICA SE A FATURA É PRÉ PAGAMENTO
            await self.page.get_by_role("link", name="Pré-pagamento ao fornecedor #").click(timeout=3000)
            SystemMessages().error('Comprovante com Status de pré pagamento')
            return
        except:
            pass

        await self.page.get_by_role("link", name="Fatura #").click(timeout=3000)
        await self.page.wait_for_timeout(2000)
        await self.page.locator("#main_form").get_by_role("listitem").filter(has_text="arquivo Nova nota Status").get_by_role("link").click()

        # PAGINA NO CONTEXTO DO POPUP
        async with self.page.expect_popup() as pageup:
            await self.page.get_by_role("button", name="arquivo").click()

        SystemMessages().log('Enviando comprovantes...')

        page_popup = await pageup.value
        await page_popup.get_by_role("textbox", name="Nome do arquivo").fill(file)
        await page_popup.set_input_files('input[type="file"]', access_dir('docs/downloads', file))
        await page_popup.wait_for_timeout(1500)
        await page_popup.get_by_role("button", name="Salvar").click()
        await page_popup.close()
