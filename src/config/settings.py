from playwright.async_api import async_playwright
from src.utils.common_utils import read_json_file
import os


class PlaywrightsConfigs:
    async def __aenter__(self):
        self.pw = await async_playwright().start()
        chromium = self.pw.chromium

        is_ci = os.environ.get('CI') == 'true'
        viewport_size = None

        if is_ci:
            viewport_size = {"width": 1920, "height": 1080}

        self.browser = await chromium.launch(
            headless=is_ci,
            args=['--start-maximized']
        )
        self.context = await self.browser.new_context(no_viewport=True, viewport=viewport_size)
        return self.context

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
        await self.pw.stop()


class ItauConfigs:
    __configSettings = read_json_file('data')['settings']['itau']
    __configInputData = read_json_file('data')['input_data']

    OPERATOR_ITAU = __configSettings['operator']
    PASSWORD_ITAU = __configSettings['password']
    COMPANIES_TO_EXECUTE = __configInputData['companies_to_execute']
    DATE_BEGIN = __configInputData['date_begin']
    DATE_END = __configInputData['date_end']


class NetsuiteConfigs:
    __configSettings = read_json_file('data')['settings']['netsuite']

    USER_NETSUITE = __configSettings['user']
    PASSWORD_NETSUITE = __configSettings['password']
    ANSWERS = [
        (__configSettings['security1']['question'],
         __configSettings['security1']['answer']),
        (__configSettings['security2']['question'],
         __configSettings['security2']['answer']),
        (__configSettings['security3']['question'],
         __configSettings['security3']['answer'])
    ]
