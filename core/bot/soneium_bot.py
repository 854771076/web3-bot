from core.bot.basebot import *
with open('contracts/SeaDrop.json','r') as f:
    contract_json=json.load(f)
class SoneiumBot(BaseBot):
    def _init_contract(self):
        self.nft_manager=self.web3.eth.contract(address=contract_json['address'],abi=contract_json['abi'])
    
    def __init__(self,account,web3,config:Config):
        super().__init__(account,web3,config)
        self.web3_base = Web3(Web3.HTTPProvider(self.config.base_rpc_url,request_kwargs={"proxies": self.proxies}))
        self.task=[4,0,1,2,3,5,8,7,6]
        self.daily_task=[6]
        self._init_contract()
    def mint_nft(self):
        if self.account.get('mint'):
            logger.warning(f"账户:{self.wallet.address},已经mint过,跳过")
            return
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance==0:
            logger.warning(f"账户:{self.wallet.address},余额不足,跳过")
            return
        logger.info(f"账户:{self.wallet.address},铸造中...")
        func=self.nft_manager.functions.mintPublic(
            '0x1e807EfC2416c6CD63cb3B01Dc91232D6F02d50A',
            '0x0000a26b00c1F0DF003000390027140000fAa719',
            '0x0000000000000000000000000000000000000000',
            1000, 
        )
        tx=func.build_transaction({
            'from':self.wallet.address,
            'nonce':self.web3.eth.get_transaction_count(self.wallet.address),
            'gasPrice':self.web3.eth.gas_price,
        })
        signed_txn = self.wallet.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:{self.wallet.address},mint成功")
            self.account['mint']=True
            self.config.save_accounts()
        else:
            logger.error(f"账户:{self.wallet.address},,mint失败,原因:{receipt}")
    def do_task(self,task_id):
        assert self.account.get('registed'),"账户未注册"
        def complete_task(task_id):
            json_data = {
                'task_id': task_id,
            }
            response = self.session.post('https://soneiumevent.unemeta.com/api/sonieum/v1/task/complete', json=json_data)
            data=self._handle_response(response)
            logger.success(f"账户:{self.wallet.address},任务完成-{task_id}")
        def claim_task(task_id):
            nonce=self.get_sign()
            json_data = {
                'task_id': task_id,
                'nonce':nonce
            }
            response = self.session.post('https://soneiumevent.unemeta.com/api/sonieum/v1/task/claim', json=json_data)
            data=self._handle_response(response)
            logger.success(f"账户:{self.wallet.address},领取任务成功-{task_id}")
           
        if not self.account.get(f'task_{task_id}') or task_id in self.daily_task:
            try:
                complete_task(task_id)
            except Exception as e:
                logger.warning(f"账户:{self.wallet.address},完成任务失败-{task_id},{e}")
            try:
                claim_task(task_id)
            except Exception as e:
                logger.warning(f"账户:{self.wallet.address},领取任务失败-{task_id},{e}")
    def run_45_tx(self):
        if self.account.get('45_tx'):
            return
        for i in range(45):
            self.get_sign()
            logger.info(f"账户:{self.wallet.address},发送交易-{i}")
        logger.success(f"账户:{self.wallet.address},run_45_tx成功")
        self.account['45_tx']=True
        self.config.save_accounts()
    def do_all_task(self):
        for task_id in self.task:
            try:
                self.do_task(task_id)
                self.account[f'task_{task_id}']=True
                self.config.save_accounts()
            except Exception as e:
                logger.warning(f"账户:{self.wallet.address},任务失败-{task_id},{e}")
    def mini_nft1(self):
        if self.account.get('mini_nft1'):
            return
        abi=json.loads('[{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nopayable","type":"function"}]')
        address='0x52d44Bea684eCd8Cad6d02205e40FC3bD59Ad877'
        contract = self.web3.eth.contract(address=address, abi=abi)
        tx = contract.functions.mint().build_transaction({
            'from': self.wallet.address,
            'gas': 200000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address),

        })
        tx_hash=send_transaction(self.web3,tx,self.wallet.key)
        receipt=self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status==0:
            logger.warning(f"账户:{self.wallet.address},mint失败,{receipt}")
            return
        logger.success(f"账户:{self.wallet.address},mint成功")
        self.account['mini_nft1']=True
        self.config.save_accounts()
    def mini_nft2(self):
        if self.account.get('mini_nft2'):
            return
        abi=json.loads('[{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nopayable","type":"function"}]')
        address='0xAF27443284F86CBdc1fa71941e8B787e5A4440De'
        contract = self.web3.eth.contract(address=address, abi=abi)
        tx = contract.functions.mint().build_transaction({
            'from': self.wallet.address,
            'gas': 200000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address),

        })
        tx_hash=send_transaction(self.web3,tx,self.wallet.key)
        receipt=self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status==0:
            logger.warning(f"账户:{self.wallet.address},mint失败,{receipt}")
            return
        logger.success(f"账户:{self.wallet.address},mint成功")
        self.account['mini_nft2']=True
        self.config.save_accounts()
    def bridge_eth(self):
        if  self.account.get('bridge'):
            return
        def get_transaction(address,amount=0.000187):
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://superbridge.app',
                'Pragma': 'no-cache',
                'Referer': 'https://superbridge.app/',
                'User-Agent': self.ua.chrome,
            }

            json_data = {
                'host': 'superbridge.app',
                'amount': str(self.web3.to_wei(amount, 'ether')),
                'fromChainId': '8453',
                'toChainId': '1868',
                'fromTokenAddress': '0x0000000000000000000000000000000000000000',
                'toTokenAddress': '0x0000000000000000000000000000000000000000',
                'fromTokenDecimals': 18,
                'toTokenDecimals': 18,
                'fromGasPrice': self.web3_base.eth.gas_price,
                'toGasPrice': self.web3.eth.gas_price,
                'graffiti': 'superbridge',
                'recipient': address,
                'sender': address,
                'forceViaL1': False,
            }
            response = requests.post('https://api.superbridge.app/api/v2/bridge/routes', headers=headers, json=json_data)
            initiatingTransaction=response.json()['results'][0]['result']['initiatingTransaction']
            return initiatingTransaction
        initiatingTransaction=get_transaction(self.wallet.address)
        initiatingTransaction['nonce']=self.web3_base.eth.get_transaction_count(self.wallet.address)
        initiatingTransaction['gasPrice']=self.web3_base.eth.gas_price
        initiatingTransaction['gas']=200000
        initiatingTransaction['chainId']=int(initiatingTransaction['chainId'])
        initiatingTransaction['value']=int(initiatingTransaction['value'])
        send_transaction(self.web3_base,initiatingTransaction,self.wallet.key)
        logger.success(f"账户:{self.wallet.address},桥接成功")
        self.account['bridge']=True
        self.config.save_accounts()
    def get_user_info(self):
        response = self.session.get('https://soneiumevent.unemeta.com/api/sonieum/v1/user/info')
        data=self._handle_response(response)
        userinfo=data.get('data',{})
        self.account.update(userinfo['user_info'])
        self.task_info=userinfo['task_info']
        self.config.save_accounts()
        return userinfo
    def get_sign(self):
        resp=self.session.get('https://soneiumevent.unemeta.com/api/sonieum/v1/nonce/max')
        data=self._handle_response(resp)
        max_nonce=data.get('data').get('nonce')

        address='0xbb4904e033Ef5Af3fc5d3D72888f1cAd7944784D'
        abi=json.loads('[{"inputs":[],"name":"Sign","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":false,"internalType":"uint256","name":"_newValue","type":"uint256"}],"name":"SignEvent","type":"event"},{"inputs":[],"name":"getCurrentNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
        contract=self.web3.eth.contract(address=address,abi=abi)
        tx=contract.functions.Sign().build_transaction({
            'from': self.wallet.address,
            'gas': 200000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address), 
        })
        signed_txn = self.wallet.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:{self.wallet.address},合约:{self.wallet.address},sign成功")
        else:
            logger.error(f"账户:{self.wallet.address},合约:{self.wallet.address},sign失败,原因:{receipt}")
            
        return max_nonce+1
    def checkin(self):
        assert self.account.get('registed'),"账户未注册"
        def start_checkin(nonce):
            json_data = {
                'nonce': nonce,
            }
            response = self.session.post('https://soneiumevent.unemeta.com/api/sonieum/v1/task/checkin', json=json_data)
            data=self._handle_response(response)
            msg=data.get('msg')
            logger.success(f"账户:{self.wallet.address},{msg},签到成功")
        def start_checkin_by_contract():
            nonce=self.get_sign()
            
            start_checkin(nonce)
            
        assert self.account.get('registed'),"账户未注册"
        self.get_user_info()
        can_checkin=self.task_info.get('can_checkin_task_today')
        if can_checkin:
            
            start_checkin_by_contract()
        else:
            logger.warning(f"账户:{self.wallet.address},24小时内已签到")

    def login(self):
        def set_invitationCode():
            json_data = {
                'invite_code': self.config.invite_code,
            }
            response = self.session.post('https://soneiumevent.unemeta.com/api/sonieum/v1/invite/fill', json=json_data)
            try:
                data=self._handle_response(response)
                logger.success(f"账户:{self.wallet.address},设置邀请码成功")
                self.account['registed']=True
                self.config.save_accounts()
            except Exception as e:
                logger.error(f"账户:{self.wallet.address},设置邀请码失败,{e}")
        token=self.account.get('token')
        
        # if token and check_jwt_exp(token):
        #     logger.info(f"账户:{self.wallet.address},token复用")
        # else:
        if not self.account.get('registed'):
            logger.warning(f"账户:{self.wallet.address},未注册,注册中...")
        else:
            logger.warning(f"账户:{self.wallet.address},token失效,登录中...")
        json_data = {
        'wallet_address': self.wallet.address,
        'okx_connect': True,
        }
        response = self.session.post('https://soneiumevent.unemeta.com/api/sonieum/v1/connect/wallet', json=json_data)
        data=self._handle_response(response)
        token=data.get('data',{}).get('token')                
        self.account['token']=token
        self.config.save_accounts()
        self.session.headers.update({
            'Authorization': 'Bearer '+token
        })
        self.session.cookies.update({
            'Authorization': 'Bearer '+token
        })
        if not self.account.get('registed'):
            set_invitationCode()
            
        self.get_user_info()
        logger.success(f"登录成功,账户:{self.wallet.address}")
class SoneiumBotManager(BaseBotManager):
    def run_single(self,account):
        bot=SoneiumBot(account,self.web3,self.config)
        try:
            bot.mint_nft()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},mint失败,{e}")
        try:
            bot.bridge_eth()
            time.sleep(30)
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},桥接失败,{e}")
        try:
            bot.login()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},登录失败,{e}")
        try:
            bot.checkin()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},签到失败,{e}")
        try:
            bot.do_all_task()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},任务失败,{e}")
        bot.get_user_info()
        try:
            bot.run_45_tx()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},run_45_tx失败,{e}")
        try:
            bot.mini_nft1()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},mini_nft1失败,{e}")
        try:
            bot.mini_nft2()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},mini_nft2失败,{e}")
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")
