import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core.bot.humanity_bot import *
from core.config import *
from core.extensions.agent import *
if __name__ == '__main__':
    config_path='./config/config_humanity.json'
    manager=HumanityManager(config_path)
    username, password, host, port = split_proxy_url(manager.config.proxy)
    proxy_auth_plugin_path = create_proxy_auth_extension(
        plugin_path="./agent",
        proxy_host=host,
        proxy_port=port,
        proxy_username=username,
        proxy_password=password
    )
    
    manager.run()
    scheduler = BlockingScheduler()
    scheduler.add_job(manager.run, 'interval', hours=24) 
    scheduler.start()