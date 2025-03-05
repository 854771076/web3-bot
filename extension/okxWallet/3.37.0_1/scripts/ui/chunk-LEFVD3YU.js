import{q as o}from"./chunk-AACZ2HW4.js";import{N as w,w as A}from"./chunk-4IQZG47E.js";import{a as _}from"./chunk-X7RY3AWM.js";import{a as T}from"./chunk-WQYVBC56.js";import{f as m,m as s,o as r}from"./chunk-CS4SUKWE.js";s();r();var t=m(T()),e=m(_());w();s();r();var p={walletAsset:"_walletAsset_1rhpe_1",unsupport:"_unsupport_1rhpe_8"};var l=(0,t.memo)(f=>{let{isRpcMode:y,currentRpcNetwork:i,hiddenAssets:n,walletAsset:u,hiddenText:a,unsopportCurrentNetwork:d}=f,h=()=>d?A("extension_wallet_list_not_support",{network:i?.chainName}):n?a:u||`0 ${i?.symbol}`;return t.default.createElement(t.default.Fragment,null,y?t.default.createElement(o.Text,{ellipsis:!0,className:{[p.walletAsset]:!0,[p.unsupport]:d}},h()):t.default.createElement(o.DisplayAmount,{ellipsis:!0,mode:o.LEGAL,useApproximate:!1,hidden:n?a:!1,className:p.walletAsset},u))});l.defaultProps={hiddenText:"***"};l.propTypes={isRpcMode:e.default.bool.isRequired,hiddenAssets:e.default.bool.isRequired,walletAsset:e.default.oneOfType([e.default.string,e.default.number]).isRequired,hiddenText:e.default.string};var M=l;export{M as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-LEFVD3YU.js.map
