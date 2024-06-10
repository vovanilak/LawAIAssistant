from aiogram.fsm.state import State, StatesGroup
class Registration(StatesGroup):
    email = State()
    password = State()
    send = State()
    code = State()
    finish = State()
    
class Account(StatesGroup):
    welcome = State()

    add_money = State()
    summ = State()
    method = State()
    card = State()
    sbp = State()

    balance_info = State()


class App(StatesGroup):
    welcome = State()

    search = State()
    deal = State()
    semantic = State()
    
    
    analysis = State()
    links = State()
    practice = State()
    situation = State()

    calculator = State()
    nalog = State()


    forecast = State()
    risk = State()
    sud = State()

class Favourites(StatesGroup):
    welcome = State()
    search = State()
    analysis = State()
    calculator = State()
    forecast = State()
    
class Settings(StatesGroup):
    welcome = State()
    password = State()
    old = State()
    new = State()

    notifications = State()
    choose = State()
    change = State()

class Gip(StatesGroup):
    welcome = State()
    answer = State()
    another = State()