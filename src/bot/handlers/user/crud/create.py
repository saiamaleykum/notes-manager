import aiohttp
from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.default.basic import main_keyboard, note_keyboard, cancel_keyboard
import states


async def input_title(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Выберите действие", reply_markup=note_keyboard)
        await state.set_state(states.user.UserMainMenu.note_menu)
        return
    
    await state.update_data(title=answer)
    await msg.answer("Введите описание заметки", reply_markup=cancel_keyboard)
    await state.set_state(states.user.NoteMenu.input_content)
    
    
async def input_content(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Введите название заметки", reply_markup=cancel_keyboard)
        await state.set_state(states.user.UserMainMenu.note_menu)
        return
    
    await state.update_data(content=answer)
    await msg.answer("Введите теги заметки (через запятую)", reply_markup=cancel_keyboard)
    await state.set_state(states.user.NoteMenu.input_tags)
    

async def input_tags(
    msg: types.Message, 
    state: FSMContext
):
    answer = msg.text
    if answer == "Назад":
        await msg.answer("Введите описание заметки", reply_markup=cancel_keyboard)
        await state.set_state(states.user.UserMainMenu.note_menu)
        return
    
    data = await state.get_data()
    try:
        cookies = data['cookies']
    except KeyError:
        await msg.answer("Вы не авторизованы!", reply_markup=main_keyboard)
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
            print("Response status:", response.status)
            print("Response headers:", response.headers)
            
            cookies = response.cookies
            if not cookies:
                print("Куки не установлены сервером.")
            else:
                for key, cookie in cookies.items():
                    print(f"{key}: {cookie.value}")

            status = response.status
            cookies = response.cookies
            print(f"create cookie: {cookies}")
            await state.update_data(cookies=cookies)

    if status == 200:
        m = [
            "Заметка создана!\n\n"
            f"<b>Название:</b> {title}\n"
            f"<b>Описание:</b> {content}\n"
            f"<b>Теги:</b> {', '.join(tags)}"
        ]
        await msg.answer("\n".join(m), reply_markup=note_keyboard)
    elif status == 401:
        await msg.answer("Вы не авторизованы!", reply_markup=main_keyboard)
        await state.set_state(states.user.UserMainMenu.main_menu)
        # del data['session']
    else:
        await msg.answer(f"Неизвестная ошибка!\nКод: {status}")

    await state.set_state(states.user.UserMainMenu.note_menu)
    


