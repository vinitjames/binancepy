from operator import itemgetter
from typing import Union
import hashlib
import hmac


def create_sorted_list(data: dict) -> list:
    data_list = [(key, value) for key, value in data.items()]
    data_list.sort(key=itemgetter(0))
    return data_list


def generate_signature(query_string: str, api_secret: str) -> str:
    h = hmac.new(api_secret.encode('utf-8'),
                 query_string.encode('utf-8'), hashlib.sha256)
    return h.hexdigest()


def create_query_string(data: Union[dict, list]) -> str:
    if isinstance(data, dict):
        return '&'.join(['{}={}'.format(key, value) for key, value in data.items()])

    return '&'.join(['{}={}'.format(d[0], d[1]) for d in data])
