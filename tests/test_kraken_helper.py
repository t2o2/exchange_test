from unittest import TestCase
from unittest.mock import MagicMock, patch
from exchange_kraken import order_feeder, KrakenExchange


class KrakenHelperTest(TestCase):
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

    @patch('requests.post')
    def test_query_trade_when_query_should_pass_credentials_correctly(self, mock_post: MagicMock):
        # Arrange
        mock_response = MagicMock()
        result_target = {'abc': {'x': 1}}
        mock_response.json.return_value = {'error': [], 'result': result_target}
        mock_post.return_value = mock_response
        key = 'mock_key'
        secret = 'mock_secret=='
        order_id = 'mock_id'
        ex = KrakenExchange(key=key, secret=secret)

        # Act
        _ = ex.query_order_id(order_id)

        # Assert
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.kwargs['headers']['API-Key'], key, 'API key should be passed correctly')
        self.assertEqual(mock_post.call_args.kwargs['data']['txid'], order_id, 'Order ID should be passed correctly')