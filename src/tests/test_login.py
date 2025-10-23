from src.config.settings import PlaywrightsConfigs
from src.pages.itau_page.login_page import LoginPageItau
import os
import pytest
from pathlib import Path


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
        base_path = Path(os.environ.get('GITHUB_WORKSPACE', '.'))

        try:
            await login_itau.goto_login()

        except TimeoutError as e:
            # 🚨 Usa o caminho absoluto garantido
            screenshot_path = base_path / "failure_screenshot.png"
            html_path = base_path / "failure_page.html"

            await page.screenshot(path=str(screenshot_path))

            html_content = await page.content()
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            print(
                f"DEBUG: Screenshot e HTML salvos em {screenshot_path} e {html_path}")
            raise e
