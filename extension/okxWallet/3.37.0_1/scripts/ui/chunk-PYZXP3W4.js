import{a as d}from"./chunk-QDNQKTGP.js";import{r as m}from"./chunk-TYUTKD3A.js";import{c as a,f as y}from"./chunk-V2SICOMY.js";import{Fc as u,Ga as f,Gc as I,Oc as P,Xa as g,xa as c}from"./chunk-QWQGBYOY.js";import{m as p,o as C}from"./chunk-CS4SUKWE.js";p();C();P();g();function B({coin:i,walletIdentity:e,options:o={}}){let{needFilterBaseCoin:t=!1,isKeystone:n,isMPC:r,isHardWallet:s}=o,W=n??a(e?.initialType),F=s??y(e?.keyringIdentityType),l=r??d(e?.keyringIdentityType);return!l&&!F?!0:t&&m(i)?!!l:W&&i.baseCoinId===c&&i.coinId===f?!1:l?!Object.values(I).includes(i.protocolId):!Object.values(u).includes(i.protocolId)}function O({coins:i=[],walletIdentity:e,options:o={}}){let t=a(e?.initialType),n=y(e?.keyringIdentityType),r=d(e?.keyringIdentityType);return i.filter(s=>B({coin:s,walletIdentity:e,options:{...o,isMPC:r,isHardWallet:n,isKeystone:t}}))}export{B as a,O as b};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-PYZXP3W4.js.map
