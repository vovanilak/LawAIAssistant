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
from handlers.states import Gip
from aiogram.fsm.state import default_state
from handlers.start import cmd_menu
from gpt.main import GPT

router = Router()

@router.callback_query(Gip.welcome, F.data.in_(('1', '2', '3', '4', '5', '6')))
async def gip_welcome(call: CallbackQuery, state: FSMContext):
    await state.set_state(default_state)
    dct = {
        1: 'На основании чего плательщик страховых взносов исчисляет сумму страховых взносов?',
        2: 'На какой период осуществляется перерасчет сумм ранее исчисленных налогов?',
        3: 'Какие сведения должны быть указаны в налоговом уведомлении?',

        4: 'Может ли в налоговом уведомлении указываться информация по нескольким подлежащим уплате налогам?',
        5: 'Какие виды уведомления может получить налогоплательщик?',
        6: 'Если налогоплательщик не получает налоговое уведомление по почте, в каком случае оно считается полученным?'
    }
    gp = GPT(mode='tuned')
    txt = dct[int(call.data)]
    await call.message.answer(txt)
    await call.message.answer(gp.gpt_request(txt))
    await cmd_menu(call.message, state)

@router.callback_query(Gip.welcome, F.data=='Другое')
async def gip_welcome2(call: CallbackQuery, state: FSMContext):
    await state.set_state(Gip.answer)
    await call.message.answer('Задай вопрос обученной модели')

@router.message(Gip.answer)
async def gip_question(message: Message, state: FSMContext):
    await state.set_state(default_state)
    try:
        gp = GPT(mode='tuned')
        await message.answer(gp.gpt_request(message.text))
    except Exception as e:
        await message.answer('Возникла ошибка, попробуй ещё раз\n' + str(e))
    await cmd_menu(message, state)
