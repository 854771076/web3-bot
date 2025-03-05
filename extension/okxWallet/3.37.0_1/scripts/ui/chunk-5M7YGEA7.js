import{a as u}from"./chunk-Y4W36EYJ.js";import{a as s}from"./chunk-N5PE2NEH.js";import{b as n}from"./chunk-JJBV375X.js";import{k as r}from"./chunk-67OZVYSW.js";import{m,o as a}from"./chunk-CS4SUKWE.js";m();a();var B=(e=r)=>{let{isBuyRoute:p,queryParams:d}=s(),c=p||d?.get("tab")==="buy",{memeAccountStore:i,memeBuyStore:_,memeSellStore:l,memeQuoteStore:t}=n(),{chainId:k,chainName:o}=u(),g=i?.getAddressByChainId(k);return({button_name:y,custom_or_auto:f,popup_type:S,tab_name:h,type:T})=>{e&&e({button_name:y,custom_or_auto:f,popup_type:S,type:T,tab_name:h,wallet_address:g,from_token_address:t?.computedGetQuoteFrom?.tokenContractAddress,from_token_amount:t?.computedGetQuoteFromAmount,from_amount_usdt:t?.computedFromTokenValue,to_token_address:t?.computedGetQuoteTo?.tokenContractAddress,to_token_amount:t?.computedGetQuoteToAmount,to_amount_usdt:t?.computedToTokenValue,swap_type:"swap",balance_bracket:c?_?.fromToken?.amountNum:l?.toToken?.amountNum,slippage:{type:t?.slippage?.type,amount:t?.slippage?.value},trade_dialog:"no",from_chain:o,to_chain:o,chain:o})}};export{B as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-5M7YGEA7.js.map
