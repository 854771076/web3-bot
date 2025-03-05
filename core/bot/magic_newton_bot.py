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
    # ...

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
