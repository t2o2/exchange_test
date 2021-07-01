import unittest
from kraken_helper import order_feeder


class KrakenHelperTest(unittest.TestCase):
    def test_order_feeder_when_order_feeder_has_21_orders_should_split_orders(self):
        # Arrange
        orders = [x for x in range(21)]
        target = order_feeder(orders)

        # Act
        group_one = next(target)
        group_two = next(target)

        # Assert
        self.assertEqual(len(group_one), 20, 'First group should have 20 elements')
        self.assertEqual(len(group_two), 1, 'Second group should have 1 element')
