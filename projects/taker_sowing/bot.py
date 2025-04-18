import os
import sys
import time
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..','..'))
sys.path.append(project_root)
from core.bot.basebot import *

from core.bot.basebot import *
class TakerBot(BaseBot):
    def _handle_response(self, response: requests.Response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            try:
                data=response.json()
                if data.get('code')!=200:
                    raise Exception(f"执行异常,{data.get('message')}")
                return data
            except Exception as e:
                return response.text
        # 抛出代理错误
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    def get_user_info(self):
        response = self.session.get('https://sowing-api.taker.xyz/user/info')
        data=self._handle_response(response)
        userinfo=data.get('result',{})
        self.account.update(userinfo)
        self.config.save_accounts()
        return userinfo
    def login(self):
        def get_nonce():
            json_data = {
                'walletAddress': self.wallet.address,
            }
            response = self.session.post('https://sowing-api.taker.xyz/wallet/generateNonce', json=json_data)
            data=self._handle_response(response)
            nonce=data.get('result',{}).get('nonce')
            return nonce
        
        token=self.account.get('token')
        login_time=self.account.get('login_time')
        if token and check_exp(login_time):
            logger.info(f"账户:{self.wallet.address},token复用")
        else:
            if not self.account.get('registed'):
                logger.warning(f"账户:{self.wallet.address},未注册,注册中...")
                nonce=get_nonce()
                json_data = {
                    'address': self.wallet.address,
                    'signature': get_sign(self.web3,self.wallet.key, nonce),
                    "invitationCode":self.config.invite_code,
                    'message': nonce,
                }
            else:
                logger.warning(f"账户:{self.wallet.address},token失效,登录中...")
                nonce=get_nonce()
                json_data = {
                    'address': self.wallet.address,
                    'signature': get_sign(self.web3,self.wallet.key, nonce),
                    'message': nonce,
                }
                
            response = self.session.post('https://sowing-api.taker.xyz/wallet/login', json=json_data)
            data=self._handle_response(response)
            token=data.get('result',{}).get('token')
            login_time=int(time.time())
            if not self.account.get('registed'):
                self.account['registed']=True
                self.config.save_accounts()
            self.account['token']=token
            self.account['login_time']=login_time
            self.config.save_accounts()
        self.session.headers.update({
            'Authorization': 'Bearer '+token
        })
        self.get_user_info()
        logger.success(f"登录成功,账户:{self.wallet.address}")
    def connect_x(self,url="https://twitter.com/i/oauth2/authorize?response_type=code&client_id=d1E1aFNaS0xVc2swaVhFaVltQlY6MTpjaQ&redirect_uri=https%3A%2F%2Fearn.taker.xyz%2Fbind%2Fx&scope=tweet.read+users.read+follows.read&state=state&code_challenge=challenge&code_challenge_method=plain"):
        assert self.account.get('registed'),"账户未注册"
        if self.account.get('bind_x'):
            return
        if self.account.get('x_token_bad'):
            raise Exception(f"账户:{self.wallet.address},x_token失效")
            
        def submit_connect_x(oauth_token):
            json_data = {
                'code': oauth_token,
                'redirectUri': 'https://earn.taker.xyz/bind/x',
                'bindType': 'x',
            }
            response = self.session.post('https://lightmining-api.taker.xyz/odyssey/bind/mediaAccount', json=json_data)
            data=self._handle_response(response)
            msg=data.get('msg')
            self.account['bind_x']=True
            self.config.save_accounts()
            logger.success(f"账户:{self.wallet.address},{msg},x绑定成功")
        xauth=XAuth(self.account.get('x_token'),proxies=self.proxies)
        try:
            oauth_token=xauth.oauth2(url)[0]
        except Exception as e:
            if "Bad Token" in str(e):
                self.account['x_token_bad']=True
                self.config.save_accounts()
            raise e
        submit_connect_x(oauth_token)
    def mining(self):
        assert self.account.get('registed'),"账户未注册"
        
        def start_mining():
            cf_token=get_cf_token(self.config.site,self.config.sitekey,method=self.config.cf_api_method,url=self.config.cf_api_url,authToken=self.config.cf_api_key)
            self.session.headers.update({
               'cf-turnstile-token':cf_token 
            })
            response = self.session.get('https://sowing-api.taker.xyz/task/signIn?status=true')
            response.raise_for_status()
            if not self.account.get('mining_first'):
                self.account['mining_first']=True
                self.config.save_accounts()
            logger.success(f"账户:{self.wallet.address},{response.text},开始挖矿")
        def start_mining_by_contract(abi,address):
            # cf_token=get_cf_token(self.config.site,self.config.sitekey,method=self.config.cf_api_method,url=self.config.cf_api_url,authToken=self.config.cf_api_key)
            contract=self.web3.eth.contract(address=address,abi=abi)
            tx=contract.functions.active().build_transaction({
                'from': self.wallet.address,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address), 
            })
            signed_txn = self.wallet.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                logger.success(f"账户:{self.wallet.address},合约:{address},开始挖矿")
                start_mining()
            else:
                logger.error(f"账户:{self.wallet.address},合约:{address},开始挖矿失败,原因:{receipt}")
        assert self.account.get('registed'),"账户未注册"
        address='0xf929ab815e8bfb84cdab8d1bb53f22eb1e455378'
        abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"}],"name":"ERC1967InvalidImplementation","type":"error"},{"inputs":[],"name":"ERC1967NonPayable","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[],"name":"UUPSUnauthorizedCallContext","type":"error"},{"inputs":[{"internalType":"bytes32","name":"slot","type":"bytes32"}],"name":"UUPSUnsupportedProxiableUUID","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"Active","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"UPGRADE_INTERFACE_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"active","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserActiveLogs","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"initialOwner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"userActiveLogs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userLastActiveTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"users","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"usersLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
        if not self.account.get('mining_first'):
            start_mining()
        else:
            start_mining_by_contract(abi,address)

    def get_task(self):
        assert self.account.get('registed'),"账户未注册"
        return [
            {
            "assignmentId":6,
            "taskEvent":[
                {
                    "eventId":1, 
                    "answer":[
                        "C"
                    ]
                },
                {
                    "eventId":2, 
                    "answer":[
                        "A"
                    ]
                },
                {
                    "eventId":3, 
                    "answer":[
                        "D"
                    ]
                }
            ]
        }
                
        ]
    def done_tasks(self):
        def claim_reward(taskId):
            params = {
                'taskId': str(taskId),
            }
            try:
                cf_token=get_cf_token(self.config.site,self.config.sitekey,method=self.config.cf_api_method,url=self.config.cf_api_url,authToken=self.config.cf_api_key)
                self.session.headers.update({
                'cf-turnstile-token':cf_token 
                })
                response = self.session.post('https://sowing-api.taker.xyz/task/claim-reward', params=params)
                data=self._handle_response(response)
                logger.success(f"账户:{self.wallet.address},任务:{taskId},领取奖励成功,{data}")
                self.account[f'{taskId}_reward']=True
                self.config.save_accounts()
            except Exception as e:
                logger.error(f"账户:{self.wallet.address},任务:{taskId},领取奖励失败,{e}")
        def done_task(task):
            
            assignmentId=task.get('assignmentId')
            taskEvent=task.get('taskEvent')
            if self.account.get(f'{assignmentId}_reward'):
                logger.info(f"账户:{self.wallet.address},任务:{assignmentId}已领取奖励,跳过")
                return
            for event in taskEvent:
                eventId=event.get('eventId')
                answer=event.get('answer')
                json_data = {
                    'taskId': assignmentId,
                    'taskEventId':eventId,
                    'answerList': answer,
                }
                success_count=0
                try:
                    if self.account.get(f'{assignmentId}_{eventId}'):
                        logger.info(f"账户:{self.wallet.address},任务:{assignmentId},{eventId}已完成,跳过")
                        success_count+=1
                        continue
                    response = self.session.post('https://sowing-api.taker.xyz/task/check', json=json_data)
                    data=self._handle_response(response)
                    msg=data
                    logger.success(f"账户:{self.wallet.address},完成任务:assignmentId:{assignmentId},eventId:{eventId},{msg}")
                    success_count+=1
                    self.account[f'{assignmentId}_{eventId}']=True
                    self.config.save_accounts()
                    
                except Exception as e:
                    logger.error(f"账户:{self.wallet.address},完成任务:assignmentId:{assignmentId},eventId:{eventId},失败,{e}")
                time.sleep(3)
            logger.success(f"账户:{self.wallet.address},任务:{assignmentId}完成")
            claim_reward(assignmentId)

        assert self.account.get('registed'),"账户未注册"
        task_list=self.get_task()
        if not task_list:
            return
        for task in task_list:
            try:
                done_task(task)  
            except Exception as e:
                logger.error(f"账户:{self.wallet.address},完成任务:{task.get('assignmentId')}失败,{e}")
            time.sleep(3)

class TakerBotManager(BaseBotManager):
    def run_single(self,account):
        bot=TakerBot(account,self.web3,self.config)
        bot.login()
        try:
            bot.mining()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},挖矿失败,{e}")
        bot.done_tasks()
        try:
            bot.get_user_info()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},获取用户信息失败,{e}")
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts if not account.get('x_token_bad')]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # logger.error(f"执行过程中发生错误: {e}")
                    logger.exception(e)
