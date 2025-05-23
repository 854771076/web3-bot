from core.bot.basebot import *
from core.config import Config
from threading import Lock
import hashlib
import hmac
from urllib.parse import urlparse, urlencode
lock=Lock()
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
def c():
    def inner(e, r):
        key = r.encode('utf-8')
        srcs = e.encode('utf-8')
        encrypted = hmac.new(key, srcs, hashlib.sha256).hexdigest()
        return encrypted
    return inner

def a():
    def inner(e):
        srcs = e.encode('utf-8')
        encrypted = hashlib.md5(srcs).hexdigest()
        return encrypted
    return inner

def get_signature(url, params=None):
    result = {}
    n = str(time.time())
    parsed_url = urlparse(url)
    o = parsed_url.path

    if params:
        filtered_params = {k: v for k, v in params.items() if v is not None}
        if filtered_params:
            query_string = urlencode(filtered_params)
            o += f"?{query_string}"

    result["X-API-Timestamp"] = n

    hmac_func = c()
    i = hmac_func(f"36657-{n}", "monad-secret")
    s = ''.join([i[e] for e in range(1, len(i), 2)])
    result["X-APP-ID"] = s

    md5_func = a()
    l = md5_func(o + s + str(n))
    u = ''.join([l[e + 1] + l[e] for e in range(0, len(l), 2)])
    result["X-API-Signature"] = u

    return result
ERC20_ABI=open('./contracts/ERC20.json').read()
nfts={
    '0x0768BDD56A00Fe7E18A91033d4b84Ddbb74d0201':[{"inputs":[{"internalType":"address","name":"initialOwner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ERC721EnumerableForbiddenBatchMint","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721IncorrectOwner","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721InsufficientApproval","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC721InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"ERC721InvalidOperator","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721InvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC721InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC721InvalidSender","type":"error"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721NonexistentToken","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"ERC721OutOfBoundsIndex","type":"error"},{"inputs":[],"name":"EnforcedPause","type":"error"},{"inputs":[],"name":"ExpectedPause","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"numberOfTokens","type":"uint256"}],"name":"batchMint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isMintFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mintNFTForOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"price","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"safeMint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_isMintFee","type":"bool"}],"name":"setMintFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newPrice","type":"uint256"}],"name":"updatePrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}],
    '0xf38c90BbECeE227a7Ae153B1fA4c7216292C8b61':[{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"}],"name":"ERC1967InvalidImplementation","type":"error"},{"inputs":[],"name":"ERC1967NonPayable","type":"error"},{"inputs":[],"name":"ERC721EnumerableForbiddenBatchMint","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721IncorrectOwner","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721InsufficientApproval","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC721InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"ERC721InvalidOperator","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"ERC721InvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC721InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC721InvalidSender","type":"error"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ERC721NonexistentToken","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"ERC721OutOfBoundsIndex","type":"error"},{"inputs":[],"name":"EnforcedPause","type":"error"},{"inputs":[],"name":"ExpectedPause","type":"error"},{"inputs":[],"name":"FailedCall","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[],"name":"ReentrancyGuardReentrantCall","type":"error"},{"inputs":[],"name":"UUPSUnauthorizedCallContext","type":"error"},{"inputs":[{"internalType":"bytes32","name":"slot","type":"bytes32"}],"name":"UUPSUnsupportedProxiableUUID","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"MetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardsClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"StakeNft","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"UnstakeNft","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"UPGRADE_INTERFACE_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"admin","type":"address"}],"name":"addAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"admins","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"alreadyClaimed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"numberOfTokens","type":"uint256"}],"name":"batchMint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"calculateReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"calculateTotalRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"checkRewardedTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"claimMint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"nftStakedCount","type":"uint256"},{"internalType":"uint256","name":"totalRewards","type":"uint256"}],"name":"claimRewards","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"enableMaxMint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"getAllNFTs","outputs":[{"internalType":"uint256","name":"totalNFTs","type":"uint256"},{"internalType":"uint256[]","name":"ownedNFTs","type":"uint256[]"},{"internalType":"uint256[]","name":"stakedNFTs","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"getStakedNFTs","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"initialOwner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mintAndStake","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"mintAndStakePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mintNFTForOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"multiUnstake","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"payToMint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"payToStake","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"payToUnStake","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"price","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"receiveToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"admin","type":"address"}],"name":"removeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"safeMint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"sendToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenContractAddress","type":"address"}],"name":"setTokenContractAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokensRewardedPerHour","type":"uint256"}],"name":"setTokensRewardedPerHour","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"stakeNFT","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"stakePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"stakes","outputs":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"address","name":"owner","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"togglePayToMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"togglePayToStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"togglePayToUnStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenContractAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unStakePrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"unstake","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"unstakeMint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"_enable","type":"bool"}],"name":"updateEnableMaxMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_mintAndStakePrice","type":"uint256"}],"name":"updateMintAndStakePrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newPrice","type":"uint256"}],"name":"updatePrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newStakePrice","type":"uint256"}],"name":"updateStakePrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newUnStakePrice","type":"uint256"}],"name":"updateUnStakePrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"userMintedNfts","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"userStakedNfts","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"}],"name":"withdrawAllToAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawEth","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdrawToken","outputs":[],"stateMutability":"nonpayable","type":"function"}]
}    
SimpleERC721=json.loads(open('./contracts/SimpleERC721.json').read())    
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
        # 实例化nfts
        self.nfts={}
        for address,abi in nfts.items():
            self.nfts[address]=self.web3.eth.contract(address=Web3.to_checksum_address(address),abi=abi)
    def deplay_nft(self):
        """
        部署nft
        """
        try:
            if self.account.get('my_nft_address'):
                logger.info(f"账户:第{self.index}个地址,{self.wallet.address},已经部署nft")
                return
            # 生成随机的代币名称和符号
            token_name = ''.join(random.choices(string.ascii_uppercase, k=6))
            token_symbol = ''.join(random.choices(string.ascii_uppercase, k=3))
            address=deploy_contract(self.web3,self.wallet,SimpleERC721,(token_name,token_symbol),1,2000000)
            if address:
                logger.success(f"账户:第{self.index}个地址,{self.wallet.address},部署nft成功,地址:{address}")
                self.account['my_nft_address']=address
                self.config.save_accounts()
                contract=self.web3.eth.contract(address=Web3.to_checksum_address(address),abi=SimpleERC721['abi'])
                # safeMint(self,address,tokenId)
                tx = contract.functions.safeMint(self.wallet.address).build_transaction({
                    'from': self.wallet.address, 
                    'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
                    'gasPrice': self.web3.eth.gas_price,
                    'gas': 200000,  # 可以根据需要调整

                })
                tx_hash = send_transaction(self.web3, tx, self.wallet.key)
                receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
                if receipt.status == 1:
                    logger.success(f"账户:第{self.index}个地址,{self.wallet.address},铸造自己的nft成功")
                    self.account['my_nft_minted']=True
                    self.config.save_accounts()
                else:
                    logger.error(f"账户:第{self.index}个地址,{self.wallet.address},铸造自己的nft失败")
        except Exception as e:
            logger.exception(f"账户:第{self.index}个地址,{self.wallet.address},部署nft失败,{e}")

    def mint_other_nft(self):
        """
        铸造其他nft
        """
        try:
            address=random.choice([i.get('my_nft_address') for i in self.config.accounts if i.get('my_nft_address')])
            if not address:
                logger.warning(f"没有其他账户部署nft")
                return
            contract=self.web3.eth.contract(address=Web3.to_checksum_address(address),abi=SimpleERC721['abi'])
            tx = contract.functions.safeMint(self.wallet.address).build_transaction({
                'from': self.wallet.address,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
                'gasPrice': self.web3.eth.gas_price,
                'gas': 200000,  # 可以根据需要调整 
            })
            tx_hash = send_transaction(self.web3, tx, self.wallet.key)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                logger.success(f"账户:第{self.index}个地址,{self.wallet.address},铸造其他nft成功")
            else:
                logger.error(f"账户:第{self.index}个地址,{self.wallet.address},铸造其他nft失败")
        except Exception as e:
            logger.exception(f"账户:第{self.index}个地址,{self.wallet.address},铸造其他nft失败,{e}")
    def __init__(self, account, web3, config: Config):
        super().__init__(account, web3, config)
        self._init_contract()
        try:
            self.main_wallet=self.web3.eth.account.from_key(self.config.main_wallet_private_key)
        except:
            self.main_wallet=None
    def mint_nfts(self):
        """
        铸造nfts
        """
        for address,contract in self.nfts.items():
            if not self.account.get(f'{address}_minted'): 
                logger.info(f"账户:第{self.index}个地址,{self.wallet.address},铸造{address}中...")
                try:     
                    tx = contract.functions.safeMint(self.wallet.address).build_transaction({
                        'from': self.wallet.address,
                        'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
                        'gasPrice': self.web3.eth.gas_price,
                        'gas': 300000,  # 可以根据需要调整
                    })
                    tx_hash = send_transaction(self.web3, tx, self.wallet.key)
                    receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
                    if receipt.status == 1:
                        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},铸造{address}成功")
                        self.account[f'{address}_minted']=True
                        self.config.save_accounts()
                    else:
                        logger.exception(f"账户:第{self.index}个地址,{self.wallet.address},铸造{address}失败")
                except Exception as e:
                    logger.error(f"账户:第{self.index}个地址,{self.wallet.address},铸造{address}失败,{e}")
            else:
                logger.info(f"账户:第{self.index}个地址,{self.wallet.address},{address}已经铸造过,跳过")

    def get_token_info(self):
        """获取token信息"""
        url = 'https://monad-api.blockvision.org/testnet/api/account/tokenPortfolio'
        params = {
            'address': self.wallet.address,
        }
        headers=get_signature(url, params)
        try:
            response = self.session.get('https://monad-api.blockvision.org/testnet/api/account/tokenPortfolio', params=params, headers=headers)
            data=response.json()
        except Exception as e:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},获取token信息失败,{e}")
            return []
        if data.get('message')=='OK':
            self.tokens=response.json().get('result',{}).get('data')

        else:
            self.tokens=[]
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},获取token信息失败,{data.get('message')}")
        return self.tokens
    def transfer_token_other(self):
        
        
        random_private_key=self.config.get_random_private_key()
        random_address=self.web3.eth.account.from_key(random_private_key).address
        if not self.account.get('token_address'):
            tokens=[i for i in self.get_token_info() if i.get('contractAddress')!='0x0000000000000000000000000000000000000000']
            tokens=sorted(tokens,key=lambda x:float(x.get('balance')),reverse=True)
            if not tokens:
                logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},没有token,跳过")
                return
            token=tokens[0].get('contractAddress')
            self.account['token_address']=token
            self.config.save_accounts()
        else:
            token=self.account.get('token_address')
        contract_ERC20=self.web3.eth.contract(address=Web3.to_checksum_address(token),abi=ERC20_ABI)
        balance=contract_ERC20.functions.balanceOf(self.wallet.address).call()
        send_balance=balance*random.uniform(0.01,0.05)
            
        if not is_any_hours_away(self.account.get('last_token_transfer_time'),12):
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},12小时内已经token转账,跳过")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},随机token转账中...")
        transaction=contract_ERC20.functions.transfer(random_address,int(send_balance)).build_transaction({
            'from': self.wallet.address,
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
            'gasPrice': self.web3.eth.gas_price,
            'gas': 100000, 
        })
        
        tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},token转账成功")
            now=time.time()
            self.account['last_token_transfer_time']=now
            self.config.save_accounts()
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},token转账失败,原因:{receipt}")
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
    def get_verification_token(self,session):
        response = session.get('https://testnet.monad.xyz/')
        text=re.sub('\s','',response.text).replace('\\','')
        requestVerification=re.findall('requestVerification":(\\{.*?\\})',text)
        try:
            if requestVerification:
                data=json.loads(requestVerification[0])
                return {
                    'X-Request-Timestamp':data['timestamp'],
                    'X-Request-Verification-Token':data['token'],
                }
            else:
                return None
        except Exception as e:
            logger.error(e)
    def get_faucet(self):
        """获取faucet"""
        if not is_any_hours_away(self.account.get('last_faucet_time'),12):
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},faucet,跳过")
            return
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin': 'https://testnet.monad.xyz',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://testnet.monad.xyz/',
        }
        session=self.get_new_session(headers)
        # requestVerification=self.get_verification_token(session)
        # if requestVerification:
        #     headers.update(requestVerification)
        # else:
        #     return self.get_faucet()
        
        visitorId=''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
        token=get_cf_token(self.config.site,self.config.sitekey,method=self.config.cf_api_method,url=self.config.cf_api_url,authToken=self.config.cf_api_key)
        json_data = {
            'address': self.wallet.address,
            # 'visitorId': visitorId,
            'cloudFlareResponseToken': token,
        }
        session.headers.update({
           'x-fingerprint':visitorId 
        })
        try:
            response = session.post('https://faucet-claim.molandak.org/', headers=headers, json=json_data)
            response.raise_for_status()
        except Exception as e:
            
            if 'already claimed' in response.text.lower() or 'claimed already' in response.text.lower():
                logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},faucet,已经领取过")
                return
            else:
                logger.error(f"账户:第{self.index}个地址,{self.wallet.address},获取faucet失败,{e},{response.text}")
                time.sleep(3)
                self.get_faucet()
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},获取faucet,{response.text}")
        time.sleep(3)

        if 'success' in response.text.lower():
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},获取faucet成功")
            self.account['faucet']=True
            now=time.time()
            self.account['last_faucet_time']=now
            self.config.save_accounts()
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},获取faucet失败,{response.text}")
            time.sleep(3)
            self.get_faucet()
    def set_contract(self):
        if self.account.get('deployed'):
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},设置合约中...")
        compiled_contract=generate_random_erc20_contract()
        address=deploy_contract(self.web3,self.wallet,compiled_contract,(compiled_contract['total_supply'],),1,1000000)
        if address:
            logger.info(f'第{self.index}个地址,{self.wallet.address}-部署合约成功')
            self.account['deployed']=True
            self.config.save_accounts()
            return True
        else:
            logger.error(f'第{self.index}个地址,{self.wallet.address}-部署合约失败')
            return False
            
    def registe(self):
        if self.account.get('registed'):
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},注册中...")
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
        logger.success(f"账户:第{self.index}个地址,{self.wallet.address},注册成功")
    def mint_box(self):
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance<self.box_manager_contract.functions.BOX_PRICE().call():
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},余额不足,跳过")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},铸造中...")
        func=self.box_manager_contract.functions.mint(1,Web3.to_checksum_address(self.main_wallet.address))
        # gas=get_contract_transaction_gas_limit(self.web3, func, self.wallet.address)
        tx=func.build_transaction(
            {
                'from': self.wallet.address,
                'value': self.box_manager_contract.functions.BOX_PRICE().call(),
                'gasPrice': self.web3.eth.gas_price,
                'gas': 350000,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
            }
        )
        signed_txn = self.wallet.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},mint成功")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},,mint失败,原因:{receipt}")
    def transfer_MonAI(self) :
        # 通过self.MonAI_contract 查询数量
        MonAI_balance=self.MonAI_contract.functions.balanceOf(self.wallet.address).call()
        if MonAI_balance==0:
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},没有$MonAI,跳过")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},transfer中...")
        transaction=self.MonAI_contract.functions.transfer(self.main_wallet.address,MonAI_balance).build_transaction(
            {
                'from': self.wallet.address,
                'gasPrice': self.web3.eth.gas_price,
                'gas': 200000,
                'nonce': self.web3.eth.get_transaction_count(self.wallet.address),

            } 
        )
        tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},transfer $MonAI 成功")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},transfer $MonAI 失败,原因:{receipt}")
    
    def transfer_box(self) :
        # 通过self.box_nft_contract 查询box数量
        box_count=self.box_nft_contract.functions.balanceOf(self.wallet.address).call()
        if box_count==0:
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},没有box,跳过")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},transfer中...")
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
                logger.success(f"账户:第{self.index}个地址,{self.wallet.address},transfer box 成功")
            else:
                logger.error(f"账户:第{self.index}个地址,{self.wallet.address},transfer box 失败,原因:{receipt}")
    def transfer_eth(self):
        
        # 从主地址转账随机余额（0.12-0.13）到钱包地址，如果余额大于等于0.12eth则跳过
        balance=self.web3.eth.get_balance(self.wallet.address)
        if balance>self.web3.to_wei(0.12,'ether'):
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},余额足够,跳过")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},转账中...")
        with lock:
            transaction={
                'from': self.main_wallet.address,
                'to': self.wallet.address,
                'value': self.web3.to_wei(random.uniform(0.15,0.155),'ether'),
                'gasPrice': self.web3.eth.gas_price, 
                'gas': 200000,
                'nonce': self.web3.eth.get_transaction_count(self.main_wallet.address),
            } 
            tx_hash = send_transaction(self.web3, transaction, self.main_wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},转账成功")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},转账失败,原因:{receipt}")
    def transfer_eth_other(self,is_all=False,address=None):
        if address:
            random_address=address
        else:
            random_private_key=self.config.get_random_private_key()
            random_address=self.web3.eth.account.from_key(random_private_key).address
        balance=self.web3.eth.get_balance(self.wallet.address)
        balance_human=float(self.web3.from_wei(balance,'ether'))
        if balance_human<0.01:
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},余额不足,跳过")
            return
        if not is_any_hours_away(self.account.get('last_transfer_time'),12):
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},12小时内已经转账,跳过")
            return
        logger.info(f"账户:第{self.index}个地址,{self.wallet.address},随机转账中...")
        if is_all:
            send=balance_human-0.003
        else:
            send=random.uniform(balance_human*0.01,balance_human*0.05)
        if send>1:
            send=1
        transaction={
            'from': self.wallet.address,
            'to': Web3.to_checksum_address(random_address),
            'value': self.web3.to_wei(send,'ether'),
            'gasPrice': self.web3.eth.gas_price, 
            'gas': 50000,
            'nonce': self.web3.eth.get_transaction_count(self.wallet.address),
        } 
        tx_hash = send_transaction(self.web3, transaction, self.wallet.key)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},转账成功")
            now=time.time()
            self.account['last_transfer_time']=now
            self.config.save_accounts()
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},转账失败,原因:{receipt}")
    def checkin(self):
        if not is_any_hours_away(self.account.get('last_checkin_time'),12):
            logger.warning(f"账户:第{self.index}个地址,{self.wallet.address},12小时内已经checkin,跳过")
            return
        address='0xF33D3ff75a2fB1b6fF108b11F3a6F0Ad455d93F1'
        abi=[{'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'user', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'timestamp', 'type': 'uint256'}], 'name': 'CheckedIn', 'type': 'event'}, {'inputs': [], 'name': 'checkIn', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'getCheckIns', 'outputs': [{'internalType': 'uint256[]', 'name': '', 'type': 'uint256[]'}], 'stateMutability': 'view', 'type': 'function'}]
        contract=self.web3.eth.contract(address=address,abi=abi)
        func=contract.functions.checkIn()
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
            now=time.time()
            self.account['last_checkin_time']=now
            self.config.save_accounts()
            logger.success(f"账户:第{self.index}个地址,{self.wallet.address},checkin成功")
        else:
            logger.error(f"账户:第{self.index}个地址,{self.wallet.address},checkin失败,原因:{receipt}")
class MonadBotManager(BaseBotManager):
    def run_single(self,account):
        bot=MonadBot(account,self.web3,self.config)
        # bot.get_faucet()
        # try:
        #     bot.transfer_token_other()
        # except Exception as e:
        #     logger.error(f"账户:第{bot.index}个地址,{bot.wallet.address},transfer_token_other失败,原因:{e}")
        # bot.set_contract()
        bot.transfer_eth_other()
        # bot.checkin()
        # bot.mint_nfts()
        # bot.deplay_nft()
        # bot.mint_other_nft()

        # bot.registe()
        # bot.transfer_eth()
        # time.sleep(5)
        # bot.mint_box()
        # time.sleep(5)
        # bot.transfer_box()
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")

class MonadBotManager2(BaseBotManager):
    def run_single(self,account):
        bot=MonadBot(account,self.web3,self.config)
        bot.get_faucet()
        bot.transfer_eth_other(is_all=True,address='0x1e5f36cc94e30d31ea1f5a235aca673558edc574')
       
    def run(self):
        with ThreadPoolExecutor(max_workers=self.config.max_worker) as executor:
            futures = [executor.submit(self.run_single, account) for account in self.accounts]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"执行过程中发生错误: {e}")

    