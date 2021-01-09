from AdvancedSimulator.AdvancedSimulatorGUI import AdvancedSimulatorGUI
from Bots.SimpleBot.SimpleBot import SimpleBot

def main():
    bot = SimpleBot()
    sim = AdvancedSimulatorGUI(1000, '11-1-2020', 0.10, 0.05, bot, exclude=['DNB','BBBY'])

if __name__ == '__main__':
    main()