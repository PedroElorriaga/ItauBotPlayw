from typing import Callable, Awaitable, Any
from src.services.system_messages import SystemMessages


class RetryExecuter:
    def __init__(self):
        self.attempts = 5
        self.exception = Exception

    async def run(self, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        attempts = self.attempts
        while attempts > 0:
            try:
                return await func(*args, **kwargs)
            except self.exception as err:
                SystemMessages().log('Retrying again...')
                attempts -= 1
                if attempts == 0:
                    SystemMessages().error(f'RetryExecuter -> {str(err)}')
                    raise
