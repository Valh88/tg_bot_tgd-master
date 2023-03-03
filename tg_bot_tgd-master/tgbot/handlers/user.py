from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message
from ..models.base import session
from ..models.models import User
from ..lexicon.lexicon import COMMANDS_FULL
from ..services.rocket import get_available_currencies,  create_invoice_tg
# from ..config import config


router: Router = Router()


@router.message(CommandStart())
async def start_command(message: Text):
    user = message.from_user
    # print(message.json(exclude_none=True, indent=4))
    b = await create_invoice_tg(
        amount=32,
        currency='TONCOIN',
    )
    print(b)
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
    await message.answer(COMMANDS_FULL[message.text])


# @router.message('/bay')
# async def bay_premium(message: Text):
#     pass