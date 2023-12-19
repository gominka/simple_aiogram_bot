from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from database.models import User
from loader import dp

from user_interface import text

router = Router()


class StartState(StatesGroup):
    start_state = State()


def get_user_info(message: types.Message) -> tuple:
    """Retrieve user information from a Telegram message."""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    return user_id, username, first_name, last_name, chat_id


def create_and_save_user(user_id, username, first_name, last_name):
    """Create a new User object and save it to the database."""
    User(user_id=user_id, username=username, first_name=first_name, last_name=last_name).save()


@dp.message(Command(commands=["start"]))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start command."""

    await state.set_state(StartState.start_state)
    await message.reply(text.START_MSG)


@dp.message(Command("start_again"))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start_again command."""

    user_id, _, _, _, chat_id = get_user_info(message)

    await message.reply(text="Previously selected conditions have been reset")
    await state.clear()
    await message.answer(text=text.HELP_MSG)

