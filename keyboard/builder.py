from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram import types

def reply(lst):
    builder = ReplyKeyboardBuilder()
    for j in lst:
        builder.add(types.KeyboardButton(text=j))
    return builder.adjust(2).as_markup(resize_keyboard=True)

def inline(lst):
    builder = InlineKeyboardBuilder()
    for i in lst:
        builder.button(text=i, callback_data=i)
    return builder.adjust(1).as_markup()

def inline2(lst):
    builder = InlineKeyboardBuilder()
    for i in lst:
        builder.button(text=i, callback_data=i)
    return builder.adjust(2).as_markup()