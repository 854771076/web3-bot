import{d as r}from"./chunk-CHLBHCPL.js";import{a as l}from"./chunk-WQYVBC56.js";import{f as y,m as o,o as s}from"./chunk-CS4SUKWE.js";o();s();var i=y(l());var g=n=>{let[a,c]=(0,i.useState)({});return(0,i.useEffect)(()=>{let e;return(async()=>{let t=await Promise.resolve(r.extension_config),f=await t.get(n);c(f||{}),e=t.liveQuery({extensionKey:n}).subscribe((p,x)=>{!x&&p?.length&&c(p[0])})})(),()=>{e&&e?.unsubscribe()}},[n]),{extensionConfig:a,setExtensionConfig:async e=>{try{await(await Promise.resolve(r.extension_config)).set({...e,extensionKey:n})}catch{console.log("setRpcInfo fail")}}}};o();s();export{g as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-DFIMOBBJ.js.map
