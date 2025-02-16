import requests
from loguru import logger
import time
from functools import *
from typing import *
from urllib.parse import urlparse, parse_qs

from loguru import logger
from fake_useragent import UserAgent
from web3 import Web3
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from eth_account.messages import encode_defunct
from threading import Lock
from functools import *
from eth_account.signers.local import LocalAccount
import jwt
from apscheduler.schedulers.blocking import BlockingScheduler
from curl_cffi.requests import Session
import json
import hashlib
import random
from ratelimit import limits, sleep_and_retry
REQUESTS_PER_SECOND = 10
ONE_SECOND = 1
def send_transaction(web3,transaction,private_key):
    signed_tx = web3.eth.account.sign_transaction(transaction,private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    except Exception as e:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    except Exception as e:
        logger.error(e)
    return tx_hash

def get_sign(web3,private_key, msg):
    # 账户信息
    # 使用web3.py编码消息
    message_encoded = encode_defunct(text=msg)
    # 签名消息
    signed_message = web3.eth.account.sign_message(
        message_encoded, private_key=private_key
    ).signature.hex()
    if '0x' not in signed_message:
        signed_message = '0x' + signed_message
    # 打印签名的消息
    return signed_message
# 写一个函数检查jwttoken的过期时间
def check_jwt_exp(token):
    if not token:
        return False
    # 解析JWT
    payload = jwt.decode(token, options={"verify_signature": False})
    # 获取过期时间
    exp = payload.get('exp')
    # 当前时间
    now = int(time.time())
    # 检查过期时间
    if exp and exp < now:
        return False
    return True
def check_exp( login_time,expire_time=60*60*5):
    
    if not login_time:
        return False
    login_time=float(login_time)
    now = int(time.time())
    # 检查过期时间
    if login_time and login_time + expire_time < now:
        return False
    return True
def parse_url_params(url):
    """
    解析给定的 URL 中的 GET 参数，并返回一个字典。
    
    :param url: 包含 GET 参数的 URL
    :return: 字典形式的 GET 参数
    """
    # 解析 URL
    parsed_url = urlparse(url)
    # 解析 GET 参数
    params = parse_qs(parsed_url.query)
    
    # 将值从列表转换为单个值
    return {key: value[0] for key, value in params.items()}
class XAuth:
    TWITTER_AUTHORITY = "twitter.com"
    TWITTER_ORIGIN = "https://twitter.com"
    TWITTER_API_BASE = "https://twitter.com/i/api/2"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    AUTHORIZATION = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    MAX_RETRIES = 3
    RETRY_INTERVAL = 1
    ACCOUNT_STATE = {
        32: "Bad Token",
        64: "SUSPENDED",
        141: "SUSPENDED",
        326: "LOCKED"
    }
    def __init__(self, auth_token: str,proxies=None):
        """初始化XAuth实例"""
        self.auth_token = auth_token
        self.session = self._create_session()
        self.session2 = self._create_session(include_twitter_headers=False)
        if proxies:
            self.session.proxies.update(proxies)
            self.session2.proxies.update(proxies)
    def _create_session(self, include_twitter_headers: bool = True) -> requests.Session:
        """创建配置好的requests session"""
        session = requests.Session()
        
        # 设置基础headers
        headers = {
            "user-agent": self.USER_AGENT
        }
        
        if include_twitter_headers:
            headers.update({
                "authority": self.TWITTER_AUTHORITY,
                "origin": self.TWITTER_ORIGIN,
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-active-user": "yes",
                "authorization": self.AUTHORIZATION
            })
        
        session.headers.update(headers)
        session.cookies.set("auth_token", self.auth_token)
        
        return session
    def _handle_response(self, response: requests.Response, retry_func=None) -> None:
        """处理响应状态"""
        if response.status_code == 429:  # Too Many Requests
            time.sleep(self.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
            response.raise_for_status()
        
    def get_twitter_token(self, oauth_token: str) -> str:
        """获取Twitter认证token"""
        if not oauth_token:
            raise ValueError("oauth_token不能为空")
        params = {"oauth_token": oauth_token}
        response = self.session2.get("https://api.x.com/oauth/authenticate", params=params)
        self._handle_response(response)
        
        content = response.text
        
        if "authenticity_token" not in content:
            if "The request token for this page is invalid" in content:
                raise ValueError("请求oauth_token无效")
            raise ValueError("响应中未找到authenticity_token")
        # 尝试两种可能的token格式
        token_markers = [
            'name="authenticity_token" value="',
            'name="authenticity_token" type="hidden" value="'
        ]
        
        token = None
        for marker in token_markers:
            if marker in content:
                token = content.split(marker)[1].split('"')[0]
                break
                
        if not token:
            raise ValueError("获取到的authenticity_token为空")
        return token
    def oauth1(self, oauth_token: str) -> str:
        """执行OAuth1认证流程"""
        authenticity_token = self.get_twitter_token(oauth_token)
        
        data = {
            "authenticity_token": authenticity_token,
            "oauth_token": oauth_token
        }
        
        response = self.session2.post("https://x.com/oauth/authorize", data=data)
        self._handle_response(response)
        
        content = response.text
        
        if "oauth_verifier" not in content:
            if "This account is suspended." in content:
                raise ValueError("该账户已被封禁")
            raise ValueError("未找到oauth_verifier")
            
        verifier = content.split("oauth_verifier=")[1].split('"')[0]
        if not verifier:
            raise ValueError("获取到的oauth_verifier为空")
            
        return verifier
    def get_auth_code(self, params: Dict[str, str]) -> str:
        """获取认证码"""
        if not params:
            raise ValueError("参数不能为空")
        def retry():
            return self.get_auth_code(params)
        response = self.session.get(f"{self.TWITTER_API_BASE}/oauth2/authorize", params=params)
        self._handle_response(response, retry)
        data = response.json()
        
        # 处理CSRF token
        if data.get("code") == 353:
            ct0 = response.cookies.get("ct0")
            if ct0:
                self.session.headers["x-csrf-token"] = ct0
                return self.get_auth_code(params)
            raise ValueError("未找到ct0 cookie")
        # 检查错误
        if "errors" in data and data["errors"]:
            error_code = data["errors"][0].get("code")
            if error_code in self.ACCOUNT_STATE:
                raise ValueError(f"token状态错误: {self.ACCOUNT_STATE[error_code]}")
        auth_code = data.get("auth_code")
        if not auth_code:
            raise ValueError("响应中未找到auth_code")
            
        return auth_code
    def oauth2(self,url) -> str:
        """执行OAuth2认证流程"""
        params=parse_url_params(url)
        auth_code = self.get_auth_code(params)
        
        data = {
            "approval": "true",
            "code": auth_code
        }
        
        def retry():
            return self.oauth2(params)
        response = self.session.post(f"{self.TWITTER_API_BASE}/oauth2/authorize", data=data)
        self._handle_response(response, retry)
        if  "redirect_uri" not in response.text:
            raise ValueError("响应中未找到redirect_uri")
        return auth_code
@sleep_and_retry
@limits(calls=REQUESTS_PER_SECOND, period=ONE_SECOND)
def get_cf_token(site,siteKey,method="turnstile-min",url='http://127.0.0.1:3000',authToken=None):
    if authToken:
        data = {
            "url": site,
            "siteKey": siteKey,
            "mode": method,
            "authToken": authToken
        }
    else:
        data = {
            "url": site,
            "siteKey": siteKey,
            "mode": method
        }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        logger.success(f"请求cf_token成功")
        return result["token"]
    except requests.RequestException as e:
        logger.exception(f"请求过程中发生错误: {e}")
#计算该时间戳1739267133秒后距离现在的时间是否有24小时
@sleep_and_retry
@limits(calls=REQUESTS_PER_SECOND, period=ONE_SECOND)
def get_cf_waf(site,siteKey,method="waf-session",url='http://127.0.0.1:3000',authToken=None):
    if authToken:
        data = {
            "url": site,
            "siteKey": siteKey,
            "mode": method,
            "authToken": authToken
        }
    else:
        data = {
            "url": site,
            "siteKey": siteKey,
            "mode": method
        }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        logger.success(f"请求cf_waf成功")
        headers = result.get('headers', {})
        headers["Cookie"] = "; ".join(
            [
                f"{cookie['name']}={cookie['value']}"
                for cookie in result["cookies"]
            ]
        )
        return headers
    except Exception as e:
        logger.exception(f"请求过程中发生错误: {e}")
        return None
def is_24_hours_away(timestamp):
    if not timestamp:
        return True
    current_time = time.time()
    time_difference =  current_time-timestamp
    if time_difference >= 24 * 60 * 60:
        return True
    else:
        return False
    
if __name__ == "__main__":
    timestramp=1739261163
    print(is_24_hours_away(timestramp))