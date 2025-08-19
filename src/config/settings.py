from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

load_dotenv()


class PlaywrightsConfigs:
    async def __aenter__(self):
        self.pw = await async_playwright().start()
        chromium = self.pw.chromium
        self.browser = await chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        self.context = await self.browser.new_context(no_viewport=True)
        return self.context

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
        await self.pw.stop()


class ItauConfigs:
    OPERADOR_ITAU = os.getenv('OPERADOR_ITAU')
    PASSWORD_ITAU = os.getenv('PASSWORD_ITAU')
