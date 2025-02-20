from core import TakerBotManager,ReddioBotManager,BlockingScheduler
if __name__ == '__main__':
    #邀请码任务平台网站 soneiumevent.unemeta.com/?invitationCode=true&codes=39YH8
    config_path='./config/config_reddio.json'
    manager=ReddioBotManager(config_path)
    manager.run()
    # 执行后每过24小时执行一次
    scheduler = BlockingScheduler()
    scheduler.add_job(manager.run, 'interval', hours=24)
    scheduler.start()