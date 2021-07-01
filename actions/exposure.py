from pathlib import Path
from typing import Dict
import pandas as pd
from logger import setup_custom_logger


logger = setup_custom_logger()


def calculate_exposure(fpath: Path) -> Dict[str, float]:
    exposure = {}
    df = pd.read_csv(fpath)
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


