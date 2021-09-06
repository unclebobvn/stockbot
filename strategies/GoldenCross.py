import math
import backtrader as bt
from bots.TelegramBot import TelegramBot
from datetime import datetime

class GoldenCross(bt.Strategy):
    params = (('fast', 10), ('slow', 30), ('order_percentage', 0.95), ('ticker', 'fpt'), ('avg_volume_period', 10))
   

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period = self.params.fast, plotname = '10 days moving average'
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period = self.params.slow, plotname = '30 days moving average'
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)
    
    def next(self):
        self.step_date = self.data.datetime.date().strftime("%Y-%m-%d")
        self.today = datetime.now().strftime("%Y-%m-%d")
        if self.crossover > 0:
            if self.step_date == self.today:
                TelegramBot.send("{} - SMA({}) has cross over SMA({}) ".format(self.params.ticker, self.params.fast, self.params.slow))

        if self.crossover < 0:
            if self.step_date == self.today:
                TelegramBot.send("{} - SMA({}) has cross over SMA({}) ".format(self.params.ticker, self.params.slow, self.params.fast))