from interfaces.i_exchange import IExchange
from kraken_helper import KrakenExchange
from logger import setup_custom_logger
from pathlib import Path
from typing import Dict
import pandas as pd


logger = setup_custom_logger()


def validate_orders(ex: KrakenExchange, fpath: Path):
    order_df = pd.read_csv(fpath)
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
    logger.info('Cleaning order')
    exported_orders = set()
    cleaned_orders = []
    for _, order in order_df.iterrows():
        if order.ordertxid in exported_orders:
            continue
        formatted_trade = format_to_output(trade_info[order.ordertxid])
        cleaned_orders.append(formatted_trade)
        exported_orders.add(order.ordertxid)
    logger.info('Exporting to output file')
    pd.DataFrame(cleaned_orders).sort_values('time', ascending=False).to_csv('reconciled_trades.csv')


def clean_order_info(ex: IExchange, order_df: pd.DataFrame) -> dict:
    unique_list = order_df['ordertxid'].unique().tolist()
    logger.info(f'Retrieving trade Ids: {unique_list}')
    rsp = ex.query_order_id_batch(unique_list)
    trade_info = {}
    for k, v in rsp.items():
        trade_info[k] = {'txid': k, **v}
    return trade_info


