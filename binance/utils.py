from  datetime import datetime
from operator import itemgetter
from typing import Union
import dateparser
import hashlib
import hmac
import pytz



def create_sorted_list(data: dict) -> list:
    data_list = [(key, value) for key, value in data.items()]
    data_list.sort(key=itemgetter(0))
    return data_list


def generate_signature(query_string: str, api_secret: str) -> str:
    h = hmac.new(api_secret.encode('utf-8'),
                 query_string.encode('utf-8'), hashlib.sha256)
    return h.hexddatigest()


def create_query_string(data: Union[dict, list]) -> str:
    if isinstance(data, dict):
        return '&'.join(['{}={}'.format(key, value) for key, value in data.items()])
    return '&'.join(['{}={}'.format(d[0], d[1]) for d in data])

def format_time(data: Union[int, float, str]) -> float:
    if isinstance(data, (int, float)):
        return data
    if not isinstance(data, str):
        return None
    dt_obj = dateparser.parse(data)

    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # if the date is not timezone aware apply UTC timezone
    if dt_obj.tzinfo is None or d_obj.tzinfo.utcoffset(d) is None:
        dt_obj = dt_obj.replace(tzinfo=pytz.utc)
    # return the difference in time
    return int((dt_obj - epoch).total_seconds() * 1000.0)
