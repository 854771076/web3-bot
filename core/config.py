import json
import random
import pandas as pd
from threading import Lock


class Config():
    def __init__(self,path='./config.json'):
        self.path=path
        self.config=self.load_config()
        self.accounts=self.load_accounts()
        self._lock = Lock()
    def load_config(self):
        with open(self.path,'r') as f:
            config=json.load(f)
        for key in config:
            setattr(self,key,config[key])
        return config
    def load_accounts(self):
        try:
            df=pd.read_csv(self.account_path)
        except:
            df=pd.read_csv(self.account_path,encoding='gbk')
        df=df.fillna(False).replace('False',None).replace('True',True)
        return df.to_dict('records') 
    def save_accounts(self):
        with self._lock:
            df=pd.DataFrame(self.accounts)
            df.to_csv(self.account_path,index=False)
    def get_random_invite_code(self):
        register_account=[i.get('invitationCode') for i in self.accounts if i.get('invitationCode') and i.get('bind_x')][:10]+[self.invite_code for i in range(10)]
        if not register_account:
            return self.invite_code
        return random.choice(register_account)
    def get_random_accounts(self,account,num=1):
        accounts=[a for a in self.accounts if account['address'] != a['address'] ]
        choice_accounts=random.sample(accounts,num)
        if not choice_accounts:
            raise ValueError("没有可用的账户")
        return choice_accounts
    def get_random_private_key(self):
        private_key=random.choice(self.accounts).get('private_key')

        return private_key