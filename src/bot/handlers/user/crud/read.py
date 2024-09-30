import aiohttp
from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime

from keyboards.default import basic
import states


async def read_menu(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Выберите действие", reply_markup=basic.note_keyboard)
        await state.set_state(states.user.UserMainMenu.note_menu)
    elif answer == "Найти по ID":
        await msg.answer("Введите ID", reply_markup=basic.cancel_keyboard)
        await state.set_state(states.user.NoteMenu.input_id)
    elif answer == "Найти по тегу":
        pass
    elif answer == "Посмотреть все":
        pass
    else:
        await msg.answer(text="Я не знаю такое!")
    

async def input_id(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Выберите действие", reply_markup=basic.read_keyboard)
        await state.set_state(states.user.NoteMenu.read_menu)
        return
    
    data = await state.get_data()
    try:
        session = data['session']
    except KeyError:
        await msg.answer("Вы не авторизованы!", reply_markup=basic.main_keyboard)
        await state.set_state(states.user.UserMainMenu.main_menu)
        return
    
    if answer.isdigit():
        url = f'http://127.0.0.1:8000/note/{answer}'
        headers = {
            'accept': 'application/json',
        }
        async with session.get(url, headers=headers) as response:
            status = response.status
            response_data: dict = await response.json()

        if status == 200:
            tags = response_data['tags']
            tags = [tag['name'] for tag in tags]
            created_at = datetime.strptime(response_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            updated_at = datetime.strptime(response_data['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            m = [
                f"<b>Название:</b> {response_data['title']}\n"
                f"<b>Описание:</b> {response_data['content']}\n"
                f"<b>Создана:</b> {created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"<b>Обновлена:</b> {updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"<b>Теги:</b> {', '.join(tags)}"
            ]
            m = "\n".join(m)
        elif status == 401:
            m = "Вы не авторизованы!"
            del data['session']
        elif status == 403:
            m = "Это не ваша заметка!"
        elif status == 404:
            m = "Такой заметки не существует!"
        else:
            m = f"Неизвестная ошибка!\nКод: {status}"
        await msg.answer(m, reply_markup=basic.read_keyboard)
        await state.set_state(states.user.NoteMenu.read_menu)
    else:
        await msg.answer("Введите целое число!", reply_markup=basic.cancel_keyboard)










async def input_tag(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Введите описание заметки", reply_markup=basic.cancel_keyboard)
        await state.set_state(states.user.UserMainMenu.note_menu)
        return
    
    data = await state.get_data()
    try:
        cookies = data['cookies']
    except KeyError:
        await msg.answer("Вы не авторизованы!", reply_markup=basic.main_keyboard)
        await state.set_state(states.user.UserMainMenu.main_menu)
        return
    
    title = data['title']
    content = data['content']
    content = data['content']
    tags = answer.split(',')
    tags = [tag.strip() for tag in tags]

    url = 'http://127.0.0.1:8000/note'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        'title': title,
        'content': content,
        'tags': tags,
    }

    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.post(url, headers=headers, json=data) as response:
            status = response.status
            cookies = response.cookies
            await state.update_data(cookies=cookies)

    if status == 200:
        m = [
            "Заметка создана!\n\n"
            f"<b>Название:</b> {title}\n"
            f"<b>Описание:</b> {content}\n"
            f"<b>Теги:</b> {', '.join(tags)}"
        ]
        await msg.answer("\n".join(m), reply_markup=basic.note_keyboard)
    elif status == 401:
        await msg.answer("Вы не авторизованы!", reply_markup=basic.main_keyboard)
        await state.set_state(states.user.UserMainMenu.main_menu)
    else:
        await msg.answer(f"Неизвестная ошибка\nКод: {status}")

    await state.set_state(states.user.UserMainMenu.note_menu)
    


