import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core import *
if __name__ == '__main__':
    config_path='./config/config_soneium.json'
    manager=SoneiumBotManager(config_path)
    while True:
        logger.info('run')
        manager.run()
        time.sleep(24*60*61)