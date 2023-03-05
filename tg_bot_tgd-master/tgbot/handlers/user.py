from typing import Dict

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import default_state
from ..models.base import session
from ..models.models import User
from ..lexicon.lexicon import COMMANDS_FULL, BUTTON, CURRENCIES
from ..keyboards.inline import create_inline_kb, button_bay
from ..filters.currencies import IsCurrency
from ..services.rocket import get_available_currencies,  create_invoice_tg, get_all_currencies
from ..misc.states import BayFormFSM
from ..config import config
from ..setting import CURRENCIES as CURRENCY

router: Router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    user = message.from_user
    # print(message.json(exclude_none=True, indent=4))
    try:
        user = session.query(User).filter(User.telega_id == user.id).first()
    except Exception as e:
        user = User(
            telega_id=user.id,
            username=user.username,
            first_name=user.first_name,
            language_code=user.language_code
        )
        session.add(user), session.commit()
    keyword = create_inline_kb(2, **BUTTON,)
    await message.answer(text='3123',
                         reply_markup=keyword)


@router.message(Command(commands=['bay']))
async def bay_premium(message: Message):
    keyboard = create_inline_kb(1, premium=COMMANDS_FULL['/bay'])
    await message.answer(
        text=COMMANDS_FULL['/bay'],
        reply_markup=keyboard
    )


@router.callback_query(Text(text=['prem']),  StateFilter(default_state))
async def process_button_2_press(callback: CallbackQuery, state: FSMContext):
    keyword = create_inline_kb(2, **CURRENCIES, back='назад',)
    await callback.message.edit_text(
        text='Выбрать доступную валюту для обмена',
        reply_markup=keyword
    )
    await state.set_state(BayFormFSM.currency)

    await callback.answer()


@router.callback_query(Text(text='back'))
async def get_currency(callback: CallbackQuery, state: FSMContext):
    keyword = create_inline_kb(2, **BUTTON,)
    await state.clear()
    await callback.message.edit_text(
        text=f'Главная страничка',
        reply_markup=keyword
    )


@router.callback_query(Text(text=CURRENCY), StateFilter(BayFormFSM.currency))
async def get_currency(callback: CallbackQuery, state: FSMContext):
    await state.update_data(currency=callback.data)
    currency: Dict[str, str] = await state.get_data()
    # res = await create_invoice_tg(
    #     amount=200,
    #     currency=currency['currency'],
    #     description='это тестовая оплата',
    # )
    await state.clear()
    #"https://t.me/ton_rocket_test_bot?start=inv_qFsTCmNvHNnbCsi"res['data']['link']
    keyboard = button_bay(url="https://t.me/ton_rocket_test_bot?start=inv_qFsTCmNvHNnbCsi")
    await callback.message.edit_text(
        text=f'Выбрали{callback.data}.Получаете Премиум',
        reply_markup=keyboard
    )
