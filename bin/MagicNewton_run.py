import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core import *
if __name__ == '__main__':
    config_path='./config/config_magic_newton.json'
    manager=MagicNewtonManager(config_path)
    # manager.run()
    # # 执行后每过24小时执行一次
    # scheduler = BlockingScheduler()
    # scheduler.add_job(manager.run, 'interval', hours=24) 
    # scheduler.start()
    manager.run_single(manager.accounts[0])