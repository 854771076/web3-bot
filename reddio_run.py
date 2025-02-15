from core import TakerBotManager,ReddioBotManager,BlockingScheduler
if __name__ == '__main__':
    config_path='./config/config_reddio.json'
    manager=ReddioBotManager(config_path)
    manager.run()
    # 执行后每过24小时执行一次
    scheduler = BlockingScheduler()
    scheduler.add_job(manager.run, 'interval', hours=24)
    scheduler.start()