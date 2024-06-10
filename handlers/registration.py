from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard import builder
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile
import os
from aiogram.fsm.state import State, StatesGroup
from handlers.states import Registration
from aiogram.fsm.state import default_state

router = Router()



@router.message(Registration.email)
async def reg_email(message: Message, state: FSMContext):
    await state.set_state(Registration.password)
    await state.update_data(email=message.text)
    await message.answer(
        text='Пожалуйста, введите пароль'
    )

@router.message(Registration.password)
async def reg_password(message: Message, state: FSMContext):
    await state.set_state(Registration.send)
    await state.update_data(password=message.text)
    await message.answer(
        text='Вам на почту отправлен код подтверждения. Пожалуйста, вставьте его сюда'
    )
    

@router.message(Registration.send)
async def reg_send(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer('Код верный! Вы успешно зарегистрировались!')
    await message.answer(
        text='Воспользуйтесь /menu, чтобы открыть главное меню'
    )