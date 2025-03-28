from bot import *
if __name__ == '__main__':
    config_path='projects/monaddailynft/config.json'
    manager=MonadDailyNFTBotManager(config_path)
    manager.run()