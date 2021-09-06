import os, sys, argparse
from backtrader import strategy
import pandas as pd
import backtrader as bt
from strategies.GoldenCross import GoldenCross
from strategies.Volume import Volume
from strategies.SMA import SMA
import gspread
import os.path

gc = gspread.service_account(filename='crawl/xxxxxxxxx')
sh = gc.open_by_key('xxxxxxxxxxx')
worksheet = sh.get_worksheet(0)
tickers = worksheet.col_values(1)

strategies = {
    "golden_cross": GoldenCross,
    "volume": Volume,
    "sma": SMA
}

parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="which strategy to run", type=str)
args = parser.parse_args()

if not args.strategy in strategies:
    print("invalid strategy, must be one of {}".format(strategies.keys()))
    sys.exit()
for i in range(0, len(tickers)):
    cerebro = bt.Cerebro()
    symbol = tickers[i]
    data = pd.read_csv('data/%s.txt' % symbol, index_col='Date', parse_dates=True)

    feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(feed)
        
    if args.strategy == 'golden_cross':
        cerebro.addstrategy(strategies[args.strategy], ticker = symbol, fast = 10, slow = 30)
    elif args.strategy == 'sma':
        cerebro.addstrategy(strategies[args.strategy], ticker = symbol, sma_period = 20)
    else:        
        cerebro.addstrategy(strategies[args.strategy], ticker = symbol, avg_volume_period = 10)
    
    cerebro.run()
    print("Finished to running strategy {} with ticket {}".format(args.strategy, symbol))