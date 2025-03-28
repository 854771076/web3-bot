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
class MonadDailyNFTBot(BaseBot):
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
        if self.account.get('registed'):
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},注册中...")
        json_data = {
            'walletAddress': self.wallet.address,
        }

        response = self.session.post('https://monadecobackend-production.up.railway.app/register', json=json_data)
        response=self._handle_response(response)
        data=response.json()
        if not self.account.get('registed'):
            self.account['registed']=True
            
            self.config.save_accounts()
        token=data.get('token')
        if not token:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},注册失败,{data.get('message')}")
            return
        self.session.headers['Authorization']=f'Bearer {token}'
        self.account.update(data)
        self.config.save_accounts()
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},注册成功")
    def status(self):
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},查询状态中...")

        response = self.session.get(f'https://monadecobackend-production.up.railway.app/user/status/{self.wallet.address}')
        response=self._handle_response(response)
        data=response.json()
        
        self.account.update(data)
        self.config.save_accounts()
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},查询状态成功")
    
class MonadDailyNFTBotManager(BaseBotManager):
    def run_single(self,account):
        bot=MonadDailyNFTBot(account,self.web3,self.config)
        bot.registe()
        bot.status()
    
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")


    