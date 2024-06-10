from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboard import builder
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from handlers.states import App
from aiogram.fsm.state import default_state
from handlers.start import cmd_menu
from gpt.main import GPT

router = Router()

@router.callback_query(App.welcome)
async def app_welcome(call: CallbackQuery, state: FSMContext):
    await state.update_data(app=call.data)
    await call.answer()
    if call.data == 'Поиск':
        await state.set_state(App.search)
        await call.message.answer(
            text='Что хотите найти?',
            reply_markup=builder.reply(('Судебные дела', "Законы и справочники"))
        )

    elif call.data == 'Анализ':
        await state.set_state(App.analysis)
        await call.message.answer(
            text='Что хотите анализировать?',
            reply_markup=builder.reply(('Связи документов', "Судебная практика", "Гражданская ситуация"))
        )

    elif call.data == 'Калькуляторы':
        await state.set_state(App.calculator)
        await call.message.answer(
            text='Выбери калькулятор',
            reply_markup=builder.reply(('Индексация зарплаты', "НДФЛ"))
        )

    elif call.data == 'Прогнозы':
        await state.set_state(App.forecast)
        await call.message.answer(
            text='Выбери прогноз',
            reply_markup=builder.reply(('Исход дела', "Риски"))
        )
        
@router.message(App.search)
async def app_search(message: Message, state: FSMContext):
    await state.set_state(App.deal)
    await message.answer('Напишите в свободной форме, что хотите найти', reply_markup=ReplyKeyboardRemove())

@router.message(App.deal)
async def app_deal(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer("Найдены следующие результаты:\n...", reply_markup=builder.inline(('⭐',)))
    await cmd_menu(message, state)
    
@router.message(App.analysis)
async def app_analyze(message: Message, state: FSMContext):
    if message.text == 'Связи документов':
        await state.set_state(App.links)
        await message.answer('Введите документ', reply_markup=ReplyKeyboardRemove())
    else:
        await state.set_state(App.situation)
        await message.answer('Опишите в свободной форме свою ситуацию', reply_markup=ReplyKeyboardRemove())

@router.message(App.links)
async def app_links(message: Message, state: FSMContext):
    await state.set_state(App.situation)
    await message.answer("Найдены следующие результаты:\n...", reply_markup=builder.inline(('⭐',)))
    await cmd_menu(message, state)
        
@router.message(App.situation)
async def app_situation(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer('Генерирую ответ')
    gp = GPT(mode='vanila')
    await message.answer(str(gp.gpt_request(message.text)), reply_markup=builder.inline(('⭐',)))
    await cmd_menu(message, state)

@router.message(App.calculator)
async def app_calculators(message: Message, state: FSMContext):
    if message.text == 'НДФЛ':
        await state.set_state(App.nalog)
        await message.answer('Введите зарплату работника', reply_markup=ReplyKeyboardRemove())

    else:
        await state.set_state(default_state)
        await message.answer('В разработке')
        await cmd_menu(message, state)
        
@router.message(App.nalog, F.text.isdigit())
async def app_nalog(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(f"Результат: {int(message.text) * 0.3}", reply_markup=builder.inline(('⭐',)))
    await cmd_menu(message, state)
    
@router.message(App.nalog)
async def app_nalog_error(message: Message, state: FSMContext):
    await message.answer('Неверный ввод. Используйте только цифры. Пожалуйста, попробуйте заново')

@router.message(App.forecast)
async def app_forecasts(message: Message, state: FSMContext):
    await state.set_state(App.sud)
    await message.answer("Пожалуйста, опишите свою ситуцию", reply_markup=ReplyKeyboardRemove())
    
@router.message(App.sud)
async def app_sud(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await message.answer(f"Я решаю, что ...", reply_markup=builder.inline(('⭐',)))
    await cmd_menu(message, state)