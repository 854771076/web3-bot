import{d as u}from"./chunk-4AVGLJGA.js";import{o as b}from"./chunk-DD3BDKUM.js";import{Hb as s,dc as l,fc as B}from"./chunk-QWQGBYOY.js";import{f,m as a,o as c}from"./chunk-CS4SUKWE.js";a();c();var i=f(b());B();a();c();var p=(...n)=>{let e=n.shift();return(...r)=>e?n.reduce((t,o)=>o(t),e(...r)):null},A=(...n)=>async(...e)=>n.slice(1).reduce((t,o)=>t.then(m=>o(m)),Promise.resolve(n[0](...e))),h=()=>{throw new Error};function x(n,e,r){let t={coinId:e,coinAmount:0,coinAmountInt:0,currencyAmount:0};return!Array.isArray(n)||!n?.length||(r?t=n.find(o=>+o.coinId==+e&&+o.addressType==+r)||{}:t=n.find(o=>+o.coinId==+e)||{}),t}function C(n,e){let r=u();return(0,i.useCreation)(()=>x(r,n,e),[r,n,e])}var I=(n={})=>{let e=n.coinAmountInt||0;return String(e)},v=n=>{let e=C(n);return I(e)},D=(n,e)=>p(s,l)(n,10**e);var k=()=>{let n=u();return(0,i.useMemoizedFn)(e=>n.find(t=>t.coinId===+e)||{})},z=n=>{let e=u();return n.map(t=>e.find(o=>o.coinId===+t)||{})};export{p as a,A as b,h as c,x as d,C as e,v as f,D as g,k as h,z as i};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-HN3RS7KM.js.map
