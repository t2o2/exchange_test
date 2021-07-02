import base64
import hashlib
import hmac
import requests
import time
import urllib.parse
from exceptions import *
from interfaces.i_exchange import IExchange
from logger import setup_custom_logger
from ratelimit import limits, sleep_and_retry
from typing import List, Dict


logger = setup_custom_logger()


def order_feeder(orders: List, batch_size: int = 20) -> List:
    idx = 0
    while idx < len(orders):
        yield orders[idx:idx+batch_size]
        idx += batch_size


class KrakenExchange(IExchange):
    api_url = "https://api.kraken.com"
    ONE_MINUTE = 60
    RATE_LIMIT = 20

    def __init__(self, *, key, secret):
        self.api_key = key
        self.api_sec = secret

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=ONE_MINUTE)
    def kraken_request(self, uri_path: str, data: dict, api_key: str, api_sec: str):
        headers = {}
        headers['API-Key'] = api_key
        # get_kraken_signature() as defined in the 'Authentication' section
        headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
        rsp = requests.post((self.api_url + uri_path), headers=headers, data=data)
        return rsp

    def _query_private(self, endpoint: str, data: Dict) -> Dict:
        response = self.kraken_request(endpoint, data, self.api_key, self.api_sec)
        rsp = response.json()
        if len(rsp['error']) > 0:
            raise ExchangeResponseError(rsp['error'])
        return rsp['result']

    def query_order_id(self, trade_id: str) -> Dict[str, Dict]:
        return self._query_private('/0/private/QueryOrders', {
            "nonce": str(int(1000 * time.time())),
            "txid": trade_id
        })

    def query_order_id_batch(self, order_ids: List[str]) -> Dict[str, Dict]:
        rslt = {}
        for order_batch in order_feeder(order_ids):
            rsp = self.query_order_id(','.join(order_batch))
            rslt = {**rslt, **rsp}
        return rslt


def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

