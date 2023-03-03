import json

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
        amount: float,
        currency: str,
        description: str = 'n items',
        hidden_message: str = "thank you",
        callback_url: str = None,
        expired_in: int = 3000,
):

    """ Одноразовая платежка """

    # url = 'https://pay.ton-rocket.com/tg-invoices'
    url = 'https://dev-pay.ton-rocket.com/tg-invoices'
    async with aiohttp.ClientSession() as session:
        data = {
            'amount': amount,
            'currency': currency,
            'description': description,
            'hidden_message': hidden_message,
            'callbackUrl': callback_url,
            'expired_in': expired_in,
        }
        res = await session.post(url=url, data=data, headers=headers)
        return await res.json()
