import vnquant.DataLoader as dl
import pandas as pd
import datetime
import csv  
import gspread
import os.path, os
from shutil import copyfile

def init_csv_file(file_name):
    f = open(file_name, 'w')
    writer = csv.writer(f)
    writer.writerow(['Date','Open','High','Low','Close','Adj Close','Volume'])
    f.close()

gc = gspread.service_account(filename='xxxxxxxxxxx')
sh = gc.open_by_key('xxxxxxxxxx')
worksheet = sh.get_worksheet(0)
tickers = worksheet.col_values(1)
try:
    for i in range(0, len(tickers)):
        symbol = tickers[i]
        start_date = '2000-01-01'
        now = datetime.datetime.now()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        csv_file_name = r'../data/%s.txt' % symbol
        csv_file_name_backup = r'../data/{}-{}.txt'.format(symbol, today)
        
        if os.path.isfile(csv_file_name):
            start_date = today
            if os.path.isfile(csv_file_name_backup):
                copyfile(csv_file_name_backup, csv_file_name)
            else:
                copyfile(csv_file_name, csv_file_name_backup)
        end_date = today
        

        loader = dl.DataLoader(symbol, start_date, end_date, data_source='VND', minimal=True)
        data = loader.download()
        df = pd.DataFrame(data, columns=[('open', symbol),
                                        ('high', symbol),
                                        ('low', symbol),
                                        ('close', symbol),
                                        ('avg', symbol),
                                        ('volume', symbol)
                                        ])
       
        if os.path.isfile(csv_file_name):
            df.to_csv (csv_file_name, index = True, header=False, mode='a')
        else: 
            init_csv_file(csv_file_name)
            df.to_csv (csv_file_name, index = True, header=False, mode='a')

except:
  print("An exception occurred")


