import tkinter as tk
from tkinter.filedialog import askopenfilename
from .AdvancedSimulatorGUI import AdvancedSimulatorGUI
from Bots.SimpleBot.SimpleBot import SimpleBot

class SimulatorSetupGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x1200")
        self.title = tk.Label(text="Paper Money Simulator")
        self.title.pack()
        self.money_label = tk.Label(text="Starting Money:")
        self.money_entry = tk.Entry()
        self.money_label.pack()
        self.money_entry.pack()
        
        self.start_label = tk.Label(text="Start Date:")
        self.start_entry = tk.Entry()
        self.start_label.pack()
        self.start_entry.pack()
        
        self.losslimit_label = tk.Label(text="Loss limit (%):")
        self.losslimit_entry = tk.Entry()
        self.losslimit_label.pack()
        self.losslimit_entry.pack()

        self.gainlimit_label = tk.Label(text="Gain limit (%):")
        self.gainlimit_entry = tk.Entry()
        self.gainlimit_label.pack()
        self.gainlimit_entry.pack()

        self.data_file_name = ""
        self.file_selection = tk.Label(text=self.data_file_name)
        self.file_selection.pack()


        self.submit_button = tk.Button(text="START FULL SIMULATION")
        self.submit_button.bind("<Button-1>", self.start_simulation)
        self.submit_button.pack()

        self.window.mainloop()
    
    def select_file(self, event):
        print("Choosing data file...")
        self.data_file_name = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.file_selection.config(text = self.data_file_name)
        print("Selected file: " + self.data_file_name)

    def start_simulation(self, event):
        print("Handling click...")
        money = int(self.money_entry.get()) if self.money_entry.get() != "" else 0
        print("Money: "  + str(money))
        start_date = self.start_entry.get()
        print("Start date: " + start_date)
        loss_limit = float(self.losslimit_entry.get()) / 100
        print(f"Loss limit {loss_limit}%")
        gain_limit = float(self.gainlimit_entry.get()) / 100
        print(f"Gain limit {gain_limit}%")
        self.window.destroy()
        adv_sim_gui = AdvancedSimulatorGUI(money, start_date, loss_limit, gain_limit, SimpleBot())
        
            
def main():
    SimulatorSetupGUI()

if __name__ == '__main__':
    main()