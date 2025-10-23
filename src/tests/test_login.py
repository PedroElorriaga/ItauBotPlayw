from src.config.settings import PlaywrightsConfigs
from src.pages.itau_page.login_page import LoginPageItau
import os
import pytest


@pytest.mark.asyncio
async def test_login_itau():
    operator = os.environ.get('OPERATOR_ITAU')
    password = os.environ.get('PASSWORD_ITAU')

    if operator == None and password == None:
        raise EnvironmentError(
            'As variáveis "OPERATOR_ITAU" e "PASSWORD_ITAU" devem ser configuradas.')

    async with PlaywrightsConfigs() as context:
        login_itau = LoginPageItau(
            await context.new_page(), operator, password, 'https://www.itau.com.br/itaubba-pt')
        await login_itau.goto_login()
