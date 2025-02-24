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
            raise Exception(f"请求过程中发生错误,{e}")
    def register(self):
        def connect_x():
            if self.account.get('bind_x'):
                return True
            assert self.account.get('x_token'), 'x_token is empty'
            params = {
                'wallet_address': self.wallet.address,
            }
            response = self.session.get('https://points-mainnet.reddio.com/v1/login/twitter', params=params,impersonate='chrome')
            url=response.json()['data']['url']
            xauth=XAuth(self.account.get('x_token'),self.proxies)
            oauth_token,resp=xauth.oauth2(url)
            url2=resp.json()['redirect_uri']
            resp2=self.session.get(url2)
            if resp2.status_code==200:
                logger.info(f'第{self.index}个地址----{self.wallet.address}-绑定x成功')
                self.account['bind_x']=True
                self.config.save_account(self.account)
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
            self.config.save_account(self.account)
        connect_x()
        registe()
    def deploy(self):
        if self.account.get('deployed'):
            return True
        abi=[{'inputs': [], 'name': 'get', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'x', 'type': 'uint256'}], 'name': 'set', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'storedData', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}]
        bytecode='608060405234801561001057600080fd5b50610176806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80632a1afcd91461004657806360fe47b1146100645780636d4ce63c14610080575b600080fd5b61004e61009e565b60405161005b9190610104565b60405180910390f35b61007e600480360381019061007991906100cc565b6100a4565b005b6100886100ae565b6040516100959190610104565b60405180910390f35b60005481565b8060008190555050565b60008054905090565b6000813590506100c681610129565b92915050565b6000602082840312156100de57600080fd5b60006100ec848285016100b7565b91505092915050565b6100fe8161011f565b82525050565b600060208201905061011960008301846100f5565b92915050565b6000819050919050565b6101328161011f565b811461013d57600080fd5b5056fea26469706673582212200a619673ab087c57fedf007294664d469ba61b7441a0b5f17910cfeb09b98f7964736f6c63430008000033'
        compiled_contract={
            "abi":abi,
            "bytecode":bytecode
        }
        deploy_contract(self.web3,self.account,compiled_contract,100)
        logger.info(f'第{self.index}个地址----{self.wallet.address}-部署合约成功')
        self.account['deployed']=True
        self.config.save_account(self.account)
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
            'gas': 21000,  # Gas 限制
            'gasPrice':current_gas_price*100,
            'value': amount_wei,
        }
        try:
            tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
            if '0x' not in str(tx_hash.hex()):
                tx_hash_formatted = '0x' + tx_hash.hex()
            else:
                tx_hash_formatted = tx_hash.hex()
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status:
                logger.success(f'第{self.index}个地址----{self.wallet.address}-交易成功-{tx_hash_formatted}')
                return tx_hash_formatted
            else:
                logger.error(f'第{self.index}个地址----{self.wallet.address}-交易没有上链-{tx_hash_formatted}')
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
    def claim(self,task_uuid,daily=False):
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
            self.config.save_account(self.account)
    def claim_all(self):
        for task_uuid in self.daily_task_list.values():
            self.claim(task_uuid,True)
        for task_uuid in self.once_task_list.values():
            self.claim(task_uuid)

class ReddioBotManager(BaseBotManager):
    def run_single(self,account):
        bot=ReddioBot(account,self.web3,self.config)
        try:
            bot.register()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},注册失败,{e}")
        try:
            bot.faucet()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},领取失败,{e}")
        time.sleep(60)
        try:
            bot.transfer_task()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},转账失败,{e}")
        try:
            bot.claim_all()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},任务失败,{e}")
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")

