import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..','..'))
sys.path.append(project_root)
from core.bot.basebot import *
from core.config import Config
from threading import Lock
lock=Lock()
#实例化以上合约
class MonadScoreBot(BaseBot):
    def _handle_response(self, response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            return response
        # 抛出代理错误
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    
            
    def registe(self):
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},注册中...")
        json_data = {
            'wallet': self.wallet.address,
            'invite': self.config.invite_code,
        }

        response = self.session.post('https://mscore.onrender.com/user', json=json_data)
        response=self._handle_response(response)
        if not self.account.get('registed'):
            self.account['registed']=True
            self.config.save_accounts()
        self.config.save_accounts()
        data=response.json()
        token=data.get('token')
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})
        
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},注册成功")
    def login(self):
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},登录中...")
        json_data = {
            'wallet': self.wallet.address,
        }
        response=self.session.post('https://mscore.onrender.com/user/login', json=json_data)
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},登录成功")
        # 登录后获取用户信息
        response=self._handle_response(response)
        data=response.json()
        token=data.get('token')
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})

        user=data.get('user')
        self.account.update(user)
        self.config.save_accounts()
        
    def mining(self):
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},minting中...")
        timestamp = int(time.time() * 1000)  # 获取当前时间戳（毫秒）
        json_data = {
            'wallet': self.wallet.address,
            'startTime': timestamp,
        }

        response = self.session.put('https://mscore.onrender.com/user/update-start-time', json=json_data)
        response=self._handle_response(response)
        data=response.json()
        if not  data.get('success'):
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},minting失败,{data.get('message')}")
        user=data.get('user')
        self.account.update(user)
        self.config.save_accounts()
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},minting成功")
    def claim_tasks (self):
        tasks=[
            'task001',
            'task002',
            'task003'
        ]
        for task in tasks:
            if self.account.get(f'task-{task}'):
                logger.info(f"账户:第{self.index}个地址,{self.wallet.address},claim_task {task} 已完成")
                return 
            logger.info(f"账户:第{self.index}个地址,{self.wallet.address},claim_task {task} 中...")
            json_data = {
                'wallet': self.wallet.address,
                'taskId': task,
            }

            response = requests.post('https://mscore.onrender.com/user/claim-task', json=json_data)
            response=self._handle_response(response)
            data=response.json()
            if not  data.get('success'):
                logger.error(f"账户:第{self.index}个地址,{self.wallet.address},minting失败,{data.get('message')}")
            if not self.account.get(f'task-{task}'):
                self.account[f'task-{task}']=True
                self.config.save_accounts()
            user=data.get('user')
            self.account.update(user)
            self.config.save_accounts()
class MonadScoreBotManager(BaseBotManager):
    def run_single(self,account):
        bot=MonadScoreBot(account,self.web3,self.config)
        bot.registe()
        bot.login()
        try:
            bot.mining()
        except Exception as e:
            logger.error(f"账户:第{bot.index}个地址,{bot.wallet.address},mining失败,原因:{e}")
        bot.claim_tasks()
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")


    