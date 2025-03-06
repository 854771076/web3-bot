import os
import sys
import pandas as pd
from loguru import logger
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core.utils import XAuth
from concurrent.futures import ThreadPoolExecutor
x_token_file='data/x.csv'
try:
    x_token_list=pd.read_csv(x_token_file).to_dict(orient='records')
except:
    x_token_list=pd.read_csv(x_token_file,encoding='gbk').to_dict(orient='records')
def ckeck_alive(index,token):
    x=XAuth(token['x_token'])
    try:
        x.get_auth_code({'test':1})
    except Exception as e:
        if 'Bad Token' in str(e):
            logger.warning(f'已失效:{e}')
            token['alive']=False
        else:
            if 'ssl' in str(e).lower()():
                logger.exception(f'VPN或网络异常:{e}')
                return
            if '响应中未找到auth_code' in str(e):
                logger.warning(f'响应中未找到auth_code:{e}')
                token['alive']=False
            token['alive']=True
    logger.info(f'{index}-{token}')

with ThreadPoolExecutor(max_workers=1) as executor:
    for index,token in enumerate(x_token_list):
        executor.submit(ckeck_alive,index,token)
    
pd.DataFrame(x_token_list).to_csv('data/alive_x_token.csv',index=False)
