import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(curr_in: str, curr_out: str, amount: str):
        if curr_in == curr_out:
            raise APIException('Нельзя конвертировать одинаковые валюты!')

        try:
            curr_in_ticker = keys[curr_in]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {curr_in}')

        try:
            curr_out_ticker = keys[curr_out]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {curr_out}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать сумму для конвертации {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={curr_in_ticker}&tsyms={curr_out_ticker}')
        curr_new = (json.loads(r.content)[keys[curr_out]] * amount)

        return curr_new
