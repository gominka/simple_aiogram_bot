import logging
from typing import Callable, Union
import functools
from json import JSONDecodeError

from aiogram import types
from aiogram.fsm.context import FSMContext
from peewee import IntegrityError
from requests import ConnectTimeout, RequestException, HTTPError, Timeout

from loader import bot
from user_interface import text

logger = logging.getLogger(__name__)
TIMEOUT = 10


def handle_request_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except (ConnectTimeout, Timeout):
            logger.error("Connection timed out. Please check your internet connection or try again later.")
            return None
        except HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
        return None

    return wrapper


def exc_handler(method: Callable) -> Callable:
    """ Decorator. Logs the exception to the called function, notifies the user of the error """

    @functools.wraps(method)
    async def wrapped(message: Union[types.Message, types.CallbackQuery], state: FSMContext = None) -> None:
        try:
            await method(message, state)
        except ValueError as exception:
            if isinstance(message, types.CallbackQuery):
                message = message.message
            if exception.__class__.__name__ == 'JSONDecodeError':
                await exc_handler(method)(message, state)
            else:
                error_message = "Enter a valid number"
                await message.answer(text=error_message)
                await bot.register_next_step_handler(message=message, callback=exc_handler(method))

        except IntegrityError:
            await message.answer(text=text.HELP_MSG)

        except Exception as e:
            logger.exception("An unexpected error occurred:")
            await message.answer("To start the search, click /start")

    return wrapped