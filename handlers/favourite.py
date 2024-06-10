from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboard import builder
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile
import os
from aiogram.fsm.state import State, StatesGroup
from handlers.states import Favourites
from aiogram.fsm.state import default_state
from handlers.start import cmd_menu

router = Router()

@router.callback_query(Favourites.welcome)
async def fav_welcome(call: CallbackQuery, state: FSMContext):
    a = await state.get_data()
    if 'stars' in a:
        for mes in a['stars'].split('\n---\n'):
            await call.message.answer(mes)
    else:
        await call.message.answer('В избранном пока ничего нет!')
    await cmd_menu(call.message, state)