import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core import TakerBotManager,ReddioBotManager,BlockingScheduler
import time
if __name__ == '__main__':
    #邀请码任务平台网站 soneiumevent.unemeta.com/?invitationCode=true&codes=39YH8
    config_path='./config/config_reddio.json'
    manager=ReddioBotManager(config_path)
    def run():
        manager.run()
        time.sleep(60*20)
        manager.verify_all_task()
    run()
    # 执行后每过24小时执行一次
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'interval', hours=24)
    scheduler.start()