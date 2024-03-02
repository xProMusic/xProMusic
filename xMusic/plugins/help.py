from strings import helpers, get_command
from config import BANNED_USERS, SUPPORT_GROUP, START_IMG_URL, OWNER_ID

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from xMusic import app
from xMusic.misc import SUDOERS
from xMusic.utils import help_pannel
from xMusic.utils.decorators.language import language, languageCB
from xMusic.utils.inline.help import help_back_markup, private_help_panel


# Command
HELP_COMMAND = get_command("HELP_COMMAND")


@app.on_message(filters.command(HELP_COMMAND) & ~BANNED_USERS)
@language
async def _help(client, message: Message, _):
    if message.chat.type == ChatType.PRIVATE:
        keyboard = help_pannel(_)
        await message.reply_photo(photo=START_IMG_URL, caption=_["help_1"].format(SUPPORT_GROUP), reply_markup=keyboard)
    else:
        keyboard = private_help_panel(app.username)
        await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
@languageCB
async def helper_private(client, CallbackQuery: CallbackQuery, _):
    keyboard = help_pannel(_)
    await CallbackQuery.edit_message_text(_["help_1"].format(SUPPORT_GROUP), reply_markup=keyboard)


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    if cb == "hb9":
        if CallbackQuery.from_user.id not in SUDOERS:
            return await CallbackQuery.answer("This button is only for Sudoers.", show_alert=True)
        else:
            await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
            return await CallbackQuery.answer()
    elif cb == "hb4":
        if CallbackQuery.from_user.id != OWNER_ID:
            return await CallbackQuery.answer("This button is only for Owner.", show_alert=True)
        else:
            await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
            return await CallbackQuery.answer()
    elif cb == "hb7":
        if CallbackQuery.from_user.id != OWNER_ID:
            return await CallbackQuery.answer("This button is only for Owner.", show_alert=True)
        else:
            await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
            return await CallbackQuery.answer()
    elif cb == "hb12":
        if CallbackQuery.from_user.id != OWNER_ID:
            return await CallbackQuery.answer("This button is only for Owner.", show_alert=True)
        else:
            return await CallbackQuery.answer("This feature is now Removed.", show_alert=True)

    try:
        await CallbackQuery.answer()
    except:
        pass

    if cb == "hb1":
        await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
