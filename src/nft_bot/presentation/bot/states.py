from aiogram.fsm.state import State, StatesGroup


class ProfileStates(StatesGroup):
    main = State()


class PaginationNftStates(StatesGroup):
    main = State()


class AddNftStates(StatesGroup):
    main = State()


class SettingStates(StatesGroup):
    main = State()


class EditNftStates(StatesGroup):
    main = State()
