
import backtrader as bt
from backtrader import indicators as btind
from bots.TelegramBot import TelegramBot
from datetime import datetime

class SMA(bt.Strategy):
    params = (('sma_period', 20), ('ticker', 'HPG'))

    def __init__(self):
        print("sma")
        self.sma = btind.SimpleMovingAverage(self.params.sma_period)

    def next(self):
        self.step_date = self.data.datetime.date().strftime("%Y-%m-%d")
        self.today = datetime.now().strftime("%Y-%m-%d")
        print(self.step_date)
        if self.sma > self.data.close and self.step_date == self.today:
            TelegramBot.send("{} - SMA({}) has cross over the price. ".format(self.params.ticker, self.params.sma_period))

        elif self.sma < self.data.close and self.step_date == self.today:
            TelegramBot.send("{} -  The price has cross over SMA({}). ".format(self.params.ticker, self.params.sma_period))