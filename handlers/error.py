
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboard import builder
from aiogram.fsm.context import FSMContext
import os
from aiogram.fsm.state import default_state
from handlers.start import cmd_menu

router = Router()

@router.message()
async def cmd_menu(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer('Что-то пошло не так. Перевожу на главное меню')
    await cmd_menu(message, state)
    
@router.callback_query()
async def cmd_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    await callback.message.answer('Что-то пошло не так. Перевожу на главное меню')
    await callback.message.answer(
        text='Выберите действие',
        reply_markup=builder.reply(
            ('Личный кабинет', "Каталог приложений", "Избранное", "Настройки")
        )
    )