import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core.bot.axieinfinity_bot import *
from core.config import *
from core.extensions.agent import *
if __name__ == '__main__':
    config_path='./config/config_axieinfinity.json'
    manager=AxieinfinityManager(config_path)
    manager.run()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(manager.run, 'interval', hours=24) 
    # scheduler.start()