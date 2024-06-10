from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard import builder
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile, CallbackQuery
import os
from aiogram.fsm.state import State, StatesGroup
from handlers.states import Favourites
from aiogram.fsm.state import default_state
from handlers.start import cmd_menu

router = Router()

@router.callback_query(F.data == '⭐')
async def star_welcome(callback: CallbackQuery, state: FSMContext):
    a = await state.get_data()
    if 'stars' in a:
        await state.update_data(stars=a['stars'] + '\n---\n' + callback.message.text)
    else:
        await state.update_data(stars=callback.message.text)
    await callback.message.answer(f'Добавлено в избранное \'{a["app"]}\'!')
    await cmd_menu(callback.message, state)
