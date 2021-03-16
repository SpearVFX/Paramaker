import cryptowatch as cw
from termcolor import colored
from datetime import datetime
import colorama
colorama.init()

# Simple candle used for easier code readability
class Candle:
    def __init__(self, timestamp, opened, high, low, closed, volume, volume_quote):
        self.timestamp = timestamp
        self.opened = opened
        self.high = high
        self.low = low
        self.closed = closed
        self.volume = volume
        self.volume_quote = volume_quote
    # Currently I'm using this only for convinience - in later stages this should be the __str__ represantion
    def __repr__(self):
        if self.opened > self.closed:
            color = 'red'
        else:
            color = 'green'
        return colored('O: {}; H: {}; L: {} C: {}'.format(self.opened,
                                                          self.high,
                                                          self.low,
                                                          self.closed), color)

   # def __iter__


# This is pretty much a wrapper for an array of Candles with extra functionalities, but mainly for better readability
class CandleChart:
    def __init__(self, exchange, pair, period):
        self.data = []
        # This current implementation is for the cryptowatch sdk
        # If you want to use another API you should implement your own
        # init method and replace with this one
        self.init_cryptowatch(exchange, pair, period)
        self.exchange = exchange
        self.pair = pair
        self.period = period


    def closed_values(self):
        return [value.closed for element in self.data]

    def __setitem__(self, key):
        # We don't want setting custom candles, tis market manipulation
        pass

    def __getitem__(self, key):
        return self.data[key]


    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    """-------------------------------These are specific for Cryptowatch API-----------------------------------"""
        # Each candle is a list of [close_timestamp, opened, high, low, closed, volume, volume_quote]
    def init_cryptowatch(self, exchange, pair, period):

        #ohlc stands for opened,high,low,closed;
        ohlc_data = self.get_candles_cryptowatch(exchange, pair, period)
        for ohlc in ohlc_data:
            self.data.append(Candle(ohlc[0],
                                    ohlc[1],
                                    ohlc[2],
                                    ohlc[3],
                                    ohlc[4],
                                    ohlc[5],
                                    ohlc[6],
                                   ))

    def get_candles_cryptowatch(self, exchange, pair, period):
        with open("credentials.txt", 'r') as f:
            cw.api_key = f.readline()
        ticker = "{}:{}".format(exchange, pair).upper()
        try:
            candles = cw.markets.get(ticker, ohlc=True, periods=[period])
        except:
            print(ticker)
            print("""An Error occurred trying to get the candle data for \n
                    {} {} {}""".format(str(exchange), str(ticker), str(period)))
        if period == "1m":
            return candles.of_1m
        if period == "3m":
            return candles.of_3m
        if period == "5m":
            return candles.of_5m
        if period == "15m":
            return candles.of_15m
        if period == "30m":
            return candles.of_30m
        if period == "1h":
            return candles.of_1h
        if period == "2h":
            return candles.of_2h
        if period == "4h":
            return candles.of_4h
        if period == "6h":
            return candles.of_6h
        if period == "12h":
            return candles.of_12h
        if period == "1d":
            return candles.of_1d
        if period == "3d":
            return candles.of_3d
        if period == "1w":
            return candles.of_1w
        if period == "1w_monday":
            return candles.of_1w_monday
    """-------------------------------------------------------------------------------------------------------"""
