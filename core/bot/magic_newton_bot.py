from core.bot.basebot import *
class MagicNewtonBot(BaseBot):
    def _handle_response(self, response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            data=response.json()
            # if data.get('status')!="OK":
            #     raise Exception(f"执行异常,{data.get('error')}")
            return data
        # 抛出代理错误
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    def get_user_info(self):
        response = self.session.get('https://lightmining-api.taker.xyz/user/getUserInfo')
        data=self._handle_response(response)
        userinfo=data.get('data',{})
        self.account.update(userinfo)
        self.config.save_accounts()
        return userinfo
    def login(self):
        def get_nonce():
            response=self.session.get('https://www.magicnewton.com/portal/api/auth/csrf')
            data=self._handle_response(response)
            nonce=data.get('csrfToken')
            return nonce
        def get_session():
            response=self.session.get('https://www.magicnewton.com/portal/api/auth/session')
            self._handle_response(response)
        def get_config():
            response=self.session.get('https://auth.magic.link/api/magic-client/cGtfbGl2ZV9DMTgxOUQ1OUY1REZCOEUy/config')
            data=self._handle_response(response)
            return data
        get_session()
        get_config()
        token=self.account.get('token')
        login_time=self.account.get('login_time')
        
        if token and check_exp(login_time):
            logger.info(f"账户:{self.wallet.address},token复用")
        else:
            nonce=get_nonce()
            time=get_string_from_time()
            msg=f'www.magicnewton.com wants you to sign in with your Ethereum account:\{self.wallet.address}\n\nPlease sign with your account\n\nURI: https://www.magicnewton.com\nVersion: 1\nChain ID: 1\nNonce: {nonce}\nIssued At: {time}'
            token=get_cf_token(self.config.site,self.config.sitekey,method=self.config.cf_api_method,url=self.config.cf_api_url,authToken=self.config.cf_api_key,action=self.config.action)
            if not self.account.get('registed'):
                logger.warning(f"账户:{self.wallet.address},未注册,注册中...")
                data = {
                    'message': msg,
                    'signature':  get_sign(self.web3,self.wallet.key, msg),
                    'redirect': 'false',
                    'recaptchaToken': token,
                    'refCode': self.config.invite_code,
                    'botScore': '1',
                    'csrfToken': nonce,
                    'callbackUrl': 'https://www.magicnewton.com/portal',
                    'json': 'true',
                }
            else:
                logger.warning(f"账户:{self.wallet.address},token失效,登录中...")
                data = {
                    'message': msg,
                    'signature':  get_sign(self.web3,self.wallet.key, msg),
                    'redirect': 'false',
                    'recaptchaToken': token,
                    'refCode': '',
                    'botScore': '1',
                    'csrfToken': nonce,
                    'callbackUrl': 'https://www.magicnewton.com/portal',
                    'json': 'true',
                }
            response1=self.session.get('https://www.magicnewton.com/portal/api/auth/providers')
            nonce=get_nonce()
            response = self.session.post('https://www.magicnewton.com/portal/api/auth/callback/credentials', data=data)  
            data=self._handle_response(response)
            token=self.session.cookies.get_dict().get('__Secure-next-auth.session-token')
            login_time=int(time.time())
            if not self.account.get('registed'):
                self.account['registed']=True
                self.config.save_accounts()
            self.account['token']=token
            self.account['login_time']=login_time
            self.config.save_accounts()
        self.session.cookies.update({
            '__Secure-next-auth.session-token': token
        })
        self.get_user_info()
        logger.success(f"登录成功,账户:{self.wallet.address}")
    def connect_x(self,url="https://twitter.com/i/oauth2/authorize?response_type=code&client_id=d1E1aFNaS0xVc2swaVhFaVltQlY6MTpjaQ&redirect_uri=https%3A%2F%2Fearn.taker.xyz%2Fbind%2Fx&scope=tweet.read+users.read+follows.read&state=state&code_challenge=challenge&code_challenge_method=plain"):
        assert self.account.get('registed'),"账户未注册"
        assert self.account.get('x_token'),"x_token为空"
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
        xauth=XAuth(self.account.get('x_token'))
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
        assert  self.account.get('bind_x'),"x未绑定"
        def get_last_mining_time():
            response = self.session.get('https://lightmining-api.taker.xyz/assignment/totalMiningTime')
            data=self._handle_response(response)
            return data.get('data',{}).get('lastMiningTime')
        def start_mining():
            response = self.session.post('https://lightmining-api.taker.xyz/assignment/startMining')
            data=self._handle_response(response)
            msg=data.get('msg')
            if not self.account.get('mining_first'):
                self.account['mining_first']=True
                self.config.save_accounts()
            logger.success(f"账户:{self.wallet.address},{msg},开始挖矿")
        def start_mining_by_contract(abi,address):
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
        last_mining_time=get_last_mining_time()
        can_mining=is_24_hours_away(last_mining_time)
        if can_mining:
            address='0xB3eFE5105b835E5Dd9D206445Dbd66DF24b912AB'
            abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"}],"name":"ERC1967InvalidImplementation","type":"error"},{"inputs":[],"name":"ERC1967NonPayable","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[],"name":"UUPSUnauthorizedCallContext","type":"error"},{"inputs":[{"internalType":"bytes32","name":"slot","type":"bytes32"}],"name":"UUPSUnsupportedProxiableUUID","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"Active","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"UPGRADE_INTERFACE_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"active","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserActiveLogs","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"initialOwner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"userActiveLogs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userLastActiveTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"users","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"usersLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
            if not self.account.get('mining_first'):
                start_mining()
            else:
                start_mining_by_contract(abi,address)
        else:
            logger.warning(f"账户:{self.wallet.address},24小时内已挖矿")
    def get_task(self):
        assert self.account.get('registed'),"账户未注册"
        assert  self.account.get('bind_x'),"x未绑定"
        response = self.session.post('https://lightmining-api.taker.xyz/assignment/list')
        data=self._handle_response(response)
        tasks=[task for task in data.get('data',[]) if not task.get('done') and task.get('assignmentId') not in [2,3,6,7,8,9,10,11,12]]
        if not tasks:
            logger.warning(f"账户:{self.wallet.address},无未完成任务")
            return []
        return tasks
    def done_tasks(self):
        def done_task(task):
            assignmentId=task.get('assignmentId')
            if task.get('cfVerify'):
                if not self.config.cf_task:
                    return 
                cf_token=get_cf_token(self.config.site,self.config.sitekey,method=self.config.cf_api_method,url=self.config.cf_api_url,authToken=self.config.cf_api_key)
                json_data = {
                    'assignmentId': assignmentId,
                    'verifyResp': cf_token,
                }
            else:
                json_data = {
                    'assignmentId': assignmentId,
                }
            response = self.session.post('https://lightmining-api.taker.xyz/assignment/do', json=json_data)
            data=self._handle_response(response)
            msg=data.get('msg')
            logger.success(f"账户:{self.wallet.address},完成任务:{assignmentId},{msg}")
        assert self.account.get('registed'),"账户未注册"
        assert  self.account.get('bind_x'),"x未绑定"
        task_list=self.get_task()
        if not task_list:
            return
        for task in task_list:
            try:
                done_task(task)  
            except Exception as e:
                logger.error(f"账户:{self.wallet.address},完成任务:{task.get('assignmentId')}失败,{e}")
            time.sleep(3)

class MagicNewtonManager(BaseBotManager):
    def run_single(self,account):
        bot=MagicNewtonBot(account,self.web3,self.config)
        bot.login()
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts if not account.get('x_token_bad')]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")

# curl 'https://www.magicnewton.com/portal/api/auth/csrf' \
#   -H 'accept: */*' \
#   -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
#   -H 'cache-control: no-cache' \
#   -H 'content-type: application/json' \
#   -b '_ga=GA1.1.1780817465.1740401003; __Host-next-auth.csrf-token=6c849be943326cfe40066c4447e65a6dcd9ac34329866aa25506318923a53094%7Cdcb9ecc9fa9de5ee28bc62c200236a4659fa6c96171633a721e6bd47fcb4e0cc; __Secure-next-auth.callback-url=https%3A%2F%2Fportal.magicnewton.com; wagmi.recentConnectorId="io.metamask"; _ga_2BFPMRZ2M3=GS1.1.1740401003.1.1.1740401071.0.0.0; wagmi.store={"state":{"connections":{"__type":"Map","value":[["ce25d1e6d39",{"accounts":["0x72691a36ED1fAC3b197Fb42612Dc15a8958bf9f2"],"chainId":1,"connector":{"id":"io.metamask","name":"MetaMask","type":"injected","uid":"ce25d1e6d39"}}]]},"chainId":1,"current":"ce25d1e6d39"},"version":2}' \
#   -H 'pragma: no-cache' \
#   -H 'priority: u=1, i' \
#   -H 'referer: https://www.magicnewton.com/portal' \
#   -H 'sec-ch-ua: "Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'