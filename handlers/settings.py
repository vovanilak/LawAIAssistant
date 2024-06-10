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
from handlers.states import Settings 
from aiogram.fsm.state import default_state
from handlers.start import cmd_menu

router = Router()

@router.callback_query(Settings.welcome, F.data=='Сменить пароль')
async def settings_welcome(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Settings.old)
    await callback.message.answer(
        text='Пожалуйста, введите старый пароль'
    )

    
@router.message(Settings.old)
async def settings_old(message: Message, state: FSMContext):
    await state.set_state(Settings.new)
    await message.answer(
        text='Пожалуйста, введите новый пароль'
    )


@router.message(Settings.new)
async def settings_new(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer('Пароль успешно изменен!')
    await cmd_menu(message, state)
    

@router.callback_query(Settings.welcome, F.data=='Изменить уведомления')
async def settings_notifications(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Settings.choose)
    for mes in ('Новые законы', "Пополнение базы данных"):
        await callback.message.answer(mes, reply_markup=builder.inline(('✅', '❌')))


@router.callback_query(Settings.choose)
async def settings_choose(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(default_state)
    await callback.message.answer('Уведомления успешно изменены!')
    await cmd_menu(callback.message, state)