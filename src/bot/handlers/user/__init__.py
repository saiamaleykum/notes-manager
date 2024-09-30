from aiogram import Router
from aiogram.filters import CommandStart, StateFilter

from states import user
from filters import ChatTypeFilter, TextFilter

from . import start, menu, auth, note
from .crud import create, read

def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter(chat_type="private"))

    user_router.message.register(start.start, CommandStart())

    # AUTH
    user_router.message.register(auth.input_email, StateFilter(user.UserMainMenu.input_email))
    user_router.message.register(auth.input_pass, StateFilter(user.UserMainMenu.input_pass))

    # MENUS
    user_router.message.register(menu.main_menu, StateFilter(user.UserMainMenu.main_menu))
    user_router.message.register(note.note_menu, StateFilter(user.UserMainMenu.note_menu))

    # CREATE
    user_router.message.register(create.input_title, StateFilter(user.NoteMenu.input_title))
    user_router.message.register(create.input_content, StateFilter(user.NoteMenu.input_content))
    user_router.message.register(create.input_tags, StateFilter(user.NoteMenu.input_tags))

    # READ
    user_router.message.register(read.read_menu, StateFilter(user.NoteMenu.read_menu))
    user_router.message.register(read.input_id, StateFilter(user.NoteMenu.input_id))
    user_router.message.register(read.input_tag, StateFilter(user.NoteMenu.input_tag))


    return user_router
