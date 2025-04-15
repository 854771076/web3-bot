from bot import *
if __name__ == '__main__':
    config_path='projects/4metas/config.json'
    manager=FourmetasBotManager(config_path)
    manager.run_withdraw()
    