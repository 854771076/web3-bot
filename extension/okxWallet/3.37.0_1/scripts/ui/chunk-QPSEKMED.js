import{a as L}from"./chunk-AR6XF3U7.js";import{c as e,d as o}from"./chunk-V5XRXBAE.js";import{h as f,n as l}from"./chunk-NMBDO6HS.js";import{Oc as _,zc as A}from"./chunk-QWQGBYOY.js";import{o as S}from"./chunk-PLHFXPVU.js";import{a as C}from"./chunk-WQYVBC56.js";import{f as T,m as n,o as c}from"./chunk-CS4SUKWE.js";n();c();n();c();var E=T(C());var w=({keyringId:u="",actionMap:r,customConfig:i})=>{let a=l(u),{accountStatus:t,mpcStatus:s}=a?.status||{},M=(0,E.useMemo)(()=>t===e.FROZEN||t===e.DELETE||s===o.ESCAPE||s===o.RECOVER,[t,s]),W=(0,E.useMemo)(()=>{let p,m;switch(!0){case s===o.RECOVER:p=r["RECOVER"],m=r["SWITCH_WALLET"];break;case s===o.ESCAPE:case t===e.FROZEN:case t===e.DELETE:p=r["SWITCH_WALLET"];break;default:break}return L({accountStatus:t,mpcStatus:s},{onConfirm:p,onCancel:m,...i})},[t,r,s]);return E.default.createElement(S.Prompt,{visible:M,...W})};n();c();_();var P=T(C()),K=u=>{let r=f(u),i=(0,P.useMemo)(()=>{let{accountStatus:a,mpcStatus:t}=r?.status||{accountStatus:e.NORMAL,mpcStatus:o.INIT};switch(!0){case t===o.RECOVER:case t===o.ESCAPE:case a===e.FROZEN:case a===e.DELETE:return!1;default:return!0}},[r]);return r?.keyringIdentityType!==A.MPC||i};export{w as a,K as b};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-QPSEKMED.js.map
