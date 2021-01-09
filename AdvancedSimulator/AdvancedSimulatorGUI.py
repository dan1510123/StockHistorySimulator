import tkinter as tk
import numpy as np
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from .AdvancedSimulator import AdvancedSimulator
from .InvestmentHistory import InvestmentHistory
from Bots.Bot import Bot

class AdvancedSimulatorGUI:
    def __init__(self, initial_bal, start_date, loss_limit, gain_limit, bot: Bot, exclude=[]):
        # Create the Simulator Backend
        self.sim = AdvancedSimulator(initial_bal, start_date, loss_limit, gain_limit, bot, exclude=exclude)

        self.window = tk.Tk()
        y_pad = 140
        self._geom = "{0}x{1}+3+3".format(
            self.window.winfo_screenwidth(),
            self.window.winfo_screenheight()-y_pad)
        self.window.geometry(self._geom)
        self.window.resizable(0, 0)
        
        self.title = tk.Label(self.window, text="Advanced Stock Simulator")
        self.title.config(font=("Courier", 32))
        self.title.place(relx=0.5, y=30, anchor=tk.CENTER)

        # Create the UI for the top left corner for start, current date
        sdl_x = 5
        sdl_y = 10
        sdl_w = 75
        self.start_date_label = tk.Label(self.window, text="Start Date:")
        self.start_date_label.config(font=("Roman", 14))
        self.start_date_label.place(x=sdl_x, y=sdl_y, width=sdl_w, anchor=tk.NW)
        sdv_x = sdl_x + sdl_w
        sdv_w = 110
        self.start_date_value = tk.Label(self.window, text=start_date)
        self.start_date_value.config(font=("Courier", 18))
        self.start_date_value.place(x=sdv_x,y=sdl_y, width=sdv_w, anchor=tk.NW)
        x_buffer = 15
        cdl_x = sdv_x+sdv_w+x_buffer
        cdl_w = 90
        self.current_date_label = tk.Label(self.window, text="Current Date:")
        self.current_date_label.config(font=("Roman", 14))
        self.current_date_label.place(x=cdl_x, y=sdl_y, width=cdl_w, anchor=tk.NW)
        cdv_x = cdl_x + cdl_w
        self.current_date_value = tk.Label(self.window, text=start_date)
        self.current_date_value.config(font=("Courier", 18))
        self.current_date_value.place(x=cdv_x,y=sdl_y, width=sdv_w, anchor=tk.NW)

        # Create the UI for the top right corner for # of stocks held
        shv_x = self.get_width() - 20
        shv_y = sdl_y
        shv_w = 80
        self.stocks_held_value = tk.Label(self.window,
            text=f"{len(self.sim.stocks)}",
            bd=1,
            padx=5,
            pady=5,
            relief="solid")
        self.stocks_held_value.config(font=("Courier", 32))
        self.stocks_held_value.place(x=shv_x,y=shv_y, width=shv_w, anchor=tk.NE)
        shl_x = shv_x - shv_w - x_buffer
        y_buffer = 10
        shl_y = shv_y + y_buffer
        shl_w = 250
        self.stocks_held_label = tk.Label(self.window, text="# of stocks in portfolio:")
        self.stocks_held_label.config(font=("Courier", 16))
        self.stocks_held_label.place(x=shl_x, y=shl_y, width=shl_w, anchor=tk.NE)

        # Create the UI for the second row for invested $, balance, total return, and day return
        row2_y = 120
        data = [None, self.sim.get_total_bal(), self.sim.total_return, self.sim.today_return]
        investment_summary_text = self.get_summary_text(data)
        self.summary_label = tk.Label(self.window,
            text=investment_summary_text,
            bd=1,
            padx=10,
            pady=10,
            relief="solid")
        self.summary_label.config(font=("Courier", 20))
        self.summary_label.place(relx=0.5, y=row2_y, anchor=tk.CENTER)
        self.create_summary_chart()

        # Create the UI for the Stock Table of returns TODO: Change all these text values
        c1_x = self.get_width() - 160
        c1_y = 220
        c1_w = 180
        c1_h = 400
        self.col1 = tk.Label(self.window, text="", bd=1, relief="solid", anchor=tk.N)
        self.col1.config(font=("Courier", 28))
        self.col1.place(x=c1_x,y=c1_y, width=c1_w, height=c1_h, anchor=tk.N)
        c2_x = c1_x - c1_w
        self.col2 = tk.Label(self.window, text="", bd=1, relief="solid", anchor=tk.N)
        self.col2.config(font=("Courier", 28))
        self.col2.place(x=c2_x,y=c1_y, width=c1_w, height=c1_h, anchor=tk.N)
        c3_x = c2_x - c1_w
        self.col3 = tk.Label(self.window, text="", bd=1, relief="solid", anchor=tk.N)
        self.col3.config(font=("Courier", 28))
        self.col3.place(x=c3_x,y=c1_y, width=c1_w, height=c1_h, anchor=tk.N)

        h1_h = 50
        self.h1 = tk.Label(self.window, text="Total Change (%)", bd=1, relief="solid")
        self.h1.config(font=("Helvetica", 18))
        self.h1.place(x=c1_x,y=c1_y, width=c1_w, height=h1_h, anchor=tk.S)
        self.h2 = tk.Label(self.window, text="Today's Change (%)", bd=1, relief="solid")
        self.h2.config(font=("Helvetica", 17))
        self.h2.place(x=c2_x,y=c1_y, width=c1_w, height=h1_h, anchor=tk.S)
        self.h3 = tk.Label(self.window, text="Stock Ticker", bd=1, relief="solid")
        self.h3.config(font=("Helvetica", 18))
        self.h3.place(x=c3_x,y=c1_y, width=c1_w, height=h1_h, anchor=tk.S)

        self.submit_button = tk.Button(text="Previous Day")
        self.submit_button.bind("<Button-1>", self.previous_day)
        self.submit_button.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

        self.submit_button = tk.Button(text="Next Day")
        self.submit_button.bind("<Button-1>", self.next_day)
        self.submit_button.place(relx=0.8, rely=0.9, anchor=tk.CENTER)

        self.window.mainloop()

    def next_day(self, event):
        history = self.sim.run_next_day()
        self.update_summary_chart(history)
        self.update_labels()

    def previous_day(self, event):
        history = self.sim.run_previous_day()
        self.update_summary_chart(history)
        self.update_labels()
    
    def update_labels(self):
        data = self.sim.history.get_day_data(self.sim.current_date)
        self.summary_label.config(text = self.get_summary_text(data))

        data = self.update_ordering(data[4:])
        self.current_date_value.config(text = self.sim.current_date.strftime('%m-%d-%Y'))
        self.stocks_held_value.config(text = len(data))
        self.col3.config(text = self.get_col3_text(data))
        self.col2.config(text = self.get_col2_text(data))
        self.col1.config(text = self.get_col1_text(data))

    def create_summary_chart(self):
        fig = Figure(figsize = (7,4.5))
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)   
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.3, rely=0.53, anchor=tk.CENTER)

    def update_summary_chart(self, history):
        fig = Figure(figsize = (7,4.5))
    
        plot = fig.add_subplot()
        plot.set_title("Portfolio Performance")
        plot.tick_params(axis='x', labelrotation=80) # Change rotation to 80 degrees
        plot.plot(history[0]) # TODO Change to correct spot in Series

        fig.tight_layout()
    
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)   
        self.canvas.draw()
    
        self.canvas.get_tk_widget().place(relx=0.3, rely=0.53, anchor=tk.CENTER)

    def update_ordering(self, data):
        new_data = []
        for stock in data:
            stock = stock.split('|')
            new_data.append([stock[0],stock[2],stock[3]])
        new_data.sort(key=lambda x: x[2], reverse=True)

        return new_data

    # Gets text for first column, 'Stock Ticker'
    def get_col3_text(self, data):
        text = ""
        for stock in data:
            text += stock[0] + '\n'
        return text

    # Gets text for second column, 'Today's Change'
    def get_col2_text(self, data):
        text = ""
        for stock in data:
            text += '{:3.5f}'.format((float(stock[1]) - 1)*100) + '\n'
        return text

    # Gets text for second column, 'Total Change'
    def get_col1_text(self, data):
        text = ""
        for stock in data:
            text += '{:3.5f}'.format((float(stock[2]) - 1)*100) + '\n'
        return text

    def get_summary_text(self, data):
        initial_bal_str = '{:12.2f}'.format(self.sim.initial_total_bal)
        current_bal_str = '{:12.2f}'.format(float(data[1]))
        total_return_str = '{:5.2f}'.format(float(data[2]) * 100)
        today_return_str = '{:5.2f}'.format(float(data[3]) * 100)
        text = f"Total Invested: ${initial_bal_str} |\
 Current Balance: ${current_bal_str} |\
 Total Return: {total_return_str}% |\
 Today Return: {today_return_str}%"
        return text
    
    def get_width(self):
        return int(self._geom.split('x')[0])

    def get_height(self):
        return int(self._geom.split('x')[1].split('+')[0])

    def click_submit(self, event):
        print("Handling click...")
        money = int(self.money_entry.get())

def main():
    pass

if __name__ == '__main__':
    main()