from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["SA_B_1"], callback_data="bot_stats_sudo"),
                InlineKeyboardButton(text=_["SA_B_2"], callback_data="TopOverall")
            ],
            [
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl

def back_stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="GETSTATS"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )
    return upl
