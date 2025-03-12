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
import email
import email.header
import imaplib
import re
from email.header import decode_header
from datetime import datetime
import urllib
import re,os
from faker import Faker
REQUESTS_PER_SECOND = 10
ONE_SECOND = 1
from solcx import compile_standard, install_solc
from solcx import compile_source
import random
import string
from web3 import Web3
from web3.exceptions import ContractLogicError
import requests
from loguru import logger
from eth_account.messages import encode_defunct
from datetime import datetime
def deploy_check_in_contract():
    """
    部署一个签到合约到以太坊网络
    :param web3: 已配置的Web3对象
    :return: 部署的合约实例
    """
    # 合约源代码
    install_solc('0.8.0')
    contract_source_code = """
    pragma solidity ^0.8.0;

    contract CheckInContract {
        mapping(address => uint256[]) private _checkIns;
        
        event CheckedIn(address indexed user, uint256 timestamp);

        function checkIn() public {
            _checkIns[msg.sender].push(block.timestamp);
            emit CheckedIn(msg.sender, block.timestamp);
        }

        function getCheckIns(address user) public view returns (uint256[] memory) {
            return _checkIns[user];
        }
    }
    """

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {f"checkin.sol": {"content": contract_source_code}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "evm.bytecode"]}
                }
            }
        },
        solc_version="0.8.0",
    )
    # return compiled_sol
    # 提取 ABI 和字节码
    abi = compiled_sol["contracts"][f"checkin.sol"]['CheckInContract']["abi"]
    bytecode = compiled_sol["contracts"][f"checkin.sol"]['CheckInContract']["evm"]["bytecode"]["object"]

    # 返回编译信息
    return {
        "abi": abi,
        "bytecode": bytecode,
    }
def get_string_from_time():
    # 定义时间字符串的格式
    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt=datetime.now()
    # 将 datetime 对象格式化为字符串
    time_str = dt.strftime(time_format)
    
    # 返回格式化后的字符串
    return time_str
def generate_random_erc20_contract():
    # 安装 Solidity 编译器
    install_solc('0.8.0')

    # 生成随机的代币名称和符号
    token_name = ''.join(random.choices(string.ascii_uppercase, k=6))
    token_symbol = ''.join(random.choices(string.ascii_uppercase, k=3))

    # 生成随机的总供应量
    total_supply = random.randint(1000000, 1000000000)

    # 编写 ERC20 合约模板
    contract_code = f"""
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract {token_name} {{
        string public name = "{token_name}";
        string public symbol = "{token_symbol}";
        uint8 public decimals = 18;
        uint256 public totalSupply;

        mapping(address => uint256) public balanceOf;
        mapping(address => mapping(address => uint256)) public allowance;

        event Transfer(address indexed from, address indexed to, uint256 value);
        event Approval(address indexed owner, address indexed spender, uint256 value);

        constructor(uint256 _totalSupply) {{
            totalSupply = _totalSupply * (10 ** uint256(decimals));
            balanceOf[msg.sender] = totalSupply;
            emit Transfer(address(0), msg.sender, totalSupply);
        }}

        function transfer(address _to, uint256 _value) public returns (bool success) {{
            require(balanceOf[msg.sender] >= _value, "Insufficient balance");
            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            return true;
        }}

        function approve(address _spender, uint256 _value) public returns (bool success) {{
            allowance[msg.sender][_spender] = _value;
            emit Approval(msg.sender, _spender, _value);
            return true;
        }}

        function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {{
            require(balanceOf[_from] >= _value, "Insufficient balance");
            require(allowance[_from][msg.sender] >= _value, "Allowance exceeded");
            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            allowance[_from][msg.sender] -= _value;
            emit Transfer(_from, _to, _value);
            return true;
        }}
    }}
    """

    # 编译合约
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {f"{token_name}.sol": {"content": contract_code}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "evm.bytecode"]}
                }
            }
        },
        solc_version="0.8.0",
    )

    # 提取 ABI 和字节码
    abi = compiled_sol["contracts"][f"{token_name}.sol"][token_name]["abi"]
    bytecode = compiled_sol["contracts"][f"{token_name}.sol"][token_name]["evm"]["bytecode"]["object"]

    # 返回编译信息
    return {
        "contract_code": contract_code,
        "abi": abi,
        "bytecode": bytecode,
        "token_name": token_name,
        "token_symbol": token_symbol,
        "total_supply": total_supply
    }
def get_contract_transaction_gas_limit(web3,func,address):
    '''
    估算所需的 gas
    '''
    max_fee_cap = Web3.to_wei(100, 'ether')
    gas_estimate = func.estimate_gas({
    'from': address
    })
    # 获取当前 gas 价格
    gas_price =web3.eth.gas_price
    # 获取账户余额
    balance = web3.eth.get_balance(address)
    # 计算总费用
    total_cost = gas_estimate * gas_price
    # 判断 gas 或转账是否合理
    if total_cost > balance:
        ValueError('gas不足')
    if total_cost > max_fee_cap:
        # 如果超出上限，调整费用为 1 ETH
        gas_estimate = max_fee_cap / gas_price
        gas_estimate = int(gas_estimate)  # 将价格转换为整数
    # 返回估算的 gas
    return gas_estimate

def deploy_contract(web3,account,compiled_contract, constructor_args=(),gas_rate=1,gas=100000):
    """
    部署智能合约
    
    :param compiled_contract: 编译后的合约对象（ABI 和 Bytecode）
    :param constructor_args: 构造函数的参数
    :return: 合约地址
    """
    
    contract = web3.eth.contract(abi=compiled_contract['abi'], bytecode=compiled_contract['bytecode'])
    tx = contract.constructor(*constructor_args).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': gas,
        'gasPrice': web3.eth.gas_price*gas_rate,
    })

    tx_hash = send_transaction(web3, tx,account.key)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt.status == 1:
        contract_address = tx_receipt.contractAddress
        logger.info(f"合约已部署，地址: {contract_address}")
        return contract_address
    else:
        logger.error(f"合约部署失败，交易哈希: {tx_receipt.transactionHash.hex()}")
        return None
class Web3Tool:
    def __init__(self, rpc_url='https://rpc.ankr.com/eth/xxx',chain_id=1,explorer=None):
        """
        初始化 Web3Tool 类实例
        
        :param rpc_url: 以太坊节点的 RPC URL
        :param private_key: （可选）用于发送交易的私钥
        """
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.chain_id=chain_id
        self.explorer=explorer
        if not self.web3.is_connected():
            logger.warning(f"无法连接到节点 {rpc_url},正在重试")
            return self.__init__(rpc_url,chain_id,explorer)

        
    def get_contract_transaction_gas_limit(self,func,address):
        '''
        估算所需的 gas
        '''
        max_fee_cap = Web3.to_wei(100, 'ether')
        gas_estimate = func.estimate_gas({
        'from': address
        })
        # 获取当前 gas 价格
        gas_price = self.web3.eth.gas_price
        # 获取账户余额
        balance = self.web3.eth.get_balance(address)
        # 计算总费用
        total_cost = gas_estimate * gas_price
        # 判断 gas 或转账是否合理
        if total_cost > balance:
            ValueError('gas不足改日领水后重试')
        if total_cost > max_fee_cap:
            # 如果超出上限，调整费用为 1 ETH
            gas_estimate = max_fee_cap / gas_price
            gas_estimate = int(gas_estimate)  # 将价格转换为整数
        # 返回估算的 gas
        return gas_estimate
    def run_contract(self, func, account,value=None):
        '''
        执行合约
        '''
        try:
            checksum_address = self.web3.to_checksum_address(account.address)
            try:
                gas_limit = self.get_contract_transaction_gas_limit(func,checksum_address )
            except:
                gas_limit=210000
            nonce = self.web3.eth.get_transaction_count(checksum_address)
            if value:
                transaction = func.build_transaction({
                'chainId': self.chain_id,
                'gas': int(gas_limit),
                'gasPrice': int(self.web3.eth.gas_price),
                'nonce': nonce,
                'value':self.web3.to_wei(value, 'ether')
                })
            else:
                transaction = func.build_transaction({
                    'chainId': self.chain_id,
                    'gas': int(gas_limit),
                    'gasPrice': int(self.web3.eth.gas_price),
                    'nonce': nonce
                })
            signed_transaction = self.web3.eth.account.sign_transaction(transaction, private_key=account.key)
            
            # 确保网络已准备好接收
            tx_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            
            # 等待交易被挖矿
            try:
                status = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            except Exception as e:
                
                logger.warning(f"Error waiting for transaction receipt: {e}")
                return tx_hash, False

            return tx_hash, status.status
        except Exception as e:
            if 'nonce too low' in str(e):
                return None, True
            raise TimeoutError(f"Error in running contract function: {e}")
    
    def get_ERC20_balance(self,address,type='ERC-20'):
        '''
        获取钱包余额
        '''
        # 获取账户余额（单位是 Wei）
        balance={}
        balance_wei = self.web3.eth.get_balance(address)
        # 将余额从 Wei 转换为 Ether
        balance_ether = self.web3.from_wei(balance_wei, 'ether')
        balance['ETH']=round(float(balance_ether),5)
        if self.explorer:
            response = requests.get(f'{self.explorer}/api/v2/addresses/{address}/tokens', params={
                'type': type,
            })
            data=response.json().get('items',[])
            
            for token in data:
                balance[token['token']['symbol']]=round(int(token['value'])/(10**int(token['token']['decimals'])),5)
        return balance
    def get_conn(self):
        return self.web3
    
    def get_balance(self, address):
        """
        获取指定地址的余额
        
        :param address: 以太坊地址
        :return: 以太币为单位的余额
        """
        balance_wei = self.web3.eth.get_balance(address)
        return self.web3.from_wei(balance_wei, 'ether')
    
    def send_transaction(self, to_address, value_in_ether, gas=21000, gas_price=None):
        """
        发送以太币交易
        
        :param to_address: 接收方地址
        :param value_in_ether: 发送的以太币数量
        :param gas: 燃气上限
        :param gas_price: 燃气价格（可选）
        :return: 交易哈希
        """
        if not self.account:
            raise ValueError("私钥未设置，无法发送交易")
        
        value_wei = self.web3.to_wei(value_in_ether, 'ether')

        tx = {
            'to': to_address,
            'value': value_wei,
            'gas': gas,
            'chainId': self.chain_id ,
            'gasPrice': gas_price or self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
        }

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        try:
            status = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        except Exception as e:
            if 'low gas price' in str(e):
                pass
        return self.web3.to_hex(tx_hash)
    
    def deploy_contract(self,account,compiled_contract, constructor_args=()):
        """
        部署智能合约
        
        :param compiled_contract: 编译后的合约对象（ABI 和 Bytecode）
        :param constructor_args: 构造函数的参数
        :return: 合约地址
        """
        
        contract = self.web3.eth.contract(abi=compiled_contract['abi'], bytecode=compiled_contract['bytecode'])
        tx = contract.constructor(*constructor_args).build_transaction({
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address),
            'gas': 300000,
            'gasPrice': self.web3.eth.gas_price*10,
        })

        signed_tx = self.web3.eth.account.sign_transaction(tx, account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.contractAddress
    
    def load_contract(self, address, abi):
        """
        加载已部署的智能合约
        
        :param address: 合约地址
        :param abi: 合约的 ABI
        :return: 合约对象
        """
        return self.web3.eth.contract(address=address, abi=abi)
    
    def call_contract_function(self, contract, function_name, *args):
        """
        调用智能合约的只读方法
        
        :param contract: 合约对象
        :param function_name: 合约方法名称
        :param args: 合约方法参数
        :return: 方法的返回值
        """
        try:
            func = contract.functions[function_name](*args)
            return func.call()
        except ContractLogicError as e:
            print(f"合约方法调用错误: {e}")
            return None
    
    def send_contract_transaction(self, contract, function_name, *args, gas=300000, gas_price=None):
        """
        调用智能合约的修改状态方法并发送交易
        
        :param contract: 合约对象
        :param function_name: 合约方法名称
        :param args: 合约方法参数
        :param gas: 燃气上限
        :param gas_price: 燃气价格（可选）
        :return: 交易哈希
        """
        if not self.account:
            raise ValueError("私钥未设置，无法发送交易")

        func = contract.functions[function_name](*args)
        tx = func.buildTransaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': gas,
            'gasPrice': gas_price or self.web3.eth.gas_price,
        })

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.toHex(tx_hash)
    def sign_msg(self,private_key,msg):
        '''
        钱包签名
        '''
        # 使用web3.py编码消息
        message_encoded = encode_defunct(text=msg)
        # 签名消息
        signed_message = self.web3.eth.account.sign_message(message_encoded,private_key)
        # 打印签名的消息
        sign=signed_message.signature.hex()
        if '0x' not in sign:
            sign ='0x'+sign
        return sign
    def get_NFTs(self,address):
        '''
        获取NFT列表
        '''
        # 获取账户余额（单位是 Wei）
        balance={}
        response = requests.get(f'{self.explorer}/api/v2/addresses/{address}/nft/collections', params={'type':''})
        data=response.json().get('items',[])
        for token in data:
            balance[token['token']['symbol']]={'id':int(token['token_instances'][0]['id']),'amount':int(token['amount'])}
        return balance
    def generate_wallet(self):
        '''
        生成钱包
        '''
        # 生成新账户
        account = self.web3.eth.account.create()
        # 获取地址和私钥
        address = account.address
        try:
            private_key = account.privateKey.hex()
        except:
            private_key = account._private_key.hex()
        return address,private_key

class Discord_Sync:
    def __init__(self, auth_token,proxies=None):
        self.auth_token = auth_token
        self.ua= UserAgent(platforms='desktop')
        defaulf_cookies = {
             '__dcfduid': '3d140d46d98711eebab5628f4db44770',
            '__sdcfduid': '3d140d46d98711eebab5628f4db4477037ec5e693d8df63143030b8c7a6f18c1f2c7992ba4eed1ac52f472f0e14d2230',
            '_ga': 'GA1.1.1892447230.1726278577',
            '_ga_YL03HBJY7E': 'GS1.1.1726278577.1.1.1726278595.0.0.0',
            'locale': 'zh-CN',
            '_gcl_au': '1.1.2053326885.1726278823',
            '_cfuvid': '6OfqLdiT7YMf2xQ8H77iRt2Bm2mJ_7v8QfMl5cOr17w-1728529581965-0.0.1.1-604800000',
            'cf_clearance': 'eIKWWFmw01Q8ojymWZIrt0yktm9DmBXDV6W9zba2_3c-1728529594-1.2.1.1-ycvJ1UVtNe5stNeqmkcMyM.eFt6T8kW8IAVDyWFOLV1RiDM1aBFaVzHylYPxc_zRcC8z5fYdhPipzn.Uq5HcX7bxBVaWvaiyjOiSA59Iu4grU9njEprHYitZgJRkjVa60ddNcuISWM1clr7GVBIcrP91CmEav.fBKTwj5_vos0CbaPX4oW..4iYFAkIZMAhHdYrZPZQRfghE390YpbNkvoRjeagHKV01NAPiBR7AMDCx_mq37inFUgswTfHyRsBvB0NlDwnRx.qD.yrwG.oqXcixRNjimb1E4mjgfBcCWFl7zKHbhOxqexwClL7LFnZIUCt582d.EmXG5m1kMWxDVSnaelii5hwZWgm6jNyhF4s7fbnK7l7eIq89RwSUGGLD2E2nFxSImBdza1aNs_e4Hw',
            'OptanonConsent': 'isIABGlobal=false&datestamp=Thu+Oct+10+2024+11%3A06%3A34+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1',
            '_ga_Q149DFWHT7': 'GS1.1.1728529595.1.0.1728529607.0.0.0',
            '__cfruid': 'e54bfe3eabe5032c48af7cba343ce579d4bdf1bc-1728529886'
        }
        defaulf_headers = {
            "authority": "x.com",
            "origin": "https://x.com",
            "x-Discord-active-user": "yes",
            "x-Discord-client-language": "en",
            "authorization": auth_token,
            "user-agent":self.ua.edge,
            'Origin': 'https://discord.com',
            'Pragma': 'no-cache',
            'Referer': 'https://discord.com/oauth2/authorize?client_id=1237047186513072168&redirect_uri=https%3A%2F%2Fapi.superstellar.world%2Fapi%2Fv1%2Faccount%2Fconnect-discord%2Fcallback&response_type=code&scope=identify+guilds+guilds.members.read&state=8d690ab0051758bf4bb7d8a4672c78d00c9405bcc45619d655e50f4b55b8195e',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Debug-Options': 'bugReporterEnabled',
            'X-Discord-Locale': 'zh-CN',
            'X-Discord-Timezone': 'Asia/Shanghai',
            'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        if proxies:
            self.Discord = Session(headers=defaulf_headers, cookies=defaulf_cookies, timeout=120,impersonate='edge99',proxies=proxies)
        else:
            self.Discord = Session(headers=defaulf_headers, cookies=defaulf_cookies, timeout=120,impersonate='edge99')
        self.auth_code = None
        self.auth_success = False  # 增加标志位记录授权是否成功
    def get_auth_codeV2(self, client_id, state, redirect_uri,scope,integration_type='0',response_type='code'):
        # 如果已经授权成功，直接返回 True，不再进行授权
        if self.auth_success:
            logger.info(f'{self.auth_token} 已成功授权，跳过重新授权')
            return True

        try:
            params = {
                'integration_type': urllib.parse.unquote(integration_type),
                'client_id': urllib.parse.unquote(client_id),
                'redirect_uri': urllib.parse.unquote(redirect_uri),
                'response_type': urllib.parse.unquote(response_type),
                'scope': urllib.parse.unquote(scope).replace('+',' '),
                'state': state
            }
            
            response = self.Discord.get('https://discord.com/api/v9/oauth2/authorize', params=params)
            if "code" in response.json() and response.json()["code"] == 353:
                self.Discord.headers.update({"x-csrf-token": response.cookies["ct0"]})
                logger.warning(f'{response.json()}')
                return self.get_auth_codeV2(client_id, state, redirect_uri,scope,integration_type,response_type)
            elif response.status_code == 429:
                time.sleep(5)
                return self.get_auth_codeV2(client_id, state,redirect_uri,scope,integration_type,response_type)
            elif response.status_code == 200:
                self.auth_code = response.json()
                params.pop('integration_type')
                return params
            logger.error(f'{self.auth_token} 获取auth_code失败')
            return False
        except Exception as e:
            logger.error(e)
            return False
    def Discord_authorizeV2(self, client_id, state, redirect_uri,scope,integration_type='0',response_type='code'):
        # 如果已经授权成功，直接返回 True，不再进行授权
        if self.auth_success:
            logger.info(f'{self.auth_token} 已成功授权，跳过重新授权')
            return True
        try:
            params=self.get_auth_codeV2(client_id, state,redirect_uri,scope,integration_type,response_type)
            if not params:
                return False
            json_data = {
                'permissions': '0',
                'authorize': True,
                'integration_type': 0,
                'location_context': {
                    'guild_id': '10000',
                    'channel_id': '10000',
                    'channel_type': 10000,
                },
            }
            response = self.Discord.post('https://discord.com/api/v9/oauth2/authorize', json=json_data,params=params)
            if 'location' in response.text:
                self.auth_success = True  # 授权成功，设置标志位
                url=response.json().get('location')
                response = self.Discord.get(url)
                logger.success(f'{self.auth_token} Discord授权成功')
                return True
            elif response.status_code == 429:
                time.sleep(5)
                return self.Discord_authorizeV2(client_id, state,redirect_uri,scope,integration_type,response_type)
            logger.error(f'{self.auth_token} Discord授权失败')
            return False
        except Exception as e:
            logger.error(f'{self.auth_token} Discord授权异常：{e}')
            return False
def get(li:list,index:int=0):
    if len(li)>index:
        return li[index]
    else:
        return ""
def generate_auth_string(user:str, token:str)->str:
    auth_string = f"user={user}\1auth=Bearer {token}\1\1"
    return auth_string

def get_num_code(text:Any,num:int=6)->Union[None,str]:
    code=re.findall(r'(\d{%s})'%num,str(text))
    if code:
        return code[0]
    else:
        return None

def tuple_to_str(tuple_:tuple)->str:
    """
    元组转为字符串输出
    :param tuple_: 转换前的元组，QQ邮箱格式为(b'\xcd\xf5\xd4\xc6', 'gbk')或者(b' <XXXX@163.com>', None)，163邮箱格式为('<XXXX@163.com>', None)
    :return: 转换后的字符串
    """
    if tuple_[1]:
        out_str = tuple_[0].decode(tuple_[1])
    else:
        if isinstance(tuple_[0], bytes):
            out_str = tuple_[0].decode("gbk")
        else:
            out_str = tuple_[0]
    return out_str
class EmailOauth2Sync:
    def __init__(
        self,
        email_address:str,
        refresh_token:str,
        id:str,
        imap_server:str='outlook.live.com',
        imap_port:int=143,
        timeout:int=10
    ) -> None:
        self.email_address=email_address
        self.refresh_token=refresh_token
        self.id=id
        self.imap_server=imap_server
        self.imap_port=imap_port
        self.timeout=timeout
        self.login_imap4()
    def login_imap4(self):
        self.access_token=self.get_accesstoken(self.refresh_token)
        self.mail = imaplib.IMAP4(self.imap_server,self.imap_port,timeout=self.timeout)
        self.mail.starttls()
        self.mail.authenticate('XOAUTH2', lambda x:generate_auth_string(self.email_address, self.access_token))
        logger.success('邮箱登陆成功')
    def get_accesstoken(self, refresh_token):
        data = {
            "client_id": self.id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        ret = requests.post(
            "https://login.microsoftonline.com/consumers/oauth2/v2.0/token", data=data
        )
        assert ret.json().get("access_token"), "Token失效"
        return ret.json().get("access_token")
    def fetch_email_body(self, item):
        status, msg_data = self.mail.fetch(item, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        # 解析邮件详细信息
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            # 如果主题是字节类型，则进行解码
            subject = subject.decode(encoding if encoding else "utf-8")
        from_ = msg.get("From")
        date_ =  datetime.strptime(msg.get("Date"), '%a, %d %b %Y %H:%M:%S %z')
        body = ""
        # 处理邮件内容
        if msg.is_multipart():
            # 如果邮件是多部分的
            for part in msg.walk():
                # 获取邮件内容类型
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if (
                    content_type == "text/plain"
                    and "attachment" not in content_disposition
                ):
                    # 获取邮件正文
                    body = part.get_payload(decode=True).decode()
        else:
            # 如果邮件不是多部分的
            body = msg.get_payload(decode=True).decode()
        
        return {"from": from_, "subject": subject, "date": date_, "body": body,"item":item}
    def getmail(self,select,method='ALL'):
        assert method in ['ALL','UNSEEN'],"method not in ['ALL','UNSEEN']"
        self.mail.select(select)
        status, messages = self.mail.search(None, method) #UNSEEN 为未读邮件
        all_emails = messages[0].split()
        mails=[]
        for item in all_emails:
            mails.append(self.fetch_email_body(item))
        return mails
    def get_all_mail(self,method='ALL'):
        return self.getmail('INBOX',method) +self.getmail('Junk',method)
    #监听未读
    def listening_unsee_mails(self,_from=None,get_code=False,num=6,tries=10):
        while tries>0:
            if _from:
                mails=filter(lambda x:_from in x.get('from'),self.get_all_mail('UNSEEN'))
            else:
                mails=self.get_all_mail('UNSEEN')
            mails=list(sorted(mails,key=lambda x:x.get('date')))
            
            if mails:
                mail=mails.pop()
                # 设置已读
                self.mail.store(mail['item'], '+FLAGS', '\\Seen')
                if get_code:
                    code=get_num_code(mail['body'],num)
                    logger.debug(f'收到邮件，内容为：{code}')
                    return code
                return [mail]
            logger.debug('未收到邮件，监听中...')
            time.sleep(5)
            tries-=1
        return False
class EmailOauth2SyncByPassWord:
    def __init__(
        self,
        email_address:str,
        password:str,
        imap_server:str='mailserver.0xfiang.com',
        imap_port:int=143,
        timeout:int=10
    ) -> None:
        self.email_address=email_address
        self.password=password
        self.imap_server=imap_server
        self.imap_port=imap_port
        self.timeout=timeout
        self.login_imap4()
    def login_imap4(self):
        self.mail = imaplib.IMAP4(self.imap_server,self.imap_port)
        self.mail.starttls()
        self.mail.login(str(self.email_address), str(self.password))
        logger.success('邮箱登陆成功')

    def fetch_email_body(self, item):
        status, msg_data = self.mail.fetch(item, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        # 解析邮件详细信息
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            # 如果主题是字节类型，则进行解码
            subject = subject.decode(encoding if encoding else "utf-8")
        from_ = msg.get("From")
        date_ =  datetime.strptime(msg.get("Date").replace(" (UTC)", ""), '%a, %d %b %Y %H:%M:%S %z')
        body = ""
        # 处理邮件内容
        if msg.is_multipart():
            # 如果邮件是多部分的
            for part in msg.walk():
                # 获取邮件内容类型
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if (
                    content_type == "text/plain"
                    and "attachment" not in content_disposition
                ):
                    # 获取邮件正文
                    try:
                        body = part.get_payload(decode=True).decode("gbk")
                    except:
                        body = part.get_payload(decode=True).decode("utf8")
        else:
            # 如果邮件不是多部分的
            try:
                body = part.get_payload(decode=True).decode("gbk")
            except:
                body = part.get_payload(decode=True).decode("utf8")
        
        return {"from": from_, "subject": subject, "date": date_, "body": body,"item":item}
    def getmail(self,select,method='ALL'):
        assert method in ['ALL','UNSEEN'],"method not in ['ALL','UNSEEN']"
        self.mail.select(select)
        status, messages = self.mail.search(None, method) #UNSEEN 为未读邮件
        all_emails = messages[0].split()
        mails=[]
        for item in all_emails:
            mails.append(self.fetch_email_body(item))
        return mails
    def get_all_mail(self,method='ALL'):
        return self.getmail('INBOX',method) +self.getmail('Junk',method)
    #监听未读
    def listening_unsee_mails(self,get_code=False,num=6):
        count=100
        while count>=0:            
            mails=list(sorted(self.get_all_mail('UNSEEN'),key=lambda x:x.get('date')))
            

            if mails:
                mail=mails.pop()
                # 设置已读
                # self.mail.store(mail['item'], '+FLAGS', '\\Seen')
                if get_code:
                    code=get_num_code(mail['body'],num)
                    return mail,code
                return mail
            logger.debug('未收到邮件，监听中...')
            time.sleep(5)
            count-=1
def send_transaction(web3,transaction,private_key):
    signed_tx = web3.eth.account.sign_transaction(transaction,private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    except Exception as e:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
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
        response = self.session2.get("https://api.x.com/oauth/authenticate", params=params,verify=False)
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
        
        response = self.session2.post("https://x.com/oauth/authorize", data=data,verify=False)
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
        response = self.session.get(f"{self.TWITTER_API_BASE}/oauth2/authorize", params=params,verify=False)
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
        response = self.session.post(f"{self.TWITTER_API_BASE}/oauth2/authorize", data=data,verify=False)
        self._handle_response(response, retry)
        if  "redirect_uri" not in response.text:
            raise ValueError("响应中未找到redirect_uri")
        redirect_uri=response.json().get("redirect_uri")
        return auth_code,redirect_uri
@sleep_and_retry
@limits(calls=REQUESTS_PER_SECOND, period=ONE_SECOND)
def get_cf_token(site,siteKey,method="turnstile-min",url='http://127.0.0.1:3000',authToken=None,action=None):
    data = {
            "url": site,
            "siteKey": siteKey,
            "mode": method
        }
    if authToken:
        data.update({
            "authToken": authToken,
        })

    if action:
        data.update({
            "action": action
        })
        
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
def is_any_hours_away(timestamp,hours=12):
    if not timestamp:
        return True
    current_time = time.time()
    time_difference =  current_time-timestamp
    if time_difference >= 24 * 60 * 60:
        return True
    else:
        return False
class MailcowClient:
    def __init__(self, api_url, api_key,defualt_pwd='123456',domain='mailserver.0xfiang.com',output_path='./'):
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            'X-Api-Key':api_key
        }
        self.fa = Faker()
        self.defualt_pwd=defualt_pwd
        self.domain=domain
        self.session=requests.Session()
        self.session.headers.update(self.headers)
        self.domain_info=self.get_domain_info()
        self.output_path=output_path
        self.new_email_list=[]
    def get_domain_info(self):
        url = f"{self.api_url}/api/v1/get/domain/{self.domain}"
        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get mailbox info: {response.status_code}, {response.text}")
    def add_mailbox(self, password=None):
        assert self.domain_info['mboxes_left']>0,"邮箱数量已达上限"
        url = f"{self.api_url}/api/v1/add/mailbox"
        if not password:
            password=self.defualt_pwd
        index=self.domain_info['mboxes_in_domain']+1
        name=f'{self.fa.first_name()}{index}'.lower()
        data = {
            'active': '1',
            'domain': self.domain,
            'local_part': name,
            'name': name,
            'password': password,
            'password2': password,
            'quota': '0',
            'force_pw_update': 0,
            'sogo_access': ['0', '1'],
            'tls_enforce_in': '1',
            'tls_enforce_out': '1',
            'tags': [],
            'rl_value': '',
            'rl_frame': 's',
            'quarantine_notification': 'hourly',
            'quarantine_category': 'add_header',
        }
        response = self.session.post(url, json=data, headers=self.headers)
        if response.status_code == 200:
            self.domain_info['mboxes_in_domain']+=1
            self.domain_info['mboxes_left']-=1
            logger.debug(f"Mailbox {name}@{self.domain} added successfully.")
            email={
                'email':f'{name}@{self.domain}',
                'password':password
            }
            self.new_email_list.append(email)
            return email
        else:
            raise Exception(f"Failed to add mailbox: {response.status_code}, {response.text}")
    def add_mailbox_many(self,count=10):
        for i in range(count):
            self.add_mailbox()
        self.save_email()
    def save_email(self):
        if self.new_email_list:
            length=len(self.new_email_list)
            df = pd.DataFrame(self.new_email_list)
            file_path=os.path.join(self.output_path,f'new_mails_{length}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv')
            df.to_csv(file_path, index=False)
            logger.success(f"已保存邮箱信息到:{file_path}")
class SOGoTools:    
    def __init__(self, username, password, base_url='https://mail.0xfiang.com'):
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
        }
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login()
        self.put_xsrf_token()
    def login(self):
        json_data = {
            'userName': self.username,
            'password': self.password,
            'domain': None,
            'rememberLogin': 1,
        }
        response = self.session.post(f'{self.base_url}/SOGo/connect', headers=self.headers, json=json_data)
        if response.status_code == 200:
            logger.success(f"邮箱：{self.username}，登录成功")
        else:
            logger.error(f"邮箱：{self.username}，登录失败,{response.text}")
    def put_xsrf_token(self):
        XSRF_TOKEN=self.session.cookies.get_dict().get('XSRF-TOKEN')
        self.session.headers.update({'X-XSRF-TOKEN':XSRF_TOKEN})
    def query_msg(self,query:str=None)->list:
        if query:
            json_data = {
                'sortingAttributes': {
                    'sort': 'date',
                    'asc': 0,
                    'match': 'OR',
                },
                'filters': [
                    {
                        'searchBy': 'subject',
                        'searchInput': query,
                    },
                    {
                        'searchBy': 'from',
                        'searchInput': query,
                    },
                ],
            }
        else:
            json_data = {
                'sortingAttributes': {
                    'sort': 'date',
                    'asc': 0
                }
            }
        result=[]
        response = self.session.post(f'{self.base_url}/SOGo/so/{self.username}/Mail/0/folderINBOX/view',  headers=self.headers, json=json_data)
        if response.status_code == 200:
            uids_INBOX=response.json().get('uids',[])
        else:
            uids_INBOX=[]
        response = self.session.post(f'{self.base_url}/SOGo/so/{self.username}/Mail/0/folderJunk/view', headers=self.headers, json=json_data)
        if response.status_code == 200:
            uids_Junk=response.json().get('uids',[])
        else:
            uids_Junk=[]
        for _id in uids_INBOX:
            response = self.session.get(f'{self.base_url}/SOGo/so/{self.username}/Mail/0/folderINBOX/{_id}/view',  headers=self.headers)
            result.append(response.json())
        for _id in uids_Junk:
            response = self.session.get(f'{self.base_url}/SOGo/so/{self.username}/Mail/0/folderJunk/{_id}/view',  headers=self.headers)
            result.append(response.json())
        if result:
            return result
        else:
            logger.debug(f"邮箱：{self.username}，未找到：{query}")
            return []
    def convert_date(self,date_str):
        # 中文星期和月份映射到英文
        # 星期三对应Wednesday，九月对应September
        # 创建一个中文到英文的映射字典
        translations = {
            '星期一': 'Monday',
            '星期二': 'Tuesday',
            '星期三': 'Wednesday',
            '星期四': 'Thursday',
            '星期五': 'Friday',
            '星期六': 'Saturday',
            '星期天': 'Sunday',
            '一月': 'January',
            '二月': 'February',
            '三月': 'March',
            '四月': 'April',
            '五月': 'May',
            '六月': 'June',
            '七月': 'July',
            '八月': 'August',
            '九月': 'September',
            '十月': 'October',
            '十一月': 'November',
            '十二月': 'December'
        }

        # 替换中文的星期和月份
        for zh, en in translations.items():
            date_str = date_str.replace(zh, en)
        date_format = '%A, %B %d, %Y %H:%M'
        # 解析日期时间字符串（忽略时区）
        date_obj = datetime.strptime(date_str[:-4], date_format)
        return date_obj
    def get_num_code(self,data,num=4):
        code=re.findall(f'(\d{num})',str(data))
        if code:
            return code[0]
        else:
            return data
    def get_new_msg(self,query,code=False,num=6):
        now=datetime.now()
        count=0
        while count<60:
            data_list=self.query_msg(query)
            for _ in data_list:
                if self.convert_date(_['date'])>now:
                    return _
            time.sleep(3)
            count+=1
            logger.warning(f'邮箱：{self.username}，未收到新消息,重试中')
        return None
if __name__ == "__main__":
    token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDAwMzg4MzEsImlhdCI6MTczOTk1MjQzMSwid2FsbGV0QWRkcmVzcyI6IjB4NzI2OTFhMzZFRDFmQUMzYjE5N0ZiNDI2MTJEYzE1YTg5NThiZjlmMiJ9.EblYl7VCbD6r55d8j6XmVwtHimore9YbKBZGOruAbhg'
    print(check_jwt_exp(token))