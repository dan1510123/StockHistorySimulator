from AdvancedSimulator.AdvancedSimulatorGUI import AdvancedSimulatorGUI
from Bots.SimpleBot.SimpleBot import SimpleBot

def main():
    bot = SimpleBot()
    sim = AdvancedSimulatorGUI(1000, '1-1-2021', 0.10, 0.05, bot)

if __name__ == '__main__':
    main()