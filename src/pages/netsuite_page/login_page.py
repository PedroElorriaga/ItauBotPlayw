from src.pages.base_page import BasePage
from src.utils.common_utils import SystemMessages
from src.utils.errors_utils import LocatorTimeoutPlaywright


class LoginPageNetsuite(BasePage):
    def __init__(self, page, user_netsuite: str, password_netsuite: str, security_netsuite: list[tuple], base_url: str = None):
        super().__init__(page, base_url)
        self.__user_netsuite = user_netsuite
        self.__password_netsuite = password_netsuite
        self.__security_netsuite = security_netsuite

    async def goto_login(self):
        await self.open_url()

        await self.__insert_login_infos()

    async def __insert_login_infos(self):
        await self.page.get_by_role("textbox", name="Email address").fill(self.__user_netsuite)
        await self.page.get_by_role("textbox", name="Password").fill(self.__password_netsuite)
        await self.page.get_by_role("button", name="Log In").click()

        await self.__select_account_type()

    async def __select_account_type(self):
        try:
            await self.page.get_by_role("row", name="Grupo Arch Capital PRODUCTION").get_by_role("link").click(timeout=3500)
            await self.page.wait_for_timeout(3000)

            await self.__answer_security_question()

            SystemMessages().success('Login netsuite efetuado com sucesso!')
        except LocatorTimeoutPlaywright.TimeoutError:
            SystemMessages().success('Login netsuite efetuado com sucesso!')
        except Exception as err:
            SystemMessages().error('Algum erro inesperado aconteceu :(')
            raise Exception(err)

    async def __answer_security_question(self):
        question_tds = await self.page.locator('.smalltextnolink.text-opensans').all()
        answer_input = self.page.locator('.input.hidepassword')

        for security in self.__security_netsuite:
            if await question_tds[2].inner_text() in security:
                await answer_input.fill(security[1])
                await self.page.get_by_role("button", name="Enviar").click()
                break
