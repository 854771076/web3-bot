import{e as B}from"./chunk-4AVGLJGA.js";import{c as T,h as y}from"./chunk-64SQYTOJ.js";import{g as C}from"./chunk-NMBDO6HS.js";import{o as j}from"./chunk-DD3BDKUM.js";import{s as I}from"./chunk-TYUTKD3A.js";import{X as s,Xa as O,uc as A,xc as S}from"./chunk-QWQGBYOY.js";import{o as d,pa as k}from"./chunk-5BQQ5BTM.js";import{f as b,m as p,o as f}from"./chunk-CS4SUKWE.js";p();f();var l=b(j());k();O();S();var G=(e,g)=>{let h=C(),a=g??h,u=B(a),i=(0,l.useCreation)(()=>u.find(t=>t.coinId===e?.coinId),[u,e?.coinId])?.childrenCoin??[],o=T(s,a),c=y(s,a);return(0,l.useCreation)(()=>{if(!e||!I(e)||!Array.isArray(i)||!Array.isArray(o)||!o.length)return[];let t=i.filter(r=>r.coinId===+e.coinId).map(r=>({...r})),m=[],n=d(t[0]||e),W=t.map(r=>c[r.addressType]);return o.forEach(({address:r,addressType:w})=>{W.includes(r)||(n.userAddress=r,n.address=r,n.addressType=A[s][w],n.coinAmount=0,n.coinAmountInt=0,n.currencyAmount=0,m.push(d(n)))}),t.concat(m).filter(r=>Boolean(c[r.addressType]))},[e,i,o,c])};export{G as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-6AMXLP7C.js.map
