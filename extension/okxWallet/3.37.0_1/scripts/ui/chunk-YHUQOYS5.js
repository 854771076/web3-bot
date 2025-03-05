import{e as p}from"./chunk-U65S63W6.js";import{d as m}from"./chunk-ESXBSF3B.js";import{Db as r,Eb as i,jb as g,lb as s,mb as l}from"./chunk-TYUTKD3A.js";import{m as c,o as d}from"./chunk-CS4SUKWE.js";c();d();var e={connect:"connect",transaction:"transaction",msg:"msg",addToken:"addToken",addChain:"addChain"};function a(n={}){let t=null,o=0;return Object.keys(n).forEach(f=>{let T=n[f];Array.isArray(T)&&T.forEach(u=>{let h=u.time||0;h>=o&&(t=f,o=h)})}),t}c();d();var U=n=>{let t=m(n)?.isRpcMode,o;return t?o=a({[e.connect]:p(n),[e.transaction]:s(n),[e.msg]:g(n),[e.addToken]:i(n),[e.addChain]:r(n)}):o=a({[e.connect]:p(n),[e.transaction]:l(n),[e.addToken]:i(n),[e.addChain]:r(n)}),o},q=n=>m(n)?.isRpcMode?p(n).length+s(n).length+g(n).length+i(n).length+r(n).length:p(n).length+l(n).length+i(n).length+r(n).length;export{e as a,U as b,q as c};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-YHUQOYS5.js.map
