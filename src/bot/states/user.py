from aiogram.fsm.state import State, StatesGroup


class UserMainMenu(StatesGroup):
    auth = State()
    input_email = State()
    input_pass = State()
    login = State()

    main_menu = State()
    note_menu = State()


class NoteMenu(StatesGroup):
    # CREATE
    input_title = State()
    input_content = State()
    input_tags = State()

    # READ
    read_menu = State()
    input_id = State()
    input_tag = State()