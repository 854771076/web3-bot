import{Gb as s,Lb as m,Mb as o,Nb as e,Pb as c,ec as i,fc as q}from"./chunk-QWQGBYOY.js";import{N as T,w as C}from"./chunk-4IQZG47E.js";import{m as l,o as w}from"./chunk-CS4SUKWE.js";l();w();T();q();var L=()=>{let n=C("extension_wallet_transaction_text_minute"),x=C("extension_wallet_transaction_text_second");return(t,r,d)=>{if(d)return`-- ${n}`;let a=i(t.minCost,n,x),_=i(t.normalCost,n,x),$=i(t.maxCost,n,x),u=`> 3 ${n}`,p=`> 10 ${n}`,S=`> 60 ${n}`;return c(r,t.min)?$:e(r,t.min)&&m(r,t.normal)?`< ${$}`:c(r,t.normal)?_:e(r,t.normal)&&m(r,t.max)?`< ${_}`:c(r,t.max)?a:e(r,t.max)?`< ${a}`:m(r,t.min)?o(r,s(t.min,.85))?S:o(r,s(t.min,.9))?p:(o(r,s(t.min,.95)),u):`-- ${n}`}};export{L as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-2OUKWBEW.js.map
