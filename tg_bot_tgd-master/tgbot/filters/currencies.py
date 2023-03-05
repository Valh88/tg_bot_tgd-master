
from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCurrency(BaseFilter):
    def __init__(self, currencies: list[int]) -> None:
        self.currencies = currencies

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.currencies