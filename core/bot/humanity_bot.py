import os
import sys
import time
from DrissionPage import Chromium,ChromiumOptions
from core.extensions.OKXWallet import login_with_private_key
from loguru import logger
from faker import Faker
from random import randint
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.utils import EmailOauth2Sync
from core.bot.basebot import *

class HumanityBot(BaseBot):
    def _handle_response(self, response: requests.Response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            data=response.json()
            return data
        # 抛出代理错误
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    def login(self,tab,wallet_tab):
        try:
            tab.get(f'https://testnet.humanity.org/login?ref={self.config.invite_code}')
            tab.ele('@@tag():button@@text():Connect Wallet',timeout=120).click()
            tab.ele('@@tag():button@@text():MetaMask').click()
            logger.info(f'{self.wallet.address},开始连接钱包')
            wallet_tab.ele('@@tag():button@@text():连接',timeout=120).click()
            time.sleep(5)
            tab.ele('@@tag():button@@text():发送消息',timeout=120).click()
            time.sleep(1)
            wallet_tab.ele('xpath:/html/body/div[1]/div/div/div/div/div/div[4]/div/button[2]',timeout=120).click()
            logger.success(f'{self.wallet.address},连接钱包成功')
            time.sleep(5)
        except Exception as e:
            logger.error(e)
            return False
        return True


    def register(self,tab):
        assert self.account.get('email'),'邮箱不能为空'
        assert self.account.get('email_password'),'邮箱password不能为空'
        email = self.account.get('email')
        email_password = self.account.get('email_password')
        try:
            already_registered = tab.ele('@@tag():p@@text():Loading your profile...')
            if already_registered:
                logger.success('已经注册成功')
                tab.close()
                return True
            faker = Faker()
            num  = str(randint(999,9999))
            firstName = faker.first_name()
            lastName = faker.last_name()
            humanId =firstName+num+lastName
            human_id = tab.ele('@@tag():input@@id=identification.hp_username')
            if human_id:
                human_id.clear()
                human_id.input(humanId)
                time.sleep(2)
            tab.ele('@@tag():button@@text():Next',timeout=300).click()
            logger.info('设置humanID成功')

            first_name = tab.ele('@id=profile.first_name')
            if first_name:
                first_name.clear()
                first_name.input(firstName)
            last_name = tab.ele('@id=profile.last_name')
            if last_name:
                last_name.clear()
                last_name.input(lastName)
            time.sleep(1)
            
            email_address = tab.ele('xpath://*[@id="profile.email_address"]')
            if email_address:
                email_address.clear()
                email_address.input(email)
                time.sleep(random.random())

            confirm_email = tab.ele('xpath://*[@id="profile.confirm_email"]')
            if confirm_email:
                confirm_email.clear()
                confirm_email.input(email)
                time.sleep(random.random())
            next = tab.ele('@@tag():button@@text():Next')
            if next:
                next.click()
            check = tab.ele('@@tag():p@@text():Please enter the code sent to',timeout=120)
            if check:
                time.sleep(3)
                logger.info(f'{self.wallet.address},开始获取验证码')
                mail=EmailOauth2SyncByPassWord(email,email_password)
                body,code = mail.listening_unsee_mails(get_code=True)
                logger.info(f'{self.wallet.address},获取验证码成功,code:{code}')
                if code:    
                    logger.info('获取验证码成功')
                    inputs = tab.eles('xpath:.//div[contains(@class, "MuiInputBase-root")]//input')

                    for i, input in enumerate(inputs):
                        input.clear()  # 如果需要清空现有值
                        input.input(code[i])
                        time.sleep(0.1) 
                    logger.info('注册使用的邮箱输入成功')
                else:
                    logger.info('使用验证码失败')   
                    return False
            else:
                logger.info('获取验证码失败')
                return False
            # vf = tab.ele('xpath:/html/body/div[1]/div/div[2]/div/div[5]/div/div[3]')
            # if vf:
            #     vf.click()
            return True
        except Exception as e:
            logger.exception(e)
            return False


    def register_work(self):
        if self.account.get('register'):
            logger.info(f'{self.wallet.address},已经注册成功')
            return True
        try:
            co = ChromiumOptions()
            co.auto_port()
            #添加插件（path放路径）
            co.add_extension(
                path=r"extension/okxWallet/3.37.0_1")
            co.add_extension(path=self.config.proxy_auth_plugin_path)
            # co.headless(True)
            co.set_user_agent(self.ua.chrome)
            #配置浏览器信息
            browser = Chromium(addr_or_opts=co)
            #加载浏览器插件时间
            time.sleep(10)

            #钱包的标签页
            tab1 = browser.new_tab()
            browser.close_tabs(tab1, True)
            logger.info('关闭弹出页面')

            #使用私钥导入okx钱包
            wallet_login = login_with_private_key(private_key=self.account.get('private_key'),page_info=tab1)
            if not wallet_login:
                browser.quit()
                return False

            #项目页面的标签页
            tab2 = browser.new_tab()
            #实现humanity的登陆
            connect = self.login(tab=tab2,wallet_tab=tab1)
            if not connect:
                browser.quit()
                return False
            register_vf = self.register(tab= tab2)
            if not register_vf:
                browser.quit()
                return False
            browser.quit()
            logger.success(f'{self.wallet.address},注册成功')
            self.account['register'] = True
            self.config.save_accounts()

        except Exception as e:
            logger.exception(e)
            return False
    #使用okx钱包登陆项目
    def checkin(self):
        if not self.account.get('faucet'):
            logger.warning(f'{self.wallet.address},未领取faucet')
            return
        contract_address = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
        contract_abi = [{"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"bufferSafe","type":"bool"}],"name":"ReferralRewardBuffered","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"enum IRewards.RewardType","name":"rewardType","type":"uint8"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cycleStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vcContract","type":"address"},{"internalType":"address","name":"tkn","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"startTimestamp","type":"uint256"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]  # Place the ABI here
        contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        gas_amount = contract.functions.claimReward().estimate_gas({
            'chainId': self.web3.eth.chain_id,
            'from': self.wallet.address,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address)
        })
        transaction = contract.functions.claimReward().build_transaction({
            'chainId': self.web3.eth.chain_id,
            'from': self.sender_address,
            'gas': gas_amount,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address)
        })
        tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash.hex())
        if receipt.status:
            logger.success(f'第{self.index}个地址----{self.wallet.address}-签到成功-{tx_hash.hex()}')
            return tx_hash
        else:
            logger.error(f'第{self.index}个地址----{self.wallet.address}-签到失败-{tx_hash.hex()}')
            return None
    def get_faucet(self):
        address=self.wallet.address
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
            'Origin': 'https://faucet.testnet.humanity.org',
            'Pragma': 'no-cache',
            'Referer': 'https://faucet.testnet.humanity.org/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'address': address,
        }

        response = self.session.post('https://faucet.testnet.humanity.org/api/claim', headers=headers, json=json_data)
        data=self._handle_response(response)
        if 'Txhash' not in str(data):
            logger.error(f'{self.wallet.address},获取faucet失败,{data}')
            return False
        else:
            logger.success(f'{self.wallet.address},获取faucet成功,{data}')
            if not self.account.get('faucet'):
                self.account['faucet'] = True
                self.config.save_accounts()
            return True

class HumanityManager(BaseBotManager):
    def run_single(self,account):
       bot=HumanityBot(account,self.web3,self.config)
       bot.register_work()
       bot.get_faucet()
       time.sleep(10)
       bot.checkin()
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.exception(f"执行过程中发生错误: {e}")


# if __name__ == '__main__':
#     #线程池线程数（建议按照资源尝试修改，默认为单线程）
#     max_workers = 1
#     #账号信息的文件访问（需要修改为自己的文件路径）
#     tasks = pd.read_csv('account.csv').to_dict('records')
#     concurrent_e(tasks, max_workers, work)