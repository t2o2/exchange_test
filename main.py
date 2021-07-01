from actions.exposure import calculate_exposure
from actions.reconcile import validate_orders
from exceptions import UserInputError
from kraken_helper import KrakenExchange
from logger import setup_custom_logger
from pathlib import Path
import argparse
import pandas as pd
import json


logger = setup_custom_logger()


def load_credentials() -> (str, str):
    with open('credential_own.json', 'r') as f:
        credential = json.load(f)

    api_key = credential['key']
    api_sec = credential['secret']
    return api_key, api_sec


def action_calc_exposure(fpath: Path):
    exposure_dict = calculate_exposure(fpath)
    pd.DataFrame([exposure_dict]).to_csv('exposure.csv', index=False)


def action_reconcile(fpath: Path):
    api_key, api_sec = load_credentials()
    ex = KrakenExchange(key=api_key, secret=api_sec)
    validate_orders(ex, fpath)


def perform_action(action_name: str, fpath: Path):
    action_map = {
        'calculateExposure': action_calc_exposure,
        'reconcile': action_reconcile
    }
    action = action_map.get(action_name, None)
    if action is not None:
        action(fpath)
    else:
        raise UserInputError(f'Unknown user action: {action_name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post-trade order information tool')
    parser.add_argument('action', type=str, help='Action to take [calculateExposure|reconcile]')
    parser.add_argument('--t', dest='fpath', type=Path, default='data/kraken_tradefile1.csv', help='Path for input order file')
    args = parser.parse_args()
    perform_action(args.action, args.fpath)
