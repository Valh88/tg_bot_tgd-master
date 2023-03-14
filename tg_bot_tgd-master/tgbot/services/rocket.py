from typing import Optional

import aiohttp
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import config

headers = {
   "Accept": "application/json",
   "Rocket-Pay-Key": config.pay_rocket_token
}


async def get_available_currencies():

    """ Доступные валюты """

    url = 'https://pay.ton-rocket.com/currencies/available'
    async with aiohttp.ClientSession() as session:
        res = await session.get(url, headers=headers)
    return await res.json()


async def create_invoice_tg(
        amount: float = 0.4,
        currency: str = 'TONCOIN',
        # min_payment: float = 0,
        description: str = 'описание',
        hidden_message: str = "скрытое сообщение",
        callback_url: str = "https://t.me/ton_rocket",
        payload: str = "здесь то, что я увижу, когда получу чек",
        expired_in: int = 3000,
):

    """ Одноразовая платежка """

    # url = 'https://pay.ton-rocket.com/tg-invoices'
    url = 'https://dev-pay.ton-rocket.com/tg-invoices'
    async with aiohttp.ClientSession() as session:
        data = {
            "amount": amount,
            # "minPayment": 1.23,
            # "numPayments": 1,
            "currency": currency,
            "description": description,
            "hiddenMessage": hidden_message,
            "callbackUrl": callback_url,
            "payload": payload,
            "expiredIn": expired_in
        }
        res = await session.post(url=url, json=data, headers=headers)
        return await res.json()


async def get_all_currencies():
    url = 'https://dev-pay.ton-rocket.com/currencies/available'
    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url, headers=headers)
    return await res.json()


async def delete_invoice_tg(id_invoice: int):
    url = f'https://dev-pay.ton-rocket.com/tg-invoices/{id_invoice}'
    async with aiohttp.ClientSession() as session:
        res = await session.delete(url, headers=headers)
        res = await res.json()
        if res['success']:
            return True


async def get_invoice_by_id(id_invoice: int):
    url = f'https://dev-pay.ton-rocket.com/tg-invoices/{id_invoice}'
    async with aiohttp.ClientSession() as session:
        res = await session.get(url, headers=headers)
        return await res.json()


