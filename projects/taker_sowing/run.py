from bot import *
if __name__ == '__main__':
    config_path='projects/taker_sowing/config.json'
    manager=TakerBotManager(config_path)
    manager.run()
    while True:
        logger.info('run')
        manager.run()
        time.sleep(3*60*61)
    