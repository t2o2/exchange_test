from abc import ABC


class IExchange(ABC):
    def query_order_id(self, order_id: str):
        pass