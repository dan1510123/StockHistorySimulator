import datetime as dt
from .InvestmentHistory import InvestmentHistory
from .StockInfo import StockInfo
from Bots.Bot import Bot

HISTORY_FILE = 'AdvancedSimulator/OutputData/history.csv'
DAY = dt.timedelta(days=1)
MAX_PORTFOLIO_LIMIT = 10
class AdvancedSimulator:
    def __init__(self, initial_bal, start_date, loss_limit, gain_limit, bot: Bot, exclude=[]):
        # Set start date to be a time instance
        self.start_date = self.get_next_weekday(dt.datetime.strptime(start_date, '%m-%d-%Y') - DAY)
        self.current_date = self.start_date
        self.latest_date = self.current_date
        self.initial_total_bal = initial_bal
        self.last_total_bal = initial_bal
        self.current_remaining_bal = initial_bal
        self.total_return = 0
        self.today_return = 0
        self.stocks = [] # List of StockInfo's
        self.history = InvestmentHistory(HISTORY_FILE)

        self.loss_limit = loss_limit
        self.gain_limit = gain_limit
        self.bot = bot
        self.exclude = exclude

    def get_total_bal(self):
        return self.current_remaining_bal + self.get_portfolio_bal()

    def get_portfolio_bal(self):
        pbal = 0
        for stock in self.stocks:
            pbal += stock.holdings_value
        return pbal

    def run_next_day(self):
        # Increment the date
        self.current_date = self.get_next_weekday(self.current_date)

        # If we have done this already, just grab the existing data.
        if self.current_date <= self.latest_date:
            return self.load_old_day(self.current_date)

        self.latest_date = self.current_date

        if len(self.stocks) < MAX_PORTFOLIO_LIMIT:
            # Run code to get the next day's info
            base_orders = self.bot.get_orders(self.current_date, MAX_PORTFOLIO_LIMIT - len(self.stocks))

            orders = []
            for ticker in base_orders:
                if ticker not in self.exclude:
                    orders.append(ticker)

            # Purchase these stocks
            invest_amount = self.current_remaining_bal / (MAX_PORTFOLIO_LIMIT - len(self.stocks)) # Splits remaining money by remaining buys
            for ticker in orders:
                stock = StockInfo(ticker, self.current_date, invest_amount)
                stock.update_holdings_value(invest_amount)
                self.stocks.append(stock)

            if len(self.stocks) == MAX_PORTFOLIO_LIMIT:
                self.current_remaining_bal = 0
            
            else:
                self.current_remaining_bal -= len(orders) * invest_amount

        stock_data = []
        stocks_to_keep = []
        # Get info for all stocks for the day, updating for the day
        for stock in self.stocks:
            today_closing_price = stock.get_closing_price(self.current_date)
            stock_total_change = today_closing_price / stock.buy_price

            today_high_price = stock.get_high_price(self.current_date)
            today_low_price = stock.get_low_price(self.current_date)
            if today_high_price / stock.buy_price >= 1 + self.gain_limit:
                stock_total_change = 1 + self.gain_limit
            elif today_low_price / stock.buy_price <= 1 - self.loss_limit:
                stock_total_change = today_low_price / stock.buy_price

            store_prev_day = stock.last_day_price
            stock.update_last_price(today_closing_price)
            stock_daily_change = stock.last_day_price / store_prev_day

            stock.update_holdings_value(stock.initial_value * stock_total_change)

            stock_data.append([stock.ticker, today_closing_price, stock_daily_change, stock_total_change])
            
            # If a stock hits its gain limit, then sell it
            if stock_total_change >= 1 + self.gain_limit:
                self.current_remaining_bal += stock.holdings_value
            # Else if a stock hits its loss limit, then sell it
            elif stock_total_change <= 1 - self.loss_limit:
                self.current_remaining_bal += stock.holdings_value
            else:
                stocks_to_keep.append(stock)
        
        self.stocks = stocks_to_keep
        self.total_return = self.get_total_bal() / self.initial_total_bal - 1
        self.today_return = self.get_total_bal() / self.last_total_bal - 1
        self.last_total_bal = self.get_total_bal()

        date_string = self.current_date.strftime('%m-%d-%Y')
        self.history.add_day_data(date_string, self.get_total_bal(), self.total_return, self.today_return, stock_data)
        
        return self.history.get_history(self.current_date)

    def run_previous_day(self):
        self.current_date = self.get_previous_weekday(self.current_date)
        return self.load_old_day(self.current_date)

    def load_old_day(self, date):
        return self.history.get_history(date)

    def get_next_weekday(self, date):
        next_weekday = (date + DAY).weekday()
        if next_weekday == 5: # Sat
            return date + 3 * DAY
        elif next_weekday == 6: # Sun
            return date + 2 * DAY
        else:
            return date + DAY

    def get_previous_weekday(self, date):
        next_weekday = (date - DAY).weekday()
        if next_weekday == 6: # Sun
            return date - 3 * DAY
        elif next_weekday == 5: # Sat
            return date - 2 * DAY
        else:
            return date - DAY


def main():
    sim = AdvancedSimulator(100, '1-5-2020', None)
    print(sim.current_date)

if __name__ == '__main__':
    main()