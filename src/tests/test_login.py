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
        page = await context.new_page()
        login_itau = LoginPageItau(
            page, operator, password, 'https://www.itau.com.br/itaubba-pt')
        try:
            await login_itau.goto_login()
        except TimeoutError as e:
            # 🚨 Ação para falha: Tira uma screenshot e salva no diretório de trabalho do CI
            screenshot_path = "failure_screenshot.png"
            await page.screenshot(path=screenshot_path)

            # (Opcional) Printa o HTML da página para debug
            html_content = await page.content()
            with open("failure_page.html", "w", encoding="utf-8") as f:
                f.write(html_content)

            print(
                f"DEBUG: Screenshot e HTML salvos em {screenshot_path} e failure_page.html")
            raise e  # Levanta o erro original para o teste falhar
