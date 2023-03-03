from aiogram import Router
from aiogram.types import Message
# from ..models.base import async_session,
from ..models.base import session
from ..models.models import User
from ..lexicon.lexicon import COMMANDS_FULL
router: Router = Router()

#
# @router.message()
# async def send_echo(message: Message):
#     # print(message.json(exclude_none=True, indent=4))
#     # async with async_session as session:
#     #     result = await session.all(User)
#     # print(result.all())
#
#     # users = session.query(User).all()
#     # print(users)
#
#     await message.answer(f'Это эхо! {message.text}')
