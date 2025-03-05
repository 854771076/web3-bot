import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core.bot.humanity_bot import *
from core.config import *
if __name__ == '__main__':
    config_path='./config/config_humanity.json'
    manager=HumanityManager(config_path)
    manager.run()
