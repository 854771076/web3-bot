import{b as m}from"./chunk-TCSX4HQQ.js";import{k as p,l as a}from"./chunk-E5Q7T5U3.js";import{a as g}from"./chunk-QBSBGD35.js";import{a as S}from"./chunk-CHLBHCPL.js";import{mb as s,ob as f,vb as E}from"./chunk-QWQGBYOY.js";import{c as T,i as u,pa as l}from"./chunk-5BQQ5BTM.js";import{f as k,m as d,o as h}from"./chunk-CS4SUKWE.js";d();h();var e=k(S());l();E();var L=async o=>{let{Common:r,Hardfork:t}=await p();(0,e.isHexString)(u(o.chainId))&&(o.chainId=T(g(o.chainId)));let n=s({netWorkId:o.chainId})?.baseChain,i=()=>{let C=m(o.from,n),b=m(o.to,n);return{...o,from:C,to:b,gasLimit:o.gas||o.gasLimit}},c=s({netWorkId:o.chainId})?.localType||"custom-net",I=f(c)?.networkId||"custom-net",y={chainId:o.chainId,networkId:I,name:c},w={common:r.custom(y,{baseChain:n,hardfork:t.London})},{TransactionFactory:x}=await a();return x.fromTxData(i(),w)},N=async(o,r)=>{let t=o.toJSON();t.type=o.type;let{TransactionFactory:n}=await a(),i=n.fromTxData({...t,...r},{common:o.common,freeze:Object.isFrozen(o)});return(0,e.bufferToHex)(i.serialize())};export{L as a,N as b};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-SONOGRH4.js.map
