import{c as a}from"./chunk-452U5DPK.js";import{m as f}from"./chunk-AHWM6USP.js";import{bc as R}from"./chunk-TYUTKD3A.js";import{a as N}from"./chunk-DM24NLHH.js";import{F as m,pa as h}from"./chunk-5BQQ5BTM.js";import{a as B}from"./chunk-WQYVBC56.js";import{f as o,m as s,o as u}from"./chunk-CS4SUKWE.js";s();u();var t=o(B()),i=o(R());h();var p=o(N());var y=20*1e3,E=b=>{let k=(0,i.useDispatch)(),c=f(void 0,b),r=(0,t.useRef)(null);(0,t.useEffect)(()=>{let n=()=>{clearInterval(r.current),r.current=null},l=async()=>{try{let e=await c();if(m(e)){n();return}let d=await(0,p.default)(e.eth.getBlockNumber)();k(a(d))}catch(e){console.log(`fetch block failed 
${e}`)}};return l(),r.current=setInterval(()=>{l()},y),()=>{n()}},[c])},I=E;export{I as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-GMPC5KEE.js.map
