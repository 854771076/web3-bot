from core.bot.basebot import *
from core.config import Config
from threading import Lock
lock=Lock()
nft721='0x071126cBec1C5562530Ab85fD80dd3e3a42A70B8'
false=False
true=True
null=None
abi=[{"inputs":[],"name":"AlreadyInitialized","type":"error"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[{"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"CannotExceedMaxSupplyOfUint64","type":"error"},{"inputs":[{"internalType":"uint256","name":"basisPoints","type":"uint256"}],"name":"InvalidRoyaltyBasisPoints","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"}],"name":"MintQuantityExceedsMaxSupply","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"NewOwnerIsZeroAddress","type":"error"},{"inputs":[],"name":"NotNextOwner","type":"error"},{"inputs":[],"name":"OnlyAllowedSeaDrop","type":"error"},{"inputs":[],"name":"OnlyOwner","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"ProvenanceHashCannotBeSetAfterMintStarted","type":"error"},{"inputs":[],"name":"RoyaltyAddressCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"SameTransferValidator","type":"error"},{"inputs":[],"name":"SignersMismatch","type":"error"},{"inputs":[],"name":"TokenGatedMismatch","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"allowedSeaDrop","type":"address[]"}],"name":"AllowedSeaDropUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"newContractURI","type":"string"}],"name":"ContractURIUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"MaxSupplyUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newPotentialAdministrator","type":"address"}],"name":"PotentialOwnerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"previousHash","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"newHash","type":"bytes32"}],"name":"ProvenanceHashUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"bps","type":"uint256"}],"name":"RoyaltyInfoUpdated","type":"event"},{"anonymous":false,"inputs":[],"name":"SeaDropTokenDeployed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oldValidator","type":"address"},{"indexed":false,"internalType":"address","name":"newValidator","type":"address"}],"name":"TransferValidatorUpdated","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cancelOwnershipTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"contractURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"internalType":"uint256","name":"toTokenId","type":"uint256"}],"name":"emitBatchMetadataUpdate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"minter","type":"address"}],"name":"getMintStats","outputs":[{"internalType":"uint256","name":"minterNumMinted","type":"uint256"},{"internalType":"uint256","name":"currentTotalSupply","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTransferValidationFunction","outputs":[{"internalType":"bytes4","name":"functionSignature","type":"bytes4"},{"internalType":"bool","name":"isViewFunction","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getTransferValidator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"__name","type":"string"},{"internalType":"string","name":"__symbol","type":"string"},{"internalType":"address[]","name":"allowedSeaDrop","type":"address[]"},{"internalType":"address","name":"initialOwner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"minter","type":"address"},{"internalType":"uint256","name":"quantity","type":"uint256"}],"name":"mintSeaDrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"contractURI","type":"string"},{"internalType":"address","name":"seaDropImpl","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct PublicDrop","name":"publicDrop","type":"tuple"},{"internalType":"string","name":"dropURI","type":"string"},{"components":[{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"string[]","name":"publicKeyURIs","type":"string[]"},{"internalType":"string","name":"allowListURI","type":"string"}],"internalType":"struct AllowListData","name":"allowListData","type":"tuple"},{"internalType":"address","name":"creatorPayoutAddress","type":"address"},{"internalType":"bytes32","name":"provenanceHash","type":"bytes32"},{"internalType":"address[]","name":"allowedFeeRecipients","type":"address[]"},{"internalType":"address[]","name":"disallowedFeeRecipients","type":"address[]"},{"internalType":"address[]","name":"allowedPayers","type":"address[]"},{"internalType":"address[]","name":"disallowedPayers","type":"address[]"},{"internalType":"address[]","name":"tokenGatedAllowedNftTokens","type":"address[]"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint8","name":"dropStageIndex","type":"uint8"},{"internalType":"uint32","name":"maxTokenSupplyForStage","type":"uint32"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct TokenGatedDropStage[]","name":"tokenGatedDropStages","type":"tuple[]"},{"internalType":"address[]","name":"disallowedTokenGatedAllowedNftTokens","type":"address[]"},{"internalType":"address[]","name":"signers","type":"address[]"},{"components":[{"internalType":"uint80","name":"minMintPrice","type":"uint80"},{"internalType":"uint24","name":"maxMaxTotalMintableByWallet","type":"uint24"},{"internalType":"uint40","name":"minStartTime","type":"uint40"},{"internalType":"uint40","name":"maxEndTime","type":"uint40"},{"internalType":"uint40","name":"maxMaxTokenSupplyForStage","type":"uint40"},{"internalType":"uint16","name":"minFeeBps","type":"uint16"},{"internalType":"uint16","name":"maxFeeBps","type":"uint16"}],"internalType":"struct SignedMintValidationParams[]","name":"signedMintValidationParams","type":"tuple[]"},{"internalType":"address[]","name":"disallowedSigners","type":"address[]"}],"internalType":"struct ERC721SeaDropStructsErrorsAndEvents.MultiConfigureStruct","name":"config","type":"tuple"}],"name":"multiConfigure","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"provenanceHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"royaltyAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"royaltyBasisPoints","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"_salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint256","name":"royaltyAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newBaseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newContractURI","type":"string"}],"name":"setContractURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"setMaxSupply","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"newProvenanceHash","type":"bytes32"}],"name":"setProvenanceHash","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"royaltyAddress","type":"address"},{"internalType":"uint96","name":"royaltyBps","type":"uint96"}],"internalType":"struct ISeaDropTokenContractMetadata.RoyaltyInfo","name":"newInfo","type":"tuple"}],"name":"setRoyaltyInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newValidator","type":"address"}],"name":"setTransferValidator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPotentialOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"components":[{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"string[]","name":"publicKeyURIs","type":"string[]"},{"internalType":"string","name":"allowListURI","type":"string"}],"internalType":"struct AllowListData","name":"allowListData","type":"tuple"}],"name":"updateAllowList","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"feeRecipient","type":"address"},{"internalType":"bool","name":"allowed","type":"bool"}],"name":"updateAllowedFeeRecipient","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"allowedSeaDrop","type":"address[]"}],"name":"updateAllowedSeaDrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"payoutAddress","type":"address"}],"name":"updateCreatorPayoutAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"string","name":"dropURI","type":"string"}],"name":"updateDropURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"payer","type":"address"},{"internalType":"bool","name":"allowed","type":"bool"}],"name":"updatePayer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct PublicDrop","name":"publicDrop","type":"tuple"}],"name":"updatePublicDrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"signer","type":"address"},{"components":[{"internalType":"uint80","name":"minMintPrice","type":"uint80"},{"internalType":"uint24","name":"maxMaxTotalMintableByWallet","type":"uint24"},{"internalType":"uint40","name":"minStartTime","type":"uint40"},{"internalType":"uint40","name":"maxEndTime","type":"uint40"},{"internalType":"uint40","name":"maxMaxTokenSupplyForStage","type":"uint40"},{"internalType":"uint16","name":"minFeeBps","type":"uint16"},{"internalType":"uint16","name":"maxFeeBps","type":"uint16"}],"internalType":"struct SignedMintValidationParams","name":"signedMintValidationParams","type":"tuple"}],"name":"updateSignedMintValidationParams","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"allowedNftToken","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint8","name":"dropStageIndex","type":"uint8"},{"internalType":"uint32","name":"maxTokenSupplyForStage","type":"uint32"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct TokenGatedDropStage","name":"dropStage","type":"tuple"}],"name":"updateTokenGatedDrop","outputs":[],"stateMutability":"nonpayable","type":"function"}]
with open('contracts/SeaDrop.json','r') as f:
    contract_json=json.load(f)
#实例化以上合约
class OpenSeaBot(BaseBot):
    def _init_contract(self):
        self.nft_manager=self.web3.eth.contract(address=contract_json['address'],abi=contract_json['abi'])
        self.nft_contract=self.web3.eth.contract(address=Web3.to_checksum_address(nft721),abi=abi)
    def __init__(self, account, web3, config: Config):
        super().__init__(account, web3, config)
        self._init_contract()
        self.main_wallet=self.web3.eth.account.from_key(self.config.main_wallet_private_key)
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
    
    def mint_nft(self):
        if self.account.get('mint'):
            logger.warning(f"账户:{self.wallet.address},已经mint过,跳过")
            return
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance==0:
            logger.warning(f"账户:{self.wallet.address},余额不足,跳过")
            return
        logger.info(f"账户:{self.wallet.address},铸造中...")
        func=self.nft_manager.functions.mintPublic(
            '0x071126cBec1C5562530Ab85fD80dd3e3a42A70B8',
            '0x0000a26b00c1F0DF003000390027140000fAa719',
            '0x0000000000000000000000000000000000000000',
            1, 
        )
        tx=func.build_transaction({
            'from':self.wallet.address,
            'nonce':self.web3.eth.get_transaction_count(self.wallet.address),
            'gasPrice':self.web3.eth.gas_price,
        })
        signed_txn = self.wallet.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:{self.wallet.address},mint成功")
            self.account['mint']=True
            self.config.save_accounts()
        else:
            logger.error(f"账户:{self.wallet.address},,mint失败,原因:{receipt}")
   
    def get_token_ids(self):
        # 构建事件查询参数
        event_signature = self.web3.keccak(text="Transfer(address,address,uint256)").hex()
        
        # 构造查询过滤器
        filter_params = {
            "fromBlock": 0,
            "toBlock": "latest",
            "address": Web3.to_checksum_address(nft721),
            "topics": [
                event_signature,
                None,  # from地址
                Web3.to_hex(Web3.to_bytes(hexstr=self.wallet.address).rjust(32, b'\0'))  # to地址
            ]
        }

        # 直接获取日志
        logs = self.web3.eth.get_logs(filter_params)
        
        # 解析日志
        token_ids = []
        for log in logs:
            event_data = self.nft_contract.events.Transfer().process_log(log)
            token_id = event_data.args.tokenId
            token_ids.append(token_id)
        
        return token_ids
    def transfer_nft(self) :
        if self.account.get('transfer'):
            logger.warning(f"账户:{self.wallet.address},已经transfer过,跳过")
            return
        # 通过self.box_nft_contract 查询box数量
        nft_count=self.nft_contract.functions.balanceOf(self.wallet.address).call()
        if nft_count==0:
            logger.warning(f"账户:{self.wallet.address},没有box,跳过")
            return
        logger.info(f"账户:{self.wallet.address},transfer中...")
        token_ids=self.get_token_ids()
        for token_id in token_ids:
            func=self.nft_contract.functions.safeTransferFrom(self.wallet.address,self.main_wallet.address,token_id)
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
                logger.success(f"账户:{self.wallet.address},transfer nft 成功")
                self.account['transfer']=True
                self.config.save_accounts()
            else:
                logger.error(f"账户:{self.wallet.address},transfer nft 失败,原因:{receipt}")
    def transfer_eth(self):
        if self.account.get('transfer_eth'):
            logger.warning(f"账户:{self.wallet.address},已经transfer过,跳过")
            return
        # 从主地址转账随机余额（0.12-0.13）到钱包地址，如果余额大于等于0.12eth则跳过
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance>self.web3.to_wei(0.000002,'ether'):
            logger.warning(f"账户:{self.wallet.address},余额足够,跳过")
            return
        logger.info(f"账户:{self.wallet.address},转账中...")
        with lock:
            transaction={
                'from': self.main_wallet.address,
                'to': self.wallet.address,
                'value': self.web3.to_wei(random.uniform(0.000002,0.0000021),'ether'),
                'gasPrice': self.web3.eth.gas_price, 
                'gas': 100000,
                'nonce': self.web3.eth.get_transaction_count(self.main_wallet.address),
            } 
            tx_hash = send_transaction(self.web3, transaction, self.main_wallet.key)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                logger.success(f"账户:{self.wallet.address},转账成功")
                self.account['transfer_eth']=True
                self.config.save_accounts()
            else:
                logger.error(f"账户:{self.wallet.address},转账失败,原因:{receipt}")

class OpenSeaManager(BaseBotManager):
    def run_single(self,account):
        bot=OpenSeaBot(account,self.web3,self.config)
        bot.transfer_eth()
        time.sleep(5)
        bot.mint_nft()
        time.sleep(5)
        bot.transfer_nft()
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.exception(f"执行过程中发生错误: {e}")

    