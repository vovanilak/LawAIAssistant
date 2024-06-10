from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboard import builder
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import URLInputFile, FSInputFile
from handlers.states import Registration
from handlers import states
import os
from aiogram.enums import ParseMode
from keyboard import inline

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text='Привет👋 Это ИИ-бот предназначен для помощи юристам в поиске юридической информации и анализу гаржданской ситуации. Используй /reg для регистрации или /menu для вывода всех функций!'
    )

@router.message(Command('reg'))
async def cmd_reg(message: Message, state: FSMContext):
    await state.set_state(Registration.email)
    await message.answer(
        text='Пожалуйста, введите адрес электронной почты'
    )

@router.message(Command('menu'))
async def cmd_menu(message: Message, state: FSMContext):
    await message.answer(
        text='Выберите действие',
        reply_markup=builder.reply(
            ('Личный кабинет', "Каталог приложений", "Избранное", "Настройки", 'YaGPT', 'Статья')
        )
    )

@router.message(F.text.in_((
    ('Личный кабинет', "Каталог приложений", "Избранное", "Настройки",'YaGPT', 'Статья')
)))
async def menu_continue(message: Message, state: FSMContext):
    await message.answer('Меню🖲️', reply_markup=ReplyKeyboardRemove())
    if message.text == "Личный кабинет":
        await state.set_state(states.Account.welcome)
        await message.answer(
            text='Выберите действие',
            reply_markup=builder.inline(
                ('Пополнить баланс', 'Узнать баланс')
            )
        )
    elif message.text == "Каталог приложений":
        await state.set_state(states.App.welcome)
        await message.answer(
            text='Выберите приложение',
            reply_markup=builder.inline(
                ("Поиск", "Анализ", 'Калькуляторы', "Прогнозы" )
            )
        )
        
    elif message.text == "Избранное":
        await state.set_state(states.Favourites.welcome)
        await message.answer(
            text='Выберите категорию',
            reply_markup=builder.inline(
                ("Поиск", "Анализ", 'Калькуляторы', "Прогнозы" )
            )
        )
    elif message.text == "Настройки":
        await state.set_state(states.Settings.welcome)
        await message.answer(
            text='Настройки',
            reply_markup=builder.inline(
                ('Сменить пароль', "Изменить уведомления")
            )
        )
    elif message.text == 'YaGPT':
        await state.set_state(states.Gip.welcome)
        await message.answer(
            text="""
Вопросы из обучающей выборки:
1. На основании чего плательщик страховых взносов исчисляет сумму страховых взносов?
2. На какой период осуществляется перерасчет сумм ранее исчисленных налогов?
3. Какие сведения должны быть указаны в налоговом уведомлении?

Вопросы из тестовой выборки:
4. Может ли в налоговом уведомлении указываться информация по нескольким подлежащим уплате налогам?
5. Какие виды уведомления может получить налогоплательщик?
6. Если налогоплательщик не получает налоговое уведомление по почте, в каком случае оно считается полученным?
""",
            reply_markup=builder.inline2(
                [str(i) for i in range(1, 7)] + ['Другое']
            )
        )
    elif message.text == 'Статья':
        await message.answer(
            text='НК РФ Статья 52. Порядок исчисления налога, сбора, страховых взносов',
            reply_markup=inline.url(
                'Ссылка',
                'https://www.consultant.ru/document/cons_doc_LAW_19671/bbc7b0201b7be7a79e0b44464f1f2fa071d9a774/'
            )
        )
        await cmd_menu(message, state)
# text='<b>Вопросы из обучающей выборки:</b><br>1. На основании чего плательщик страховых взносов исчисляет сумму страховых взносов?<br>2. На какой период осуществляется перерасчет сумм ранее исчисленных налогов?<br>3. Какие сведения должны быть указаны в налоговом уведомлении?<br><br><b>Вопросы из тестовой выборки:</b><br>4. Может ли в налоговом уведомлении указываться информация по нескольким подлежащим уплате налогам?<br>5. Какие виды уведомления может получить налогоплательщик?<br>6. Если налогоплательщик не получает налоговое уведомление по почте, в каком случае оно считается полученным?',

