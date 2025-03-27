from bot import *
if __name__ == '__main__':
    config_path='projects/monadscore/config.json'
    manager=MonadScoreBotManager(config_path)
    while True:
        logger.info('run')
        manager.run()
        time.sleep(24*60*61)