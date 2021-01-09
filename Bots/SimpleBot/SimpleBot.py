from ..Bot import Bot

class SimpleBot(Bot):
    def __init__(self):
        self.setup = None
        self.single_run_done = False
    
    def get_orders(self, date, limit):
        if not self.single_run_done:
            # We don't care about date for our simple bot so ignore
            stocks = ['MSFT', 'NEX', 'FB', 'TSLA', 'AAPL']
            if limit < len(stocks):
                stocks = stocks[0:limit]

            self.single_run_done = True
            return stocks
        
        return []