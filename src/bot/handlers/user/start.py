from aiogram import html, types
from aiogram.fsm.context import FSMContext

import states
from keyboards.default.basic import main_keyboard


async def start(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    if msg.from_user is None:
        return
    m = [
        f'Hello, <a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'
    ]
    await msg.answer("\n".join(m), reply_markup=main_keyboard)
    await state.set_state(states.user.UserMainMenu.main_menu)


