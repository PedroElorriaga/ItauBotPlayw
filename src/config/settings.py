from playwright.async_api import async_playwright
from src.utils.common_utils import read_json_file


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
    OPERATOR_ITAU = read_json_file('data')['settings']['itau']['operator']
    PASSWORD_ITAU = read_json_file('data')['settings']['itau']['password']
    COMPANIES_TO_EXECUTE = read_json_file(
        'data')['input_data']['companies_to_execute']
    DATE_BEGIN = read_json_file('data')['input_data']['date_begin']
    DATE_END = read_json_file('data')['input_data']['date_end']
