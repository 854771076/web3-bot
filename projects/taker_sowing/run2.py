from bot import *
if __name__ == '__main__':
    config_path2='projects/taker_sowing/config.json'
    config_path='projects/taker_sowing/config2.json'
    manager=TakerBotManager2(config_path,config_path2)
    manager.run()
    while True:
        logger.info('run')
        manager.run()
        time.sleep(3*60*61)
    