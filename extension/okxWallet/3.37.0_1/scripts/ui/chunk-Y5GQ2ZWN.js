import{b as c}from"./chunk-P6N6KWSS.js";import{g as u}from"./chunk-NMBDO6HS.js";import{o as k}from"./chunk-DD3BDKUM.js";import{Rc as m,Wc as W,Xc as a,Yc as _,lb as n,vb as C}from"./chunk-QWQGBYOY.js";import{j as i,pa as L}from"./chunk-5BQQ5BTM.js";import{N as b,n as f}from"./chunk-4IQZG47E.js";import{a as E}from"./chunk-WQYVBC56.js";import{f as r,m as o,o as s}from"./chunk-CS4SUKWE.js";o();s();var l=r(E()),p=r(k());L();b();C();_();W();var T="update_defi_list",M=()=>{let d=u(),I=n(),t=(0,p.useRequest)(async()=>{let D=await m(a.getDefiList,{accountId:d});return i(D,["data","platformListByAccountId","0","platformListVoList"],[]).filter(g=>I.find(h=>Number(h.netWorkId)===g.chainId))},{manual:!0}),e=c("invest-DeFi",{onError:t.refresh,pollingInterval:30*1e3});return(0,l.useEffect)(()=>{e&&t.refresh()},[e]),f.listen(T,t.refresh,!1),t};export{T as a,M as b};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-Y5GQ2ZWN.js.map
