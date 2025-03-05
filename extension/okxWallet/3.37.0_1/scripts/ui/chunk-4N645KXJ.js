import{d as i}from"./chunk-CHLBHCPL.js";import{m as n,o as e}from"./chunk-CS4SUKWE.js";n();e();n();e();async function o({action:t,params:a,maxSize:g=500}){try{let s=await Promise.resolve(i.log),r=await s.get(t)||{a:t,d:[]};Array.isArray(r?.d)||(r.d=[]);let c=r.d,l={t:new Date().toLocaleString(),p:a};c.unshift(l),g&&c.splice(g),await s.set(r)}catch{console.log("set data failed")}}async function y(t){return(await Promise.resolve(i.log)).query(t)}var L=t=>o({action:"pv",params:t}),h=t=>o({action:"pms",params:t}),A=t=>o({action:"pc",params:t});var P=t=>o({action:"pr",params:t,maxSize:50});export{y as a,L as b,h as c,A as d,P as e};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-4N645KXJ.js.map
