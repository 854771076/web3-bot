from core.bot.basebot import *


class ReddioBot(BaseBot):
    
    def transfer_task(self):
        other_account=self.config.get_random_accounts(self.account)[0]
        to_address = other_account.get('address')
        current_gas_price = self.web3.eth.gas_price
        max_gas_price = self.web3.to_wei(3.5, 'gwei')
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
            'gasPrice': min(current_gas_price, max_gas_price),
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

class ReddioBotManager(BaseBotManager):
    def run_single(self,account):
        bot=ReddioBot(account,self.web3,self.config)
        try:
            bot.faucet()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},领取失败,{e}")
        time.sleep(60)
        try:
            bot.transfer_task()
        except Exception as e:
            logger.error(f"账户:{bot.wallet.address},转账失败,{e}")
        
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")

