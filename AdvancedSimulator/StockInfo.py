from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import os
import json

class StockInfo:
    def __init__(self, ticker, buy_date, initial_investment):
        self.ticker = ticker
        self.stock_data_file = f'AdvancedSimulator/IntermediateData/{self.ticker}.json'
        print(self.stock_data_file)

        self.ts = TimeSeries(key='INSERT_HERE', output_format='pandas') # TODO: Add key config
        self.data_downloaded = False
        self.download_data()

        self.initial_value = initial_investment
        self.holdings_value = initial_investment
        self.buy_price = self.get_opening_price(buy_date)
        self.last_day_price = self.buy_price

    def get_return(self):
        rtn = self.last_day_price / self.buy_price - 1 # This is the return rate
        return rtn
        
    def update_holdings_value(self, new_value):
        self.holdings_value = new_value
        
    def update_last_price(self, new_last_price):
        self.last_day_price = new_last_price
    
    def download_data(self, force=False):
        if force or not os.path.isfile(self.stock_data_file):
            raw_data = self.ts.get_daily_adjusted(symbol=self.ticker, outputsize='full')[0]
            print(type(raw_data))
            raw_data.to_json(path_or_buf=self.stock_data_file, orient='index')

        self.data_downloaded = True

    def get_data(self):
        if self.data_downloaded:
            data = pd.read_json(path_or_buf=self.stock_data_file, orient='index', typ='frame')
            return data

        else:
            raise "The file doesn't exists so download failed somehow"
    
    # Get closing price if possible
    def get_opening_price(self, date):
        return self.get_price(date, '1. open')

    # Get closing price if possible
    def get_closing_price(self, date):
        return self.get_price(date, '5. adjusted close')

    # Get closing price if possible
    def get_high_price(self, date):
        return self.get_price(date, '2. high')

    # Get closing price if possible
    def get_low_price(self, date):
        return self.get_price(date, '3. low')

    def get_price(self, date, key):
        date_string = date.strftime('%Y-%m-%d')
        data = self.get_data()
        adjusted_close = data[key]
        data_point = adjusted_close.get(date_string)

        if len(data_point) == 0:
            return None

        closing_price = float(data_point[[0]])
        return closing_price


def main():
    msft = StockInfo('MSFT')
    print(msft.get_closing_price(dt.datetime.strptime('2-12-2020', '%m-%d-%Y')))

if __name__ == '__main__':
    main()