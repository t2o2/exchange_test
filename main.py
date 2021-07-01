from kraken_helper import KrakenExchange
from interfaces.i_exchange import IExchange
from logger import setup_custom_logger
from typing import List, Dict, Tuple
import pandas as pd
import json


logger = setup_custom_logger()


def load_credentials() -> (str, str):
    with open('credential_own.json', 'r') as f:
        credential = json.load(f)

    api_key = credential['key']
    api_sec = credential['secret']
    return api_key, api_sec


def calculate_exposure(fname: str) -> Dict[str, float]:
    exposure = {}
    df = pd.read_csv(fname)
    df.sort_values('time', inplace=True)
    for i, trade in df.iterrows():
        logger.debug(trade.to_dict())
        trade_way = 1 if trade.type == 'buy' else -1
        quote_instrument = trade.pair[:4]
        base_instrument = trade.pair[-4:]
        exposure[quote_instrument] = exposure.get(quote_instrument, 0) + trade.cost * trade_way / trade.price
        exposure[base_instrument] = exposure.get(base_instrument, 0) + trade.cost * trade_way * -1 - trade.fee
        logger.debug(f'Quote {quote_instrument}: {exposure[quote_instrument]:.4f}, Base {base_instrument}: {exposure[base_instrument]:.4f}')
    logger.info(exposure)
    return exposure


def validate_orders(ex: KrakenExchange, fname: str):
    order_df = pd.read_csv(fname)
    trade_info = clean_order_info(ex, order_df)
    export_trade_info(order_df, trade_info)


def format_to_output(order: Dict) -> Dict:
    return {
        'ordertxid': order['txid'],
        'pair': order['descr']['pair'],
        'time': order['closetm'],
        'type': order['descr']['type'],
        'ordertype': order['descr']['ordertype'],
        'price': float(order['price']),
        'cost': float(order['cost']),
        'fee': float(order['fee']),
        'vol': float(order['vol_exec']),
        'margin': 0,
        'misc': order['misc']
    }


def export_trade_info(order_df: pd.DataFrame, trade_info: dict):
    exported_orders = set()
    cleaned_orders = []
    for _, order in order_df.iterrows():
        if order.ordertxid in exported_orders:
            continue
        formatted_trade = format_to_output(trade_info[order.ordertxid])
        cleaned_orders.append(formatted_trade)
        exported_orders.add(order.ordertxid)
    pd.DataFrame(cleaned_orders).sort_values('time', ascending=False).to_csv('reconciled_trades.csv')


def clean_order_info(ex: IExchange, order_df: pd.DataFrame) -> dict:
    trade_info = {}
    for i, order in order_df.iterrows():
        if order.ordertxid in trade_info:
            continue
        logger.info(f'Trade Id: {order.ordertxid}')
        rsp = ex.query_order_id(order.ordertxid)
        trade_info[order.ordertxid] = {'txid': order.ordertxid, **(rsp['result'][order.ordertxid])}
        logger.info(rsp)
    return trade_info


def main():
    exposure_dict = calculate_exposure('data/kraken_tradefile.csv')
    pd.DataFrame([exposure_dict]).to_csv('exposure.csv', index=False)

    api_key, api_sec = load_credentials()
    ex = KrakenExchange(key=api_key, secret=api_sec)
    validate_orders(ex, 'data/kraken_tradefile1.csv')


if __name__ == '__main__':
    main()