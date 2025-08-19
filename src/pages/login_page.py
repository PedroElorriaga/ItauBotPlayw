from src.pages.base_page import BasePage
from src.config.settings import ItauConfigs


class LoginPage(BasePage):
    async def goto_login(self):
        await self.open_url()
        await self.page.get_by_role("button", name="Mais acessos").click()

        await self.make_login_using_operator()

    async def make_login_using_operator(self):
        await self.page.get_by_label("Opções de acesso").click()
        await self.page.keyboard.press("ArrowDown")
        await self.page.keyboard.press("Enter")

        await self.page.get_by_role("dialog", name="Acesse sua conta").get_by_label("Código do operador").fill(ItauConfigs.OPERADOR_ITAU)
        await self.page.keyboard.press("Enter")
        await self.page.get_by_role("dialog", name="Acesse sua conta").get_by_label("Acessar").click()
        await self.enter_virtual_keyboard_password()

    async def enter_virtual_keyboard_password(self):
        password_list = [number for number in ItauConfigs.PASSWORD_ITAU]
        await self.page.wait_for_selector('.teclado.clearfix')
        await self.page.wait_for_timeout(1000)
        keyboards_elements = await self.page.locator('#campoTeclado').all()
        keyboards_numbers = [(keyboard, await keyboard.inner_text())
                             for keyboard in keyboards_elements]

        for password in password_list:
            for keyboard, text in keyboards_numbers:
                if password in text:
                    await keyboard.click()

        await self.page.get_by_role("button", name="acessar").click()
        await self.select_access_type_authentication()

    async def select_access_type_authentication(self):
        await self.page.wait_for_selector('#rdBasico')
        await self.page.locator('#rdBasico').click()
        await self.page.get_by_role("button", name="Continuar").click()
        await self.page.wait_for_timeout(5000)
