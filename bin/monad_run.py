import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core import *
if __name__ == '__main__':
    config_path='./config/config_monad.json'
    manager=MonadBotManager(config_path)
    while True:
        start_time = time.time()
        logger.info('run')
        manager.run()
        end_time = time.time()
        logger.info(f"run time: {end_time - start_time}")
        # 执行时间小于一天，休眠到一天
        if end_time - start_time < 24*60*61:
            time.sleep(24*60*61 - (end_time - start_time))