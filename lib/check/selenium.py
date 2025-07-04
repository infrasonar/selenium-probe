import os
import asyncio
from selenium import webdriver
from libprobe.asset import Asset
from libprobe.exceptions import IncompleteResultException, Severity
from ..module import get_module


_lock = asyncio.Lock()
COMMAND_EXECUTER = os.getenv("COMMAND_EXECUTER", "http://localhost:4444")


async def check_selenium(
        asset: Asset,
        asset_config: dict,
        config: dict) -> dict:
    exc = None
    items = []
    password = asset_config.get('password')
    secret = asset_config.get('secret')
    file_ids: list[int] = config.get('file_ids', [])
    for file_id in file_ids:
        async with _lock:
            if password:
                os.environ['PASSWORD'] = password
            if secret:
                os.environ['SECRET'] = secret
            try:
                try:
                    module = await get_module(file_id=file_id)
                except Exception as e:
                    exc = e
                    continue

                options = webdriver.ChromeOptions()
                driver = webdriver.Remote(
                    options=options,
                    command_executor=COMMAND_EXECUTER)

                try:
                    item = module.export.run(name=str(file_id), driver=driver)
                except Exception as e:
                    # When `run() is correct, it can't fail` as potential
                    # errors will be part of the result
                    msg = str(e) or type(e).__name__
                    raise Exception(
                        f'The `export` in file ID {file_id} is not a valid '
                        f'subclass of `TestBase` (error: {msg})')
                else:
                    items.append(item)
            finally:
                os.environ.pop('PASSWORD', None)
                os.environ.pop('SECRET', None)

    if exc is not None and not items:
        raise exc

    total = {
        'name': 'total',  # str
        'success_count': sum(i['success'] for i in items),  # int
        'failed_count': sum(not i['success'] for i in items),  # int
        'num_checks': len(items),  # int
        'total_duration': sum(i['duration'] for i in items),  # float
    }

    state = {
        'total': [total],  # single item
        'tests': items,  # multi item
    }

    if exc is not None:
        msg = str(exc) or type(exc).__name__
        raise IncompleteResultException(
            msg=msg,
            result=state,
            severity=Severity.LOW)

    return state
