import os
import sys
import pandas as pd
from loguru import logger
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from core.utils import Web3Tool
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime

def create_wallet(web3_tool):
    
    address,private_key=web3_tool.generate_wallet()
    return {'address':address,'private_key':private_key}

def main(num,max_workers=10):
    wallet_list=[]
    web3_tool=Web3Tool('https://rpc.secwarex.io/eth')
    date_time=datetime.now().strftime('%Y%m%d_%H%M%S')
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_list=[executor.submit(create_wallet,web3_tool) for _ in range(num)]
        # 获取结果
        for future in as_completed(future_list):
            wallet_list.append(future.result())
            logger.success(f'已生成{len(wallet_list)}个钱包')
    path=f'data/wallet_{date_time}.csv'
    pd.DataFrame(wallet_list).to_csv(path,index=False)
    abs_path=os.path.abspath(path)
    logger.success('生成完毕,请查看:{}'.format(abs_path))
if __name__ == '__main__':
    num=int(input('请输入要生成的钱包数量:'))
    main(num)
    
