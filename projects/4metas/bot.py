import os
import sys
import time
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..','..'))
sys.path.append(project_root)
from core.bot.basebot import *
from core.config import Config
from threading import Lock
import requests
lock=Lock()
lotteryContractAddress = "0x65ba8d178EC02b396b88971b6612b0be2c430608"
false=False
true=True
null=None
abi=[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"participant","type":"address"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"LotteryEntered","type":"event"},{"inputs":[],"name":"enterLottery","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"entries","outputs":[{"internalType":"address","name":"participant","type":"address"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEntries","outputs":[{"components":[{"internalType":"address","name":"participant","type":"address"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"internalType":"struct Lottery.Entry[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEntryCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
#实例化以上合约

class FourmetasBot(BaseBot):
    def __init__(self,account,web3,config:Config):
        super().__init__(account,web3,config)
        self.session=requests.Session(
            
        )
        self.main_wallet=self.web3.eth.account.from_key(config.main_wallet_private_key)
        self.session.headers.update({'User-Agent': self.ua.chrome})
        self.session.proxies=self.proxies
        self.login()
    def _handle_response(self, response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            data=response.json()
            if data.get('msg')!= 'success':
                raise Exception(f"执行异常,{data.get('msg')}")
            return data
        # 抛出代理错误
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    
    def login(self):
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},登录中...")
        json_data = {
            'type': 4,
            'authType': 'metamask',
            'uId': self.wallet.address,
            'address': self.wallet.address,
            'inviteCode': self.config.invite_code,
            'loginType': 2,
        }

        response = self.session.post('https://ss.4metas.io/formetas/user/login', json=json_data)
        data=self._handle_response(response)
        token=response.headers.get('access-token')
        if not token:
            raise Exception(f"登录失败,{response.text}")
        self.session.headers.update(response.headers)
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},登录成功")
        # 登录后获取用户信息
        user=json.dumps(data.get('data'))

        self.account['user']=user
        self.config.save_accounts()
    def completeMyTask(self,id):
        json_data = {
            'id': id,
        }
        response = self.session.post('https://ss.4metas.io/formetas/task/completeMyTask', json=json_data)
        data=self._handle_response(response)
        status=data.get('status')
        if status==1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},任务:{id},完成")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},任务:{id},完成失败,{response.text}")
    
    def getMyTaskReward(self,id):
        json_data = {
            'id': id,
        }
        response = self.session.post('https://ss.4metas.io/formetas/task/getMyTaskReward', json=json_data)
        data=self._handle_response(response)
        status=data.get('status')
        if status==1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},任务:{id},领取成功")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},任务:{id},领取失败,{response.text}")

    def complete_tasks(self):
        if self.account.get('task')==True:
            logger.info(f"账户:第{self.index}个地址,{self.wallet.address},任务已全部完成")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},开始完成任务...")
        json_data = {}
        response = self.session.post('https://ss.4metas.io/formetas/task/queryMyAppTaskInfo',  json=json_data)
        data=self._handle_response(response)
        for name,tasks in data.get('data',{}).items() :
            if name in ['dailyTask','checkInTask','dailyTask']:
                logger.info(f"账户:第{self.index}个地址,{self.wallet.address},任务组:{name}")
                for task in tasks:
                    try:
                        taskName= task.get('taskName')
                        if task.get('status')==1:
                            logger.debug(f"账户:第{self.index}个地址,{self.wallet.address},任务:{taskName},已完成")
                            break
                        else:
                            logger.info(f"账户:第{self.index}个地址,{self.wallet.address},任务:{taskName},开始完成")
                            errcount=0
                            while errcount<3:
                                try:
                                    self.completeMyTask(task.get('id'))
                                except Exception as e:
                                    if 'Already finish task' in str(e):
                                        logger.debug(f"账户:第{self.index}个地址,{self.wallet.address},任务:{taskName},已完成")
                                        break
                                    logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},任务:{taskName},完成失败,{e},重试中...")
                                    time.sleep(random.randint(15,30))     
                                    errcount+=1    
                            errcount=0                           
                            while errcount<3:
                                try:
                                    self.getMyTaskReward(task.get('id'))
                                except Exception as e:
                                    if 'Already' in str(e):
                                        logger.debug(f"账户:第{self.index}个地址,{self.wallet.address},任务:{taskName},已领取")
                                        break
                                    logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},任务:{taskName},领取失败,{e},重试中...")
                                    time.sleep(random.randint(15,30))
                                    errcount+=1 
                            break
                    except Exception as e:
                        
                        logger.error(f"账户:第{self.index}个地址,{self.wallet.address},任务:{taskName},完成失败,{e}")
                        time.sleep(random.randint(15,30))
                    
        self.account['task']=True
        self.config.save_accounts()

    def get_points(self):
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},开始获取积分...")
        json_data = {}
        response = self.session.post('https://ss.4metas.io/formetas/invite/queryMyInviteInfo', json=json_data)
        data=self._handle_response(response)
        currentPoints=int(data.get('data',{}).get('currentPoints'))
        return currentPoints
    def open_with_ad(self,hashId):
        json_data = {
            'id': 1,
            'ad': 0,
            'hashId': hashId,
        }

        response = self.session.post('https://ss.4metas.io/formetas/box/openWithAD', json=json_data)
        data=self._handle_response(response)
        num=data.get('data',[{}])[0].get('num')
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},开宝箱成功,获得 {num} Metas")
    def open_box(self):
        points=self.get_points()
        if points<200:
            logger.info(f"账户:第{self.index}个地址,{self.wallet.address},积分不足,无法开宝箱")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},开始开宝箱...")
        lotteryContract = self.web3.eth.contract(address=lotteryContractAddress, abi=abi)
        tx=lotteryContract.functions.enterLottery().build_transaction({
                'from': self.wallet.address,
                'gas': 2000000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address), 
            })
        tx_hash=send_transaction(self.web3,tx,self.wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)        
        if receipt.status == 1:
            self.open_with_ad(tx_hash.hex())
            logger.success(f'账户:{self.wallet.address},开宝箱成功,交易哈希:{tx_hash.hex()}')
        else:
            logger.error(f"账户:{self.wallet.address},,开宝箱失败,原因:{receipt}")
    def get_balance(self):
        json_data = {}
        response = self.session.post('https://ss.4metas.io/formetas/user/queryMyPoints', json=json_data)
        data=self._handle_response(response)
        metis=data.get('data',{}).get('metis')
        return metis
    
    def transfer_eth(self):
        if self.account.get('transfer')==True:
            logger.info(f"账户:第{self.index}个地址,{self.wallet.address},ETH已转账")
            return
        # 从主地址转账随机余额（0.023）到钱包地址，如果余额大于等于0.02eth则跳过
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance>self.web3.to_wei(0.02,'ether'):
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},余额足够,跳过")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},转账中...")
        with lock:
            transaction={
                'from': self.main_wallet.address,
                'to': self.wallet.address,
                'value': self.web3.to_wei(random.uniform(0.023,0.024),'ether'),
                'gasPrice': self.web3.eth.gas_price, 
                'gas': 50000,
                'nonce': self.web3.eth.get_transaction_count(self.main_wallet.address),
            } 
            tx_hash = send_transaction(self.web3, transaction, self.main_wallet.key)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},转账成功")
            self.account['transfer']=True
            self.config.save_accounts()
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},转账失败,原因:{receipt}")
    def transfer_eth_to_main(self):
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},转账中...")
        balance=self.web3.eth.get_balance(self.wallet.address)
        with lock:
            gas_balance=self.web3.eth.gas_price*51000
            transaction={
                'from': self.wallet.address,
                'to': self.main_wallet.address,
                'value':balance-gas_balance ,
                'gasPrice': self.web3.eth.gas_price, 
                'gas': 50000,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
            } 
            tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},转账成功")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},转账失败,原因:{receipt}")
    def withdraw(self):
        metis=self.get_balance()
        json_data = {
            'toAddress': self.wallet.address,
            'price': metis,
            'tokenId': 2,
        }

        response = self.session.post('https://ss.4metas.io/formetas/withdraw/withdrawUsdt', json=json_data)
        data=self._handle_response(response)
        status=data.get('status')
        if status==1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},提现成功,获得 {metis} metis")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},提现失败,{response.text}")
    def getspinNum(self):
        json_data = {}
        response = self.session.post('https://ss.4metas.io/formetas/box/spinNum', json=json_data)
        data=self._handle_response(response)
        spinNum=int(data.get('data',0))
        return spinNum
    def spin(self,hashId):
        json_data = {
            'hashId': hashId,
        }
        response = self.session.post('https://ss.4metas.io/formetas/box/spinIt', json=json_data)
        data=self._handle_response(response)
        num=data.get('data',{}).get('text')
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},spin成功,获得 {num} Metas")
    def start_spin(self):
        points=self.getspinNum()
        if points<=0:
            logger.info(f"账户:第{self.index}个地址,{self.wallet.address},次数不足,无法spin")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},开始spin...")
        lotteryContract = self.web3.eth.contract(address=lotteryContractAddress, abi=abi)
        tx=lotteryContract.functions.enterLottery().build_transaction({
                'from': self.wallet.address,
                'gas': 2000000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address), 
            })
        tx_hash=send_transaction(self.web3,tx,self.wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)        
        if receipt.status == 1:
            self.spin(tx_hash.hex())
            logger.success(f'账户:{self.wallet.address},spin成功,交易哈希:{tx_hash.hex()}')
        else:
            logger.error(f"账户:{self.wallet.address},spin失败,原因:{receipt}")


class FourmetasBotManager(BaseBotManager):
    def run_single(self,account):
        bot=FourmetasBot(account,self.web3,self.config)
        bot.complete_tasks()
        bot.transfer_eth()
        time.sleep(20)
        points=bot.get_points()
        while points>=200:
            try:
                logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},points:{points}")
                bot.open_box()
                points=bot.get_points()
            except Exception as e:
                logger.error(f"账户:第{bot.index}个地址,{bot.wallet.address},失败,原因:{e}")
        else:
            logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},points:{points},积分耗尽,退出")
        num=bot.getspinNum()
        while num>0:
            try:
                logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},num:{num}")
                bot.start_spin()
                num=bot.getspinNum()
            except Exception as e:
                logger.error(f"账户:第{bot.index}个地址,{bot.wallet.address},失败,原因:{e}")
        else:
            logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},num:{num},次数耗尽,退出")
        bot.transfer_eth_to_main()
    def run_withdraw_single(self,account):
        bot=FourmetasBot(account,self.web3,self.config)
        bot.withdraw()
    def run_withdraw(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_withdraw_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")
    def main_wallet_open_box(self):
        account={
            'private_key':self.config.main_wallet_private_key,
        }
        bot=FourmetasBot(account,self.web3,self.config)
        num=bot.getspinNum()
        while num>0:
            try:
                logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},num:{num}")
                bot.start_spin()
                num=bot.getspinNum()
            except Exception as e:
                logger.error(f"账户:第{bot.index}个地址,{bot.wallet.address},失败,原因:{e}")
        else:
            logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},num:{num},次数耗尽,退出")
        points=bot.get_points()
        while points>=200:
            try:
                logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},points:{points}")
                bot.open_box()
                points=bot.get_points()
            except Exception as e:
                logger.error(f"账户:第{bot.index}个地址,{bot.wallet.address},失败,原因:{e}")
        else:
            logger.info(f"账户:第{bot.index}个地址,{bot.wallet.address},points:{points},积分耗尽,退出")
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")


    