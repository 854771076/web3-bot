from core.bot.basebot import *
from core.config import Config
true=True
false=False
null=None
box_manager_contract={"address":"0x202f2025d638459b2eab6eb68bfda101c46db972","abi":[{"type":"function","name":"BOX_PRICE","inputs":[],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"boxNFT","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"commonNFT","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"firstOpen","inputs":[{"name":"","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"view"},{"type":"function","name":"initialize","inputs":[{"name":"_boxNFT","type":"address","internalType":"address"},{"name":"_commonNFT","type":"address","internalType":"address"},{"name":"_uncommonNFT","type":"address","internalType":"address"},{"name":"_rareNFT","type":"address","internalType":"address"},{"name":"_rewardToken","type":"address","internalType":"address"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"mint","inputs":[{"name":"quantity","type":"uint256","internalType":"uint256"},{"name":"refer","type":"address","internalType":"address"}],"outputs":[],"stateMutability":"payable"},{"type":"function","name":"mintableAmount","inputs":[{"name":"user","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"openBox","inputs":[{"name":"quantity","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"owner","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"rareNFT","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"referrals","inputs":[{"name":"","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"remainingMintTimes","inputs":[{"name":"","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"renounceOwnership","inputs":[],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"rewardToken","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"setBoxPrice","inputs":[{"name":"_newPrice","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"totalMints","inputs":[],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"transferOwnership","inputs":[{"name":"newOwner","type":"address","internalType":"address"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"uncommonNFT","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"withdraw","inputs":[],"outputs":[],"stateMutability":"nonpayable"},{"type":"event","name":"BoxMinted","inputs":[{"name":"user","type":"address","indexed":true,"internalType":"address"},{"name":"tokenId","type":"uint256","indexed":false,"internalType":"uint256"}],"anonymous":false},{"type":"event","name":"Initialized","inputs":[{"name":"version","type":"uint64","indexed":false,"internalType":"uint64"}],"anonymous":false},{"type":"event","name":"OwnershipTransferred","inputs":[{"name":"previousOwner","type":"address","indexed":true,"internalType":"address"},{"name":"newOwner","type":"address","indexed":true,"internalType":"address"}],"anonymous":false},{"type":"error","name":"InvalidInitialization","inputs":[]},{"type":"error","name":"NotInitializing","inputs":[]},{"type":"error","name":"OwnableInvalidOwner","inputs":[{"name":"owner","type":"address","internalType":"address"}]},{"type":"error","name":"OwnableUnauthorizedAccount","inputs":[{"name":"account","type":"address","internalType":"address"}]}]}
box_nft_contract={"address":"0x42f14e56afe10b122cdd3896d70b6be1e96b545e","abi":[{"type":"constructor","inputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"approve","inputs":[{"name":"to","type":"address","internalType":"address"},{"name":"tokenId","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"balanceOf","inputs":[{"name":"owner","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"burn","inputs":[{"name":"tokenId","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"gameContract","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"getApproved","inputs":[{"name":"tokenId","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"isApprovedForAll","inputs":[{"name":"owner","type":"address","internalType":"address"},{"name":"operator","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"view"},{"type":"function","name":"mint","inputs":[{"name":"to","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"nonpayable"},{"type":"function","name":"name","inputs":[],"outputs":[{"name":"","type":"string","internalType":"string"}],"stateMutability":"view"},{"type":"function","name":"owner","inputs":[],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"ownerOf","inputs":[{"name":"tokenId","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"address","internalType":"address"}],"stateMutability":"view"},{"type":"function","name":"renounceOwnership","inputs":[],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"safeTransferFrom","inputs":[{"name":"from","type":"address","internalType":"address"},{"name":"to","type":"address","internalType":"address"},{"name":"tokenId","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"safeTransferFrom","inputs":[{"name":"from","type":"address","internalType":"address"},{"name":"to","type":"address","internalType":"address"},{"name":"tokenId","type":"uint256","internalType":"uint256"},{"name":"data","type":"bytes","internalType":"bytes"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"setApprovalForAll","inputs":[{"name":"operator","type":"address","internalType":"address"},{"name":"approved","type":"bool","internalType":"bool"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"setBaseURI","inputs":[{"name":"newBaseURI","type":"string","internalType":"string"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"setGameContract","inputs":[{"name":"_gameContract","type":"address","internalType":"address"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"supportsInterface","inputs":[{"name":"interfaceId","type":"bytes4","internalType":"bytes4"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"view"},{"type":"function","name":"symbol","inputs":[],"outputs":[{"name":"","type":"string","internalType":"string"}],"stateMutability":"view"},{"type":"function","name":"tokenByIndex","inputs":[{"name":"index","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"tokenOfOwnerByIndex","inputs":[{"name":"owner","type":"address","internalType":"address"},{"name":"index","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"tokenURI","inputs":[{"name":"tokenId","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"string","internalType":"string"}],"stateMutability":"view"},{"type":"function","name":"tokensOfOwner","inputs":[{"name":"owner","type":"address","internalType":"address"},{"name":"limit","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"uint256[]","internalType":"uint256[]"}],"stateMutability":"view"},{"type":"function","name":"totalSupply","inputs":[],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"transferFrom","inputs":[{"name":"from","type":"address","internalType":"address"},{"name":"to","type":"address","internalType":"address"},{"name":"tokenId","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"transferOwnership","inputs":[{"name":"newOwner","type":"address","internalType":"address"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"event","name":"Approval","inputs":[{"name":"owner","type":"address","indexed":true,"internalType":"address"},{"name":"approved","type":"address","indexed":true,"internalType":"address"},{"name":"tokenId","type":"uint256","indexed":true,"internalType":"uint256"}],"anonymous":false},{"type":"event","name":"ApprovalForAll","inputs":[{"name":"owner","type":"address","indexed":true,"internalType":"address"},{"name":"operator","type":"address","indexed":true,"internalType":"address"},{"name":"approved","type":"bool","indexed":false,"internalType":"bool"}],"anonymous":false},{"type":"event","name":"BoxMinted","inputs":[{"name":"to","type":"address","indexed":true,"internalType":"address"},{"name":"tokenId","type":"uint256","indexed":false,"internalType":"uint256"}],"anonymous":false},{"type":"event","name":"OwnershipTransferred","inputs":[{"name":"previousOwner","type":"address","indexed":true,"internalType":"address"},{"name":"newOwner","type":"address","indexed":true,"internalType":"address"}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"name":"from","type":"address","indexed":true,"internalType":"address"},{"name":"to","type":"address","indexed":true,"internalType":"address"},{"name":"tokenId","type":"uint256","indexed":true,"internalType":"uint256"}],"anonymous":false},{"type":"error","name":"ERC721EnumerableForbiddenBatchMint","inputs":[]},{"type":"error","name":"ERC721IncorrectOwner","inputs":[{"name":"sender","type":"address","internalType":"address"},{"name":"tokenId","type":"uint256","internalType":"uint256"},{"name":"owner","type":"address","internalType":"address"}]},{"type":"error","name":"ERC721InsufficientApproval","inputs":[{"name":"operator","type":"address","internalType":"address"},{"name":"tokenId","type":"uint256","internalType":"uint256"}]},{"type":"error","name":"ERC721InvalidApprover","inputs":[{"name":"approver","type":"address","internalType":"address"}]},{"type":"error","name":"ERC721InvalidOperator","inputs":[{"name":"operator","type":"address","internalType":"address"}]},{"type":"error","name":"ERC721InvalidOwner","inputs":[{"name":"owner","type":"address","internalType":"address"}]},{"type":"error","name":"ERC721InvalidReceiver","inputs":[{"name":"receiver","type":"address","internalType":"address"}]},{"type":"error","name":"ERC721InvalidSender","inputs":[{"name":"sender","type":"address","internalType":"address"}]},{"type":"error","name":"ERC721NonexistentToken","inputs":[{"name":"tokenId","type":"uint256","internalType":"uint256"}]},{"type":"error","name":"ERC721OutOfBoundsIndex","inputs":[{"name":"owner","type":"address","internalType":"address"},{"name":"index","type":"uint256","internalType":"uint256"}]},{"type":"error","name":"OwnableInvalidOwner","inputs":[{"name":"owner","type":"address","internalType":"address"}]},{"type":"error","name":"OwnableUnauthorizedAccount","inputs":[{"name":"account","type":"address","internalType":"address"}]}]}
nft721={
    'MonAIEvolvedRelic': "0x3c797d0a52a1f75ed16fb4fcc690d0e9bf937c30",
    'MonAIGenesisSeed': "0xd7e0b098a1ded27f76aa619a076a0c64a1066932",
    'MonAIMystery': "0xde902fbf47253fc2680b7c206ec5a998e584cc75",
    'MonAIMysteryBox': "0x42f14e56afe10b122cdd3896d70b6be1e96b545e"
}
MonAI='0x7348fac1b35be27b0b636f0881afc9449ec54ba5'
#实例化以上合约
class MonadBot(BaseBot):
    def _init_contract(self):
        self.box_manager_contract=self.web3.eth.contract(address=Web3.to_checksum_address(box_manager_contract['address']),abi=box_manager_contract['abi'])
        self.box_nft_contract=self.web3.eth.contract(address=Web3.to_checksum_address(box_nft_contract['address']),abi=box_nft_contract['abi'])
        ERC20_ABI=json.loads(open('./contracts/ERC20.json').read())
        ERC721_ABI=json.loads(open('./contracts/NFT-ERC721.json').read())
        self.MonAI_contract=self.web3.eth.contract(address=Web3.to_checksum_address(MonAI),abi=ERC20_ABI)
        self.MonAIEvolvedRelic_contract=self.web3.eth.contract(address=Web3.to_checksum_address(nft721['MonAIEvolvedRelic']),abi=ERC721_ABI)
        self.MonAIGenesisSeed_contract=self.web3.eth.contract(address=Web3.to_checksum_address(nft721['MonAIGenesisSeed']),abi=ERC721_ABI)
        self.MonAIMystery_contract=self.web3.eth.contract(address=Web3.to_checksum_address(nft721['MonAIMystery']),abi=ERC721_ABI)
        self.MonAIMysteryBox_contract=self.web3.eth.contract(address=Web3.to_checksum_address(nft721['MonAIMysteryBox']),abi=ERC721_ABI)
    def __init__(self, account, web3, config: Config):
        super().__init__(account, web3, config)
        self._init_contract()
        self.main_wallet=self.web3.eth.account.from_key(self.config.mail_wallet_private_key)
    def _handle_response(self, response, retry_func=None) -> None:
        """处理响应状态"""
        try:
            response.raise_for_status()
            data=response.json()
            if not data.get('success'):
                raise Exception(f"执行异常,{data.get('error')}")
            return data
        # 抛出代理错误
        except requests.exceptions.ProxyError as e:
            logger.warning(f"代理错误,{e},重试中...")
            time.sleep(self.config.RETRY_INTERVAL)
            if retry_func:
                return retry_func()
        except Exception as e:
            raise Exception(f"请求过程中发生错误,{e},{response.text}")
    
    def registe(self):
        if self.account.get('registed'):
            return
        logger.info(f"账户:{self.wallet.address},注册中...")
        json_data = {
            'address': self.wallet.address,
            'refer_by': self.config.invite_code,
        }
        response = self.session.post('https://api.monai.gg/users', json=json_data)
        data=self._handle_response(response)
        if not self.account.get('registed'):
            self.account['registed']=True
            self.config.save_accounts()
        self.config.save_accounts()
        logger.success(f"账户:{self.wallet.address},注册成功")
    def mint_box(self):
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance<self.box_manager_contract.functions.BOX_PRICE().call():
            logger.warning(f"账户:{self.wallet.address},余额不足,跳过")
            return
        logger.info(f"账户:{self.wallet.address},铸造中...")
        func=self.box_manager_contract.functions.mint(1,Web3.to_checksum_address(self.main_wallet.address))
        # gas=get_contract_transaction_gas_limit(self.web3, func, self.wallet.address)
        tx=func.build_transaction(
            {
                'from': self.wallet.address,
                'value': self.box_manager_contract.functions.BOX_PRICE().call(),
                'gasPrice': self.web3.eth.gas_price,
                'gas': 300000,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
            }
        )
        signed_txn = self.wallet.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:{self.wallet.address},mint成功")
        else:
            logger.error(f"账户:{self.wallet.address},,mint失败,原因:{receipt}")
    def transfer_MonAI(self) :
        # 通过self.MonAI_contract 查询数量
        MonAI_balance=self.MonAI_contract.functions.balanceOf(self.wallet.address).call()
        if MonAI_balance==0:
            logger.warning(f"账户:{self.wallet.address},没有$MonAI,跳过")
            return
        logger.info(f"账户:{self.wallet.address},transfer中...")
        transaction=self.MonAI_contract.functions.transfer(self.main_wallet.address,MonAI_balance).build_transaction(
            {
                'from': self.wallet.address,
                'gasPrice': self.web3.eth.gas_price,
                'gas': 50000,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address),

            } 
        )
        tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            logger.success(f"账户:{self.wallet.address},transfer $MonAI 成功")
        else:
            logger.error(f"账户:{self.wallet.address},transfer $MonAI 失败,原因:{receipt}")
    
    def transfer_box(self) :
        # 通过self.box_nft_contract 查询box数量
        box_count=self.box_nft_contract.functions.balanceOf(self.wallet.address).call()
        if box_count==0:
            logger.warning(f"账户:{self.wallet.address},没有box,跳过")
            return
        logger.info(f"账户:{self.wallet.address},transfer中...")
        for i in range(box_count):
            token_id=self.box_nft_contract.functions.tokenOfOwnerByIndex(self.wallet.address,i).call()
            func=self.box_nft_contract.functions.safeTransferFrom(self.wallet.address,self.main_wallet.address,token_id)
            gas=get_contract_transaction_gas_limit(self.web3, func, self.wallet.address)
            transaction=func.build_transaction(
                {
                    'from': self.wallet.address,
                    'gasPrice': self.web3.eth.gas_price,
                    'gas': gas,
                    'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
                } 
            )
            tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                logger.success(f"账户:{self.wallet.address},transfer box 成功")
            else:
                logger.error(f"账户:{self.wallet.address},transfer box 失败,原因:{receipt}")
    def transfer_eth(self):
        # 从主地址转账随机余额（0.12-0.13）到钱包地址，如果余额大于等于0.12eth则跳过
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance>self.web3.to_wei(0.12,'ether'):
            logger.warning(f"账户:{self.wallet.address},余额足够,跳过")
            return
        logger.info(f"账户:{self.wallet.address},转账中...")
        transaction={
            'from': self.main_wallet.address,
            'to': self.wallet.address,
            'value': self.web3.to_wei(random.uniform(0.13,0.14),'ether'),
            'gasPrice': self.web3.eth.gas_price, 
            'gas': 200000,
            'nonce': self.web3.eth.get_transaction_count(self.main_wallet.address),
        } 
        tx_hash = send_transaction(self.web3, transaction, self.main_wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:{self.wallet.address},转账成功")
        else:
            logger.error(f"账户:{self.wallet.address},转账失败,原因:{receipt}")

class MonadBotManager(BaseBotManager):
    def run_single(self,account):
        bot=MonadBot(account,self.web3,self.config)
        bot.login()
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")

    