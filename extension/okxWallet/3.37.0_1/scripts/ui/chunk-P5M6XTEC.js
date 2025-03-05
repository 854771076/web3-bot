import{o as T}from"./chunk-DD3BDKUM.js";import{J as D}from"./chunk-TYUTKD3A.js";import{e as l,ha as n,pa as x}from"./chunk-5BQQ5BTM.js";import{a as B}from"./chunk-WQYVBC56.js";import{f as I,m as b,o as y}from"./chunk-CS4SUKWE.js";b();y();var e=I(B()),s=I(T());x();var U=(E,O={wait:200,disabled:!1,fetchOnce:null,onFetchSuccess:()=>{},onFetchError:()=>{}})=>{let[g,d]=(0,e.useState)({}),[m,v]=(0,e.useState)(null),[w,{setTrue:S,setFalse:o}]=(0,s.useBoolean)(!0),[k,{setFalse:r}]=(0,s.useBoolean)(!0),{address:i,inputData:c,tokenAddress:a,coinId:F,value:h}=E,{wait:q,disabled:p,fetchOnce:t,onFetchSuccess:L,onFetchError:G}=O,A=async()=>{try{let u={coinId:F,value:h,address:i&&n(i),inputData:c&&n(c)};a&&(u.tokenAddress=n(a));let{data:f}=await D(u);d(f),t&&v(t),l(L)&&L()}catch{d(f=>({...f,queryGasLimitErrorUseDefault:!0})),l(G)&&G()}finally{o(),r()}},{run:P}=(0,s.useDebounceFn)(()=>{if(p){o(),r();return}if(t===m&&t!==null){o(),r();return}A()},{wait:q});return(0,e.useEffect)(()=>{S(),P()},[i,c,a,F,h,t,m,p]),[g,w,k]},C=U;export{C as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-P5M6XTEC.js.map
