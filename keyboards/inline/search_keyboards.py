from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from site_ip.main_request import get_conditions_list

# Constants
CONTINUE_SEARCH_CALLBACK = "check_amount_products"
CANCEL_SEARCH_CALLBACK = "cancel_search_cond"
WEBSITE_LINK_CALLBACK = "website_link"
GO_TO_WEBSITE_TEXT = 'Go to the website'
CANCEL_TEXT = 'Cancel'


def create_name_selection_keyboard(params, selected_condition):
    """
    Create a custom keyboard using keyboa_maker with conditions.

    :param params: List of conditions.
    :param selected_condition: The currently selected condition.
    :return: InlineKeyboardMarkup.
    """

    buttons = [InlineKeyboardButton(text=condition, callback_data=condition) for condition in
               get_conditions_list(params=params, selected_condition=selected_condition)]

    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 5] for i in range(0, len(buttons), 5)])


def create_search_command_keyboard(search_cond):
    """
    Create an inline keyboard for search commands.

    :param search_cond: The current search condition.
    :return: InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text='Continue the search',
        callback_data=CONTINUE_SEARCH_CALLBACK))

    builder.add(types.InlineKeyboardButton(
        text=CANCEL_TEXT,
        callback_data=CANCEL_SEARCH_CALLBACK))

    if search_cond == "brand":
        builder.add(types.InlineKeyboardButton(
            text=GO_TO_WEBSITE_TEXT,
            callback_data=WEBSITE_LINK_CALLBACK))

    return builder


def create_website_link_keyboard(link):
    """Create a keyboard for a website link."""
    url_kb = InlineKeyboardMarkup()
    url_button = InlineKeyboardButton(text=GO_TO_WEBSITE_TEXT, url=link)
    cancel_button = InlineKeyboardButton(text=CANCEL_TEXT,
                                         callback_data='cancel')
    url_kb.row(url_button, cancel_button)
    return url_kb


def create_command_keyboard():
    search_command_markup = InlineKeyboardMarkup(row_width=3)
    custom_search = InlineKeyboardButton(text='Continue the search',
                                         callback_data=CONTINUE_SEARCH_CALLBACK)
    cancel = InlineKeyboardButton(text=CANCEL_TEXT,
                                  callback_data=CANCEL_SEARCH_CALLBACK)
    search_command_markup.row(custom_search, cancel)
    return search_command_markup
