from datetime import timedelta, datetime
from typing import Dict
from contextlib import suppress

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import default_state
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import exists

from ..models.base import session
from ..models.models import User, InvoiceUser
from ..lexicon.lexicon import COMMANDS_FULL, BUTTON, CURRENCIES
from ..keyboards.inline import create_inline_kb, button_bay
from ..filters.currencies import IsCurrency
from ..services.rocket import get_available_currencies,  create_invoice_tg, delete_invoice_tg, get_invoice_by_id
from ..misc.states import BayFormFSM
from ..config import config
from ..setting import CURRENCIES as CURRENCY
from ..middlewares.config_middleware import CounterMiddleware

router: Router = Router()
router.callback_query.middleware(CounterMiddleware())


@router.message(CommandStart())
async def start_command(message: Message):
    user = message.from_user
    # print(message.json(exclude_none=True, indent=4))
    # try:
    #     user = session.query(User).filter(User.telega_id == user.id).first()
    #     print(user)
    # except Exception as e:
    #     print('123')
    #     user = User(
    #         telega_id=user.id,
    #         username=user.username,
    #         first_name=user.first_name,
    #         language_code=user.language_code
    #     )
    #     print(user.id)
    #     session.add(user), session.commit()
    current_user = session.query(User).filter(User.telega_id == user.id).first()
    if current_user is None:
        new_user = User(
            telega_id=user.id,
            username=user.username,
            first_name=user.first_name,
            language_code=user.language_code
        )
        session.add(new_user), session.commit()
    keyword = create_inline_kb(2, **BUTTON,)
    await message.answer(text='3123',
                         reply_markup=keyword)


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
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text=f'Главная страничка',
            reply_markup=keyword
        )


@router.callback_query(Text(text=CURRENCY), StateFilter(BayFormFSM.currency))
async def get_currency(callback: CallbackQuery, state: FSMContext):
    await state.update_data(currency=callback.data)
    currency: Dict[str, str] = await state.get_data()
    await state.clear()
    current_user = session.query(User)\
        .filter(User.telega_id == callback.from_user.id)\
        .first()

    invoice = session.query(InvoiceUser).\
        filter(InvoiceUser.user == current_user,
               InvoiceUser.delete == False,
               InvoiceUser.paid == False,
               InvoiceUser.currency == callback.data).\
        first()
    try:
        id_invoice = invoice.rocket_id
        invoice_data = await get_invoice_by_id(id_invoice=id_invoice)
        if invoice_data['data']['status'] == 'paid':
            invoice.paid = True
            session.add(invoice), session.commit()
            await delete_invoice_tg(id_invoice=id_invoice)
            raise ValueError()
        elif invoice_data['data']['status'] == 'active':
            keyboard = button_bay(url=invoice.url)
            await callback.message.edit_text(
                text=f'Выбрали{callback.data}.Получаете Премиум',
                reply_markup=keyboard
            )
        elif invoice_data['data']['status'] == 'expired':
            invoice.delete = True
            session.add(invoice), session.commit()
            await delete_invoice_tg(id_invoice=id_invoice)

            res = await create_invoice_tg(
                amount=0.3,
                currency=currency['currency'],
                description='это тестовая оплата',
            )
            invoice = InvoiceUser(
                rocket_id=res['data']['id'],
                expired_in=res['data']['expiredIn'],
                url=res['data']['link'],
                user=current_user,
                currency=callback.data,
                valid_until=datetime.now() + timedelta(seconds=res['data']['expiredIn']),
            )
            session.add(invoice), session.commit()
            keyboard = button_bay(url=invoice.url)
            await callback.message.edit_text(
                text=f'Выбрали{callback.data}.Получаете Премиум',
                reply_markup=keyboard
            )
            await callback.answer()

    except Exception:
        res = await create_invoice_tg(
            amount=0.3,
            currency=currency['currency'],
            description='это тестовая оплата',
        )
        invoice = InvoiceUser(
            rocket_id=res['data']['id'],
            expired_in=res['data']['expiredIn'],
            url=res['data']['link'],
            user=current_user,
            currency=callback.data,
            valid_until=datetime.now() + timedelta(seconds=res['data']['expiredIn']),
        )
        session.add(invoice), session.commit()

        keyboard = button_bay(url=invoice.url)
        await callback.message.edit_text(
            text=f'Выбрали{callback.data}.Получаете Премиум',
            reply_markup=keyboard
        )
        await callback.answer()
