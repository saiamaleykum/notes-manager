import aiohttp
from aiogram import types, html
from aiogram.fsm.context import FSMContext

import states
from keyboards.default.basic import cancel_keyboard, main_keyboard


async def input_email(msg: types.Message, state: FSMContext):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Выберите действие", reply_markup=main_keyboard)
        await state.set_state(states.user.UserMainMenu.main_menu)
        return 
    await state.update_data(email=answer)
    await msg.answer("Введите пароль", reply_markup=cancel_keyboard)
    await state.set_state(states.user.UserMainMenu.input_pass)


async def input_pass(msg: types.Message, state: FSMContext):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Введите логин", reply_markup=cancel_keyboard)
        await state.set_state(states.user.UserMainMenu.input_email)
        return 
    
    data = await state.get_data()
    email = data['email']
    
    url = 'http://127.0.0.1:8000/auth/login'
    headers = {
        'accept': 'application/ ',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'password', 
        'username': str(email),
        'password': str(answer),
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            status = response.status
            cookies = response.cookies
            session = aiohttp.ClientSession(cookies=cookies)
            await state.update_data(session=session)

    if status == 400:
        m = "Неверный логин или пароль!"
    elif status == 204:
        m = "Вы успешно авторизовались!"
    else:
        m = f"Неизвестная ошибка!\nКод: {status}"

    await msg.answer(m, reply_markup=main_keyboard)
    await state.set_state(states.user.UserMainMenu.main_menu)

    

    


