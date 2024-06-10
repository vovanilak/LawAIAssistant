from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboard import builder
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile, CallbackQuery
import os
from aiogram.fsm.state import State, StatesGroup
from handlers.states import Account 
from aiogram.fsm.state import default_state
from keyboard import builder
from handlers.start import cmd_menu

router = Router()

@router.callback_query(Account.welcome)
async def account_welcome(call: CallbackQuery, state: FSMContext):
    if call.data == "Пополнить баланс":
        await state.set_state(Account.add_money)
        await call.message.answer("Введите сумму пополнения")
    elif call.data== "Узнать баланс":
        await state.set_state(default_state)
        await call.message.answer(
            text='Баланс (руб): 2560.00'
        )
        await cmd_menu(call.message, state)

@router.message(Account.add_money)
async def account_summ(message: Message, state: FSMContext):
    await state.set_state(Account.summ)
    await state.update_data(summ=message.text)
    await message.answer(
        text='Выберите способ пополнения',
        reply_markup=builder.inline(
            ("Карта", "СБП")
        )
    )
    
@router.callback_query(Account.summ)
async def account_summ(call: CallbackQuery, state: FSMContext):
    if call.data == "Карта":
        await state.set_state(Account.card)
        await call.message.answer("Введите номер карты")
    elif call.data == "СБП":
        await state.set_state(Account.sbp)
        await call.message.answer_photo(URLInputFile(
            'https://e7.pngegg.com/pngimages/611/718/png-clipart-qr-code-barcode-scanners-computer-icons-coder-miscellaneous-angle.png'),
            caption='Отсканируйте QR-код',
            reply_markup=builder.inline(('Готово!',))
        )
        
@router.message(Account.card)
async def account_card(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(
        text='Баланс пополнен!'
    )
    await cmd_menu(message, state)
    
@router.callback_query(Account.sbp)
async def account_qr(call: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    await call.message.answer(
        text='Баланс пополнен!'
    )
    await cmd_menu(callback.message, state)
