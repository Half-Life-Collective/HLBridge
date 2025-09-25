# SPDX-License-Identifier: MIT
# Copyright (c) 2018-2024 Amano LLC

from __future__ import annotations

from hydrogram import Client, filters
from hydrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from hlbridge.utils import commands ,get_version_number, get_commit
from hlbridge.utils.localization import Strings, use_chat_lang


# Using a low priority group so deeplinks will run before this and stop the propagation.
@Client.on_message(filters.command("start") & filters.private, group=2)
@Client.on_callback_query(filters.regex("^start_back$"))
@use_chat_lang
async def start_pvt(c: Client, m: Message | CallbackQuery, s: Strings):
    if isinstance(m, CallbackQuery):
        msg = m.message
        send = msg.edit_text
    else:
        msg = m
        send = msg.reply_text

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(s("start_commands_btn"), callback_data="commands"),
                InlineKeyboardButton(s("start_infos_btn"), callback_data="infos"),
            ],
            [
                InlineKeyboardButton(s("start_language_btn"), callback_data="chlang"),
                InlineKeyboardButton(
                    s("start_add_to_chat_btn"),
                    url=f"https://t.me/{c.me.username}?startgroup=new",
                ),
            ],
        ]
    )
    await send(s("start_private"), reply_markup=keyboard)


@Client.on_message(filters.command("start") & filters.group, group=2)
@use_chat_lang
async def start_grp(c: Client, m: Message | CallbackQuery, s: Strings):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    s("start_chat"),
                    url=f"https://t.me/{c.me.username}?start=start",
                )
            ]
        ]
    )
    await m.reply_text(s("start_group"), reply_markup=keyboard)


@Client.on_callback_query(filters.regex("^infos$"))
@use_chat_lang
async def infos(c: Client, m: CallbackQuery, s: Strings):
    res = s("start_info_page").format(
        version_number=f"r{get_version_number()}",
        commit=get_commit(),
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(s("general_back_btn"), callback_data="start_back")]]
    )
    await m.message.edit_text(res, reply_markup=keyboard, disable_web_page_preview=True)


commands.add_command("start", "general")
