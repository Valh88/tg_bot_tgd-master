from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class BayFormFSM(StatesGroup):
    currency = State()
