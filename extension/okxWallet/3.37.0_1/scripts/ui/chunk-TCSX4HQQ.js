import{e as l}from"./chunk-6H3Y45OD.js";import{Ya as m,eb as c,fb as u,mb as p,vb as A}from"./chunk-QWQGBYOY.js";import{b as v}from"./chunk-J52BXABX.js";import{f as y,m as r,n as i,o as e}from"./chunk-CS4SUKWE.js";r();e();A();r();e();var f=y(v());function I(t){return/^0x[0-9a-fA-F]{40}$/.test(t)}function s(t){try{let o=(0,f.toBech32)("one",i.Buffer.from(t.slice(2),"hex"));return o.length===42?o:t}catch{return t}}function x(t){try{let o=`0x${(0,f.fromBech32)(t)[1].toString("hex")}`;return I(o)?o:t}catch{return t}}r();e();function a(t){return/^0x[0-9a-fA-F]{40}$/.test(t)}function h(t){return a(t)?t.replace("0x","ronin:"):t}function T(t){let o=t.replace("ronin:","0x");return a(o)?o:t}var g=t=>!!l(t),F=(t,o,n={})=>{let C=typeof t=="string"&&typeof o=="string",E=n.baseCoinId||n.localType;if(!C||!E)return!1;let N=n.localType||p({coinId:n.baseCoinId})?.localType;return g(N)?t.toLowerCase()===o.toLowerCase():t===o},w=(t,o)=>o===c?T(t):o===u?x(t):t,S=(t,o)=>o===c?h(t):o===u?s(t):t,Y=t=>t===c||t===u?t:m;function j(t=""){return t.length<11?t:`${t.slice(0,6)}...${t.slice(-4)}`}export{F as a,w as b,S as c,Y as d,j as e};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-TCSX4HQQ.js.map
