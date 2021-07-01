from abc import ABC
from typing import List


class IExchange(ABC):
    def query_order_id(self, order_id: str):
        pass

    def query_order_id_batch(self, order_ids: List[str]):
        pass