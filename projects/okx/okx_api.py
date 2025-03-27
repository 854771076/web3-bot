
from fake_useragent import UserAgent
from loguru import logger
from web3 import Web3
from loguru import logger
from eth_account.messages import encode_defunct
import time
import requests
import hashlib
import hmac
import base64
import json
import uuid
import time
from twocaptcha import TwoCaptcha
def generate_auth_params(url, fetch_config=None, timestamp_for_test=None, token_for_test=None):
    fetch_config = fetch_config or {}
    method = fetch_config.get('method', 'GET').upper()
    body = fetch_config.get('body', '')

    # 生成token
    token = token_for_test if token_for_test is not None else str(uuid.uuid4())

    # 计算HMAC密钥和时间戳
    def compute_hmac_key(t):
        digest = hashlib.sha256(t.encode('utf-8')).digest()
        hex_str = ''.join(f"{byte:02x}" for byte in digest)
        
        current_ts = timestamp_for_test if timestamp_for_test is not None else int(time.time() * 1000)
        u = current_ts // 1000
        
        s = (u // 600) % 32
        l = (u // 3600) % 32
        key_str = ''.join([hex_str[(s + (l + f) * f) % 32] for f in range(32)])
        
        return {
            'key': key_str.encode('utf-8'),
            'timestamp': current_ts
        }

    def build_signing_string():
        base_url = url.split('?')[0] if '?' in url else url
        if method in ['POST', 'PUT']:
            return f"{base_url}{body}".replace(" ", "")
        return url.replace('?', '')

    key_data = compute_hmac_key(token)
    signing_msg = build_signing_string()
    hmac_sign = hmac.new(
        key_data['key'],
        signing_msg.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    return {
        'ok-verify-token': token,
        'ok-timestamp': str(key_data['timestamp']),
        'ok-verify-sign': base64.b64encode(hmac_sign).decode('utf-8')
    }

class OKXSession(requests.Session):
    def __init__(self, timestamp_for_test=None, token_for_test=None):
        super().__init__()
        self.timestamp_for_test = timestamp_for_test
        self.token_for_test = token_for_test

    def request(self, method, url, **kwargs):
        # 获取现有的headers
        headers = kwargs.get('headers', {})
        # 构建fetch_config
        method = method.upper()
        body = ''
        if method in ['POST', 'PUT']:
            if 'data' in kwargs:
                body = kwargs['data']
            elif 'json' in kwargs:
                import json
                body = json.dumps(kwargs['json'])
        fetch_config = {
            'method': method,
            'body': body
        }
        # 生成auth_params
        auth_params = generate_auth_params(
            url,
            fetch_config,
            self.timestamp_for_test,
            self.token_for_test
        )
        # 更新headers
        headers.update(auth_params)
        # 将更新后的headers放回kwargs
        kwargs['headers'] = headers
        # 调用父类的request方法
        return super().request(method, url, **kwargs)
class OkxDrop:
    def __init__(self,shortActivityName,twocaptcha_key=None,proxy=None):
        if proxy:
            self.proxies={
                "http":proxy,
                "https":proxy
            }
        else:
            self.proxies=None
        ua=UserAgent()
        self.solver = TwoCaptcha(twocaptcha_key)
        self.session=OKXSession()
        self.session.headers.update({
            "User-Agent":ua.chrome,
        })
        self.session.proxies=self.proxies
        self.shortActivityName=shortActivityName
        self._init_session()
        self.info=self.get_activity_info()
    def _init_session(self):
        url=f'https://web3.okx.com/zh-hans/marketplace/drops/event/{self.shortActivityName}'
        self.session.get(url)

    @property
    def timestramp(self):
        now = time.time() * 1000  # 获取当前时间的时间戳（毫秒）
        return str(int(now))
    def _handle_response(self, response: requests.Response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            data=response.json().get('data')
            if not data:
                logger.error(f"执行异常,{response.text}")
                return None
            return data
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    def get_winner(self,pageSize=100):
        url='https://web3.okx.com/priapi/v1/nft/primary/subscribed/subscribeUser'
        pageNum=1
        id=self.info.get('id')
        winSubscribePublicTime=self.info.get('winSubscribePublicTime')/1000
        now=time.time()
        total=self.info.get('list',[{}])[0].get('nftList',[{}])[0].get('total')
        winner_list=[]
        if now>winSubscribePublicTime:
            while len(winner_list)!=total:
                params={
                    'activityId':id,
                    'pageNum':pageNum,
                    'pageSize':pageSize,
                    't':self.timestramp
                }
                resp=self.session.get(
                    url,params=params
                )
                data=self._handle_response(resp)
                if data:
                    winner=list(filter(lambda x:x.get('success'),data.get('userInfoDTOS',[]) if data else []))
                    winner_list.extend(winner)
                    pageNum+=1
                    if not data.get('hasNext'):
                        break
                else:break
            return winner_list
        else:
            logger.warning(f'drop:{self.shortActivityName} winner not ready')
    def get_activity_list(self):pass
    def get_activity_info(self):
        params={
            "shortActivityName":self.shortActivityName,
            't':self.timestramp
        }
        url='https://web3.okx.com/priapi/v1/nft/primary/activity-detail'
        resp=self.session.get(
            url,params=params
        )
        data=self._handle_response(resp)
        if data:
            return data
        logger.warning(f'get_activity_info failed,resp:{resp.text}')
        return None
    def get_activity_info_detail(self,address,receivingAddress):
        params={
            "shortActivityName":self.shortActivityName,
            "address":address,
            "receivingAddress":receivingAddress,
            't':self.timestramp
        }
        url='https://web3.okx.com/priapi/v1/nft/primary/activity-detail'
        resp=self.session.get(
            url,params=params
        )
        data=resp.json()
        if data.get('data'):
            return data.get('data')
        logger.warning(f'get_activity_info failed,resp:{resp.text}')
        return None
    def get_subscribe_task(self,walletAddress):
        url='https://web3.okx.com/priapi/v1/nft/primary/subscribed/getSubscribeTask'
        params={
            'activityId':self.info.get('id'),
            'walletAddress':walletAddress,
            't':self.timestramp
        }
        resp=self.session.get(
            url,params=params 
        )
        data=self._handle_response(resp)
        subscribeTasks=data.get('subscribeTasks',[]) if data else []
        if subscribeTasks:
            subscribeTaskInfos=[]
            for task in subscribeTasks:
                subscribeTaskInfos.extend(task.get('subscribeTaskInfos'))
            return subscribeTaskInfos
        logger.warning(f'get_subscribe_task failed,resp:{resp.text}')
    #https://web3.okx.com/priapi/v1/nft/primary/subscribed/getInfo?activityId=11565&walletAddress=0x72691a36ed1fac3b197fb42612dc15a8958bf9f2&t=1742972712066
    def get_info(self,walletAddress):
        url='https://web3.okx.com/priapi/v1/nft/primary/subscribed/getInfo'
        params={
            'activityId':self.info.get('id'),
            'walletAddress':walletAddress,
            't':self.timestramp
        }
        resp=self.session.get(
            url,params=params 
        )
        data=self._handle_response(resp)
        return data
    def get_sign(self,address):
        url='https://web3.okx.com/priapi/v1/nft/user/sign'
        params={
            'address':address,
            't':self.timestramp, 
        }
        resp=self.session.get(
            url,params=params 
        )
        data=self._handle_response(resp)
        return data
    def login(self,web3,address,private_key,chainType=60):
        signData=self.get_sign(address).get('signData')
        message_encoded = encode_defunct(text=signData)
        # 签名消息
        signed_message = web3.eth.account.sign_message(
            message_encoded, private_key=private_key,
        ).signature.hex()
        if '0x' not in signed_message:
            signed_message = '0x' + signed_message
        json_data = {
            'account': address,
            'signature': signed_message,
            'chainType': chainType,
            'address': address,
            'algorithmCode': '',
        }
        params={
            't': self.timestramp,
        }
        response = self.session.post('https://web3.okx.com/priapi/v1/nft/user/login', params=params, json=json_data)
        data=self._handle_response(response)
        token=data.get('token')
        if token:
            self.session.headers.update({
                'nft_token' : token
            })
        else:
            logger.warning(f'login failed,resp:{response.text}')
        return data
    def oauth2Url(self,address,platform=1,domainType=0):
        params = {
            't': self.timestramp,
        }
        json_data = {
            'walletAddress': address,
            'platform': platform,
            'activityId': self.info.get('id'),
            'domainType': domainType,
        }
        response = self.session.post('https://web3.okx.com/priapi/v1/nft/oauth2/oauth2Url', params=params, json=json_data)
        print(response.headers)
        logger.info(f'oauth2Url,resp:{response.text}')
        return response.text
    def oauth2Url2(self,address,platform=1,domainType=0,appid='f8553adb1e94368c52b9617f669a0227'):
        params = {
            'pt': '1',
            'app_id': 'f8553adb1e94368c52b9617f669a0227',
        }

        data = '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83911c12d39442c486f379beba5fe532947c106e2a197fa60f3787cea3ba458b0ca6dcff6f2bf7f0ec2939ce06cac715c141138a3995f8cdf2f1511927141f51d1a515362546bae025d9d8e87d8630590a49919f615709f65702df403c66778795ee4b6a07b45aec5e2bc5cd23ca7e7c0c974ffa1d140ef16afefb87bb5529a7'

        response = requests.post('https://dkapi-ga.geetest.com/deepknow/v2/judge', params=params, data=data)
        logger.info(f'judge,resp:{response.text}')
        sessionId=response.json().get('session_id')
        fingerprint_id=response.json().get('fingerprint_id')
        params = {
            't': self.timestramp,
        }
        devid=str(uuid.uuid4())
        self.session.headers.update({
            'devid':devid
        })
        
        json_data = {
            'scene': 'okex_highrisk',
            'sessionId': sessionId,
        }
        self.session.cookies.update({
            appid:sessionId
        })
        self.oauth2Url(address,platform,domainType)
        response = self.session.post('https://web3.okx.com/v3/users/support/jiyanDeepKnow', params=params, json=json_data)
        logger.info(f'jiyanDeepKnow,resp:{response.text}')
        challenge=response.json().get('data',{}).get('challenge')
        params = {
            't': self.timestramp,
        }
        result = self.solver.geetest_v4(captcha_id='6ba6b71b4f3958a1c69ad839ba47836b',
                      url='https://web3.okx.com/priapi/v1/nft/oauth2/oauth2Url',  
                      challenge=challenge)
        logger.info(f'get_captcha_result,result:{result}')
        data=json.loads(result.get('code'))
        validateParam={
            'lotNumber': data.get('lot_number'),
            'captchaOutput': data.get('captcha_output'),
            'passToken': data.get('pass_token'),
            'genTime': data.get('gen_time'),
            'scene': 'okex_highrisk',
        }
        json_data = {
            'walletAddress': address,
            'platform': platform,
            'activityId': self.info.get('id'),
            'domainType': domainType,
            'validateParam': validateParam
        }
        response = self.session.post('https://web3.okx.com/priapi/v1/nft/oauth2/oauth2Url', params=params, json=json_data)
        logger.info(f'oauth2Url,resp:{response.text}')
        return response.text
    
if __name__=='__main__':
    drop=OkxDrop('onegravity','xxx')
    # data=drop.get_winner()
    # print(data)
    # data=drop.get_sign('0x72691a36ed1fac3b197fb42612dc15a8958bf9f2')
    # print(data)
    # data=drop.get_info('0x72691a36ed1fac3b197fb42612dc15a8958bf9f2')
    # print(data)
    # data=drop.get_subscribe_task('0x72691a36ed1fac3b197fb42612dc15a8958bf9f2')
    # print(data)
    web3=Web3(Web3.HTTPProvider('wallet.okex.org/fullnode/base/discover/rpc'))
    if web3.is_connected():print(web3.eth.chain_id)
    address='0xxxx'
    private_key='0xxxx'
    print(drop.login(web3,address,private_key))
    # drop.oauth2Url(address)
    drop.oauth2Url2(address)
    