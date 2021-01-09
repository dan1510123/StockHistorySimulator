import os
import pandas as pd

class InvestmentHistory:
    def __init__(self, history_file_name):
        self.history_file_name = history_file_name
        self.clean(force=True) # TODO Change force to True
    
    def get_history(self, date):
        date_string = date.strftime('%m-%d-%Y')
        hist = {}
        if os.path.isfile(self.history_file_name):
            with open(self.history_file_name, "r") as hist_file:
                for line in hist_file:
                    line = line.replace('\n','').split(',')
                    if len(line) > 0: # TODO Specify number
                        hist[line[0]] = [float(line[1])]
                        if line[0] == date_string:
                            break
        else:
            raise BaseException('History file does not exist (but it should...)')
        
        return pd.DataFrame.from_dict(hist, orient='index')

    # Adds a day's data to the history
    # stock_prices => [['MSFT', 224.3], ['AMZN', 1253]]
    def add_day_data(self, date_string, current_value, total_return, today_return, stock_data):
        line = date_string + ',' + str(current_value) + ',' + str(total_return) + ',' + str(today_return)
        for stock in stock_data:
            line += ',' + str(stock[0]) + '|' + str(stock[1]) + '|' + str(stock[2]) + '|' + str(stock[3])
        hist_file = open(self.history_file_name, "a")
        hist_file.write(line + '\n')

    def get_day_data(self, date):
        hist_file = open(self.history_file_name, "r")
        date_string = date.strftime('%m-%d-%Y')
        data = []
        for line in hist_file:
            line = line.replace('\n','').split(',')
            if len(line) > 0 and line[0] == date_string:
                data = line
                break
        hist_file.close()

        return data

    def clean(self, force=False):
        if force:
            hist_file = open(self.history_file_name, "w")
            hist_file.close()

def main():
    file_name = 'AdvancedSimulator/OutputData/history.csv'
    hist = InvestmentHistory(file_name)
    print(hist.get_history())

if __name__ == '__main__':
    main()