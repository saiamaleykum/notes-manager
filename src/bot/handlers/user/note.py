import aiohttp
from aiogram import types, html
from aiogram.fsm.context import FSMContext

from keyboards.default.basic import main_keyboard, cancel_keyboard, read_keyboard
import states


async def note_menu(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Выберите действие", reply_markup=main_keyboard)
        await state.set_state(states.user.UserMainMenu.main_menu)
    elif answer == "Создать":
        await msg.answer("Введите название заметки", reply_markup=cancel_keyboard)
        await state.set_state(states.user.NoteMenu.input_title)
    elif answer == "Посмотреть":
        await msg.answer("Выберите действие", reply_markup=read_keyboard)
        await state.set_state(states.user.NoteMenu.read_menu)
    elif answer == "Удалить":
        await msg.answer("Удалить")
    elif answer == "Обновить":
        await msg.answer("Обновить")
    else:
        await msg.answer(text="Я не знаю такое!")


