from requests import Response
from core.bot.basebot import *


class ReddioBot(BaseBot):
    daily_task_list={
        'Faucet':'c2cf2c1d-cb46-406d-b025-dd6a00369214',
        'transfer':'c2cf2c1d-cb46-406d-b025-dd6a00369215',
        # 'Bridge':'c2cf2c1d-cb46-406d-b025-dd6a00369216'
    }
    once_task_list={
       'deploy' :'c2cf2c1d-cb46-406d-b025-dd6a00369217'
    }
    def _handle_response(self, response: Response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            data=response.json()
            if data.get('status')!="OK":
                raise Exception(f"执行异常,{data.get('error')}")
            return data
        # 抛出代理错误
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    def register(self):
        if self.account.get('registed'):
            return
        def pre_register():
            if self.account.get('pre_registered'):
                return True
            logger.info(f'第{self.index}个地址----{self.wallet.address}--开始预注册')
            json_data = {
                'wallet_address': self.wallet.address,
            }
            try:
                response = self.session.post('https://points-mainnet.reddio.com/v1/pre_register', json=json_data)
                response.raise_for_status()
                if response.status_code == 200:
                    logger.success(f'第{self.index}个地址----{self.wallet.address}----预注册成功')
                    self.account['pre_registered']=True
                    self.config.save_accounts()
                    return True
            except Exception as error:
                time.sleep(1)
                logger.debug(
                    f"第{self.index}个地址----{self.wallet.address}----预注册异常{error}----{response.json()}")
                return False
        def connect_x():
            # if self.account.get('bind_x'):
            #     return True
            assert self.account.get('x_token'), 'x_token is empty'
            params = {
                'wallet_address': self.wallet.address,
            }
            response = self.session.get('https://points-mainnet.reddio.com/v1/login/twitter', params=params)
            url=response.json()['data']['url']
            xauth=XAuth(self.account.get('x_token'),self.proxies)
            oauth_token,redirect_uri=xauth.oauth2(url)
            resp2=self.session.get(redirect_uri)
            if resp2.status_code==200:
                logger.info(f'第{self.index}个地址----{self.wallet.address}-绑定x成功')
                self.account['bind_x']=True
                self.config.save_accounts()
                return True
            else:
                logger.error(f'第{self.index}个地址----{self.wallet.address}-绑定x失败')
                return False
        def registe():
            if self.account.get('registed'):
                return True
            json_data = {
                'wallet_address': self.wallet.address,
                'invitation_code': self.config.invite_code,
            }
            response = self.session.post('https://points-mainnet.reddio.com/v1/register', json=json_data)
            data=self._handle_response(response)
            logger.info(f'第{self.index}个地址----{self.wallet.address}-注册成功')
            self.account['registed']=True
            self.config.save_accounts()
        pre_register()
        connect_x()
        time.sleep(60)
        registe()
    def deploy(self):
        # if self.account.get('deployed'):
        #     return True
        compiled_contract=generate_random_erc20_contract()
        address=deploy_contract(self.web3,self.wallet,compiled_contract,(compiled_contract['total_supply'],),10)
        if address:
            logger.info(f'第{self.index}个地址----{self.wallet.address}-部署合约成功')
            self.account['deployed']=True
            self.config.save_accounts()
            return True
        else:
            logger.error(f'第{self.index}个地址----{self.wallet.address}-部署合约失败')
            return False
    def transfer_task(self):
        other_account=self.config.get_random_accounts(self.account)[0]
        to_address = other_account.get('address')
        current_gas_price = self.web3.eth.gas_price
        # 可根据需求动态估算
        amount = round(random.uniform(0.001, 0.005), 5)
        logger.info(f"{self.wallet.address}----转账金额是{amount}, 接收地址----{to_address}")
        amount_wei = self.web3.to_wei(amount, 'ether')
        transaction = {
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
            'from': self.wallet.address,
            'to': Web3.to_checksum_address(to_address) ,
            'chainId': self.config.chain_id,
            'gas': 3000000,  # Gas 限制
            'gasPrice':current_gas_price*10,
            'value': amount_wei,
        }
        try:
            tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash.hex())
            if receipt.status:
                logger.success(f'第{self.index}个地址----{self.wallet.address}-交易成功-{tx_hash.hex()}')
                return tx_hash
            else:
                logger.error(f'第{self.index}个地址----{self.wallet.address}-交易没有上链-{tx_hash.hex()}')
                return None
        except Exception as e:
            logger.error(f"第{self.index}个地址----{self.wallet.address}----交易失败: {e}")
            return None
    def faucet(self):
        headers = get_cf_waf(self.config.site,self.config.sitekey,method=self.config.cf_api_method,url=self.config.cf_api_url,authToken=self.config.cf_api_key)
        # 获取当前时间的毫秒级 Unix 时间戳
        timestamp_ms = int(time.time() * 1000)
        def encode(u, p):
            f = str(p)[2:5]
            x = u[5:9]
            v = f + "QOPL7548W" + x
            hash_object = hashlib.sha256(v.encode())
            return hash_object.hexdigest()
        u = self.wallet.address
        p = timestamp_ms
        random_hex = encode(u, p)
        json_data = {
            'address': self.wallet.address,
            'others': False,
            'time': timestamp_ms,
            'token': random_hex,
        }
        logger.info(f'第{self.index}个地址----{self.wallet.address}-开始领水')
        for j in range(3):
            response = None
            try:
                cookies = {
                    'cf_clearance': headers.get('cf_clearance'),
                }
                response = requests.post('https://testnet-faucet.reddio.com/api/claim/new', json=json_data,headers=headers,cookies=cookies)
                response.raise_for_status()
                logger.debug(response.json())
                if response.status_code == 200:
                    txHash = response.json().get('txHash')
                    logger.success(f'第{self.index}个地址----{self.wallet.address}-领水成功txHash--{txHash}')
                    return txHash
                if 'fully claiming' in str(response.text):
                    logger.warning(f"第{self.index}个地址----{self.wallet.address}----已领水")
                    return None
            except Exception as error:
                
                time.sleep(1)
                logger.debug(
                    f"第{self.index}个地址----{self.wallet.address}领水异常----重试第{j + 1}次中...{error}---{response.json()}")
        logger.error(f"第{self.index}个地址----{self.wallet.address}----领水失败")
        return None
    def get_user_info(self):
        params={
            'wallet_address': self.wallet.address,
        }
        response = self.session.get('https://points-mainnet.reddio.com/v1/userinfo',params=params)
        data=self._handle_response(response)
        userinfo=data.get('data',{})
        userinfo.pop('assets')
        self.account.update(userinfo)
        self.config.save_accounts()
        return userinfo
    def claim(self,task_uuid,daily=False):
        try:
            if not daily:
                if self.account.get(f'task_{task_uuid}'):
                    return True
            json_data = {
                'wallet_address': self.wallet.address,
                'task_uuid': task_uuid,
            }
            response = self.session.post('https://points-mainnet.reddio.com/v1/points/verify',json=json_data)
            
            data=self._handle_response(response)
            logger.info(f'第{self.index}个地址----{self.wallet.address}-任务完成')
            if not daily:
                self.account[f'task_{task_uuid}']=True
                self.config.save_accounts()
        except Exception as e:
            logger.error(f"第{self.index}个地址----{self.wallet.address}----任务失败:{e}")
            return False
    def claim_all(self):
        for task_uuid in self.daily_task_list.values():
            
            self.claim(task_uuid,True)
        for task_uuid in self.once_task_list.values():
            self.claim(task_uuid)

class ReddioBotManager(BaseBotManager):
    def run_single(self,account):
        bot=ReddioBot(account,self.web3,self.config)
        bot.register()
    
        try:
            bot.faucet()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},领取失败,{e}")
        time.sleep(60)
        try:
            bot.get_user_info()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},获取用户信息失败,{e}")
        try:
            bot.transfer_task()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},转账失败,{e}")
        try:
            bot.deploy()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},部署失败,{e}")
        try:
            bot.get_user_info()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},获取用户信息失败,{e}")
    def verify(self,account):
        bot=ReddioBot(account,self.web3,self.config)
        try:
            bot.claim_all()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},任务失败,{e}")
    def verify_all_task(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.verify, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.exception(f"执行过程中发生错误: {e}")
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.exception(f"执行过程中发生错误: {e}")

