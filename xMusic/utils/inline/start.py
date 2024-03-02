from config import SUPPORT_GROUP
from pyrogram.types import InlineKeyboardButton


def start_pannel(BOT_USERNAME, _):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_1"], url=f"https://t.me/{BOT_USERNAME}?startgroup=new")
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], url=f"https://t.me/{BOT_USERNAME}?start=help"),
            InlineKeyboardButton(text=_["S_B_6"], callback_data="settings_helper")
        ]
        ]
    return buttons

def private_panel(BOT_USERNAME, _):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_1"], url=f"https://t.me/{BOT_USERNAME}?startgroup=new")
        ],
        [
            InlineKeyboardButton(text=_["S_B_3"], url="https://t.me/xProAssociation"),
            InlineKeyboardButton(text=_["S_B_2"], url=f"https://t.me/{SUPPORT_GROUP}")
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper"),
        ]
    ]
    return buttons
