import unittest
from binance.utils import *
from binance.api_def import *

class TestUtils(unittest.TestCase):

    def test_create_sorted_list(self):
        test_dict = {'test': 1,'dict': 2, 'binance': 'api'}
        sorted_list = create_sorted_list(test_dict)
        self.assertTrue(isinstance(sorted_list, list))
        self.assertEqual(sorted_list[0], ('binance','api'))
        self.assertEqual(sorted_list[1], ('dict', 2))
        self.assertEqual(sorted_list[2], ('test', 1))

    def test_create_query_string(self):
        test_dict = {'test': 1,'dict': 2, 'binance': 'api'}
        query_string = create_query_string(test_dict)
        self.assertTrue(isinstance(query_string, str))
        self.assertEqual(query_string.split('&')[0], ('test=1'))
        self.assertEqual(query_string.split('&')[1], ('dict=2'))
        self.assertEqual(query_string.split('&')[2], ('binance=api'))
        test_list = [('test',1),('dict', 2),('binance','api')]
        query_string = create_query_string(test_dict)
        self.assertTrue(isinstance(query_string, str))
        self.assertEqual(query_string.split('&')[0], ('test=1'))
        self.assertEqual(query_string.split('&')[1], ('dict=2'))
        self.assertEqual(query_string.split('&')[2], ('binance=api'))
        
        
    def test_interval_to_ms(self):
        kline_interval = KlineInterval
        self.assertEqual(interval_to_ms(kline_interval.ONEMINUTE), 60*1000)
        self.assertEqual(interval_to_ms(kline_interval.THREEMINUTE), 3*60*1000)
        self.assertEqual(interval_to_ms(kline_interval.FIVEMINUTE), 5*60*1000)
        self.assertEqual(interval_to_ms(kline_interval.FIFTEENMINUTE), 15*60*1000)
        self.assertEqual(interval_to_ms(kline_interval.THIRTYMINUTE), 30*60*1000)
        self.assertEqual(interval_to_ms(kline_interval.ONEHOUR), 3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.TWOHOUR), 2*3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.FOURHOUR), 4*3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.SIXHOUR), 6*3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.EIGHTHOUR), 8*3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.TWELVEHOUR), 12*3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.ONEDAY), 24*3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.THREEDAY), 72*3600*1000)
        self.assertEqual(interval_to_ms(kline_interval.ONEWEEK), 7*24*3600*1000)

    def test_format_time(self):
        self.assertEqual(format_time(1614288267), 1614288267)
        self.assertEqual(format_time(1614288267.0), 1614288267.0)
        self.assertEqual(format_time('02/25/2021'), 1614211200000)
        self.assertEqual(format_time('25/2/2021'), 1614211200000)
        self.assertEqual(format_time('25.2.2021'), 1614211200000)
        self.assertEqual(format_time('2/23/2021 18:15:55'), 1614104155000)

if __name__ == '__main__':
    unittest.main()
