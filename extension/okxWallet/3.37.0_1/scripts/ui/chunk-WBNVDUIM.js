import{na as c,oa as u}from"./chunk-NC7RXVWZ.js";import{m as s,o}from"./chunk-CS4SUKWE.js";s();o();u();var L={light:"light",dark:"dark"},n=c({name:"activityBanners",initialState:{bannerList:[]},reducers:{setBannerList:(e,l)=>{let{allData:r,closedBanners:a,theme:d}=l.payload,i=r;a?.length>0&&(i=r.filter(t=>!a.find(g=>g===t.id))),e.bannerList=i.map(t=>({...t,img:d===L.dark?t.nightLogo:t.dayLogo}))}}}),{setBannerList:m}=n.actions,B=n.reducer,f=e=>e[n.name].bannerList;export{m as a,B as b,f as c};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-WBNVDUIM.js.map
