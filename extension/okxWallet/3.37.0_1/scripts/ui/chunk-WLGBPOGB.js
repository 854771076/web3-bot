import{d as l}from"./chunk-CBYWE4ZS.js";import{b as p}from"./chunk-TGTCJHHS.js";import{ob as m}from"./chunk-TYUTKD3A.js";import{y}from"./chunk-WOHVJ5VI.js";import{d as o,f as S}from"./chunk-DM24NLHH.js";import{u as T}from"./chunk-Z6Y7MSRE.js";import{Ya as u,_a as d,vb as W}from"./chunk-QWQGBYOY.js";import{m as w,o as f}from"./chunk-CS4SUKWE.js";w();f();W();S();var _=({txData:n,txParams:e,walletId:t,isRpcMode:r=!1,baseChain:a=u})=>async(s,i)=>{let c=i();t??=m(c);let g=await o().getWallet(t);p(g?.initialType)&&await l({walletInfo:g,txData:n,txParams:e,isRpcMode:r,baseChain:a})};async function I(n,e,t,r,{...a}={}){let s="";r??=await o().getWalletIdByAddress(e,t);let i=await o().getWallet(r);try{if(p(i?.initialType))return s=await l({walletInfo:i,txParams:n,baseChain:t}),s;s=await o().signTransaction(n,e,t,r,a)}catch(c){throw c?.message===T?c:new Error(y)}return s}function k(n,e,t){return async()=>I(n,e,d,t)}function v(n,e,t,r,a){return o().signPsbt(n,e,t,r,a)}export{_ as a,I as b,k as c,v as d};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-WLGBPOGB.js.map
