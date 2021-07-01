import base64
import hashlib
import hmac
import requests
import time
import urllib.parse
from interfaces.i_exchange import IExchange
from ratelimit import limits, sleep_and_retry
from logger import setup_custom_logger


logger = setup_custom_logger()


class KrakenExchange(IExchange):
    # Read Kraken API key and secret stored in environment variables
    api_url = "https://api.kraken.com"
    ONE_MINUTE = 60

    def __init__(self, *, key, secret):
        self.api_key = key
        self.api_sec = secret

    # Attaches auth headers and returns results of a POST request
    @sleep_and_retry
    @limits(calls=20, period=ONE_MINUTE)
    def kraken_request(self, uri_path: str, data: dict, api_key: str, api_sec: str):
        headers = {}
        headers['API-Key'] = api_key
        # get_kraken_signature() as defined in the 'Authentication' section
        headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
        rsp = requests.post((self.api_url + uri_path), headers=headers, data=data)
        return rsp

    def query_order_id(self, trade_id: str):
        # Construct the request and print the result
        rsp = self.kraken_request('/0/private/QueryOrders', {
            "nonce": str(int(1000*time.time())),
            "txid": trade_id
        }, self.api_key, self.api_sec)
        return rsp.json()


def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()



if __name__ == '__main__':
    #print(query_trade_id('OQCLML-BW3P3-BUCMWZ'))
    resp = kraken_request('/0/private/QueryOrders', {
        "nonce": str(int(1000 * time.time())),
        #"txid": "TUKCR7-PUQT3-VIKQUH"
        "txid": "OJXW3S-UOER3-7MAO6W"
    }, api_key, api_sec)

    print(resp.text)

    #resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XETHZEUR')
    #print(resp.json())