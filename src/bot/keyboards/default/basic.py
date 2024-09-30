from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


auth_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Авторизация')]],
    resize_keyboard=True
)

note_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Создать'), KeyboardButton(text='Посмотреть')],
              [KeyboardButton(text='Удалить'), KeyboardButton(text='Обновить')],
              [KeyboardButton(text='Назад')]],
    resize_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Выйти'), KeyboardButton(text='Войти')],
              [KeyboardButton(text='Заметки')]],
    resize_keyboard=True
)

login_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Войти'), KeyboardButton(text='Назад')]],
    resize_keyboard=True
)

read_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Найти по ID'), KeyboardButton(text='Найти по тегу')],
              [KeyboardButton(text='Назад'), KeyboardButton(text='Посмотреть все')]],
    resize_keyboard=True
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Назад')]],
    resize_keyboard=True
)