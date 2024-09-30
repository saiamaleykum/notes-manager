from aiogram import types
from aiogram.fsm.context import FSMContext

import states
from keyboards.default.basic import cancel_keyboard, note_keyboard


async def main_menu(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Войти":
        await msg.answer("Введите логин", reply_markup=cancel_keyboard)
        await state.set_state(states.user.UserMainMenu.input_email)
    elif answer == "Заметки":
        await msg.answer("Выберите действие", reply_markup=note_keyboard)
        await state.set_state(states.user.UserMainMenu.note_menu)
    elif answer == "Выйти":
        pass
    else:
        await msg.answer(text="Я не знаю такое!")


