import{c as w}from"./chunk-Z6RMGQXT.js";import{l as f}from"./chunk-BNWEXJ7R.js";import{k as n}from"./chunk-HWYDZOOB.js";import{D as u,N as P}from"./chunk-4IQZG47E.js";import{a as i}from"./chunk-WQYVBC56.js";import"./chunk-56JXL4SQ.js";import{f as p,m as t,o as r}from"./chunk-CS4SUKWE.js";t();r();var h=p(i());t();r();var S=p(i());P();var d=()=>{let{accountStore:{computedAccountId:a},walletContractStore:{transactionPayload:o},swapStore:{setSolanaSwapParams:s,sendSolanaTransaction:c,solanaSwapParams:m}}=w();return(0,S.useMemo)(()=>{try{let e=o?.map(l=>l.payload.transaction),y=e.length>1;return{showDappInfo:!1,showSwitchNetwork:!1,walletId:a,method:"signAllTransactions",params:{message:e},source:"dex",onConfirm:async l=>{let[C]=await u(c({signedTransactions:l,txArray:o,enableJito:y,swapParams:m,walletId:a}));C||s(null)},onCancel:()=>{s(null),n.history?.goBack()}}}catch{return null}},[a,c,s,m,o])};var x=()=>{let{SolanaEntry:a}=n.components,o=d();return h.default.createElement(a,{...o})},J=f(x);export{J as default};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=Solana-HC2WEUBV.js.map
