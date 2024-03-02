from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def queue_markup(_, CPLAY, videoid):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["QU_B_1"], callback_data=f"GetQueued {CPLAY}|{videoid}"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
    ]
    )
    return upl

def queue_back_markup(_, CPLAY):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"queue_back_timer {CPLAY}"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl
