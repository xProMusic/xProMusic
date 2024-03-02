from config import BANNED_USERS
from strings import get_command, get_string, languages_present

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from xMusic import app
from xMusic.utils.database import get_lang, set_lang
from xMusic.utils.decorators import ActualAdminCB, language, languageCB


# Command
LANGUAGE_COMMAND = get_command("LANGUAGE_COMMAND")


def lanuages_keyboard(_):
    keyboard = []
    board = []
    for i in languages_present:
        board.append(InlineKeyboardButton(text=languages_present[i], callback_data=f"languages:{i}"))
        if len(board) == 2:
            keyboard.append(board)
            board = []
    else:
        if board:
            keyboard.append(board)
    keyboard.append([
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
    ])
    return InlineKeyboardMarkup(keyboard)


@app.on_message(filters.command(LANGUAGE_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.id, message.chat.title), reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)

    if str(old) == str(langauge):
        return await CallbackQuery.answer(_["lang_1"], show_alert=True)

    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(_["lang_2"], show_alert=True)
    except:
        return await CallbackQuery.answer(_["lang_3"], show_alert=True)

    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(keyboard)
