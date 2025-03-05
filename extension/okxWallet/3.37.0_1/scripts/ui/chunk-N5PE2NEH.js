import{a as M}from"./chunk-F7IOPQEO.js";import{a as P}from"./chunk-WQYVBC56.js";import{f as m,m as o,o as n}from"./chunk-CS4SUKWE.js";o();n();var a=m(P()),f=m(M());o();n();function c(e){if(!e)return{};let{pathname:t,search:r,hash:s}=e,h=new URLSearchParams(r),i=new URLSearchParams(s.slice(1)),u=t?.includes("/sell"),p=t?.includes("/buy");return{isSellRoute:u,isBuyRoute:p,path:t,queryParams:h,hashParams:i}}function S(){let e=(0,f.useLocation)(),[t,r]=(0,a.useState)({});return(0,a.useEffect)(()=>{if(e){let s=c(e);r(s)}},[e]),t}export{S as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-N5PE2NEH.js.map
