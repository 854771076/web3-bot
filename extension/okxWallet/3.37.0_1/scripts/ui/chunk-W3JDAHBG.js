import{a as c}from"./chunk-E5Q7T5U3.js";import{cb as o}from"./chunk-TYUTKD3A.js";import{a as P}from"./chunk-CHLBHCPL.js";import{oc as m}from"./chunk-QWQGBYOY.js";import{f as d,m as s,o as n}from"./chunk-CS4SUKWE.js";s();n();var i=d(P());m();var h=async(t,e,r,a)=>{try{return await a(t,{privateKey:e,hrp:r}),!0}catch{return!1}},x=async(t,e)=>{let r=[],a=o(e),{getNewAddress:f}=await c();return await Promise.all(a.map(({coinType:p,cosmosPrefix:l,baseChain:u})=>h(p,t,l,f).then(y=>{y&&r.push(u)}))),r};var v=async(t,e)=>await x(t,e),C=async(t,e)=>{let r=await v(t,e);return Boolean(r[0])};export{v as a,C as b};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-W3JDAHBG.js.map
