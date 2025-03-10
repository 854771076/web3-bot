from core.bot.basebot import *
from core.config import Config
from threading import Lock
lock=Lock()

#实例化以上合约
class AxieinfinityBot(BaseBot):
    def _handle_response(self, response, retry_func=None) -> None:
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
    
    def resolve_captcha(self):
        """
        解析验证码
        """
        json_data = {
        'app_key': '889a9cb7-3ffa-4113-9e3f-36558fe19808',
        }
        session=Session(
            proxies=self.proxies,
            headers=self.headers,
            impersonate="chrome99",
            verify=False,
            timeout=600,
            http_version=3
        )
        session.headers.update({'User-Agent': self.ua.chrome})
        response = session.post('https://x.skymavis.com/captcha-srv/check', json=json_data)
        if response.json().get('id'):
            json_data = {
                'app_key': '889a9cb7-3ffa-4113-9e3f-36558fe19808',
                'id': response.json().get('id'),
                'result': 30,
            }
            response = session.post('https://x.skymavis.com/captcha-srv/submit', json=json_data)
            if response.json().get('token'):

                logger.info(f"index:{self.index}-{self.wallet.address}-解析验证码成功")
                self.session.headers.update({
                    'x-captcha': response.json().get('token'), 
                })
                return True
            else:
                time.sleep(0.1)
                logger.warning(f"index:{self.index}-{self.wallet.address}-解析验证码失败,{response.text},重试中...")
        else:
            time.sleep(0.1)
            logger.warning(f"index:{self.index}-{self.wallet.address}-解析验证码失败,{response.text},重试中...")
    def login(self):
        """
        登录
        """
        if self.account.get('accessKey'):
            self.session.headers.update({
                'authorization': f'Bearer {self.account.get("accessKey")}',
            })
            logger.info(f"index:{self.index}-{self.wallet.address}-登录成功")
            return
        timestamp=int(time.time())
        address=str(self.wallet.address).lower()
        msg=f"{address}\nWelcome to Axie Infinity: Atia's Legacy!\n{timestamp}"
        json_data = {
            'query': '\n  mutation PreRegisterWithWallet(\n    $signature: String!\n    $referredBy: String\n    $timestamp: Int!\n    $userAddress: String!\n  ) {\n    atiaLegacyPreregisterWithWallet(\n      signature: $signature\n      timestamp: $timestamp\n      referredBy: $referredBy\n      userAddress: $userAddress\n    ) {\n      accessKey\n      registered\n    }\n  }\n',
            'variables': {
                'signature': get_sign(self.web3,self.wallet.key,msg),
                'userAddress': address,
                'referredBy': self.config.invite_code,
                'timestamp': timestamp,
            },
        }

        response = self.session.post('https://graphql-gateway.axieinfinity.com/graphql', json=json_data)
        data=self._handle_response(response)

        token=data.get('data',{}).get('atiaLegacyPreregisterWithWallet',{}).get('accessKey')
        if token:
            self.session.headers.update({
                'authorization': f'Bearer {token}',
            })
            self.account.update({
                'accessKey':token, 
            })

        # userinfo=data.get('data',{}).get('atiaLegacyUserRank',{}).pop('userProfile')
        # userinfo={**data.get('data',{}).get('atiaLegacyUserRank',{}),**userinfo}
        # self.account.update(userinfo)
        logger.info(f"index:{self.index}-{self.wallet.address}-登录成功")
        self.config.save_accounts()

class AxieinfinityManager(BaseBotManager):
    def run_single(self,account):
        bot=AxieinfinityBot(account,self.web3,self.config)
        status=None
        while not status:
            try:
                status=bot.resolve_captcha()
            except Exception as e:
                logger.error(f"{e}")
        bot.login()
        
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.exception(f"执行过程中发生错误: {e}")

    