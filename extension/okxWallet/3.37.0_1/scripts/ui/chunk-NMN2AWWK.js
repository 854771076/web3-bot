import{e as T}from"./chunk-4AVGLJGA.js";import{c as g,i as C}from"./chunk-64SQYTOJ.js";import{g as y}from"./chunk-NMBDO6HS.js";import{o as b}from"./chunk-DD3BDKUM.js";import{t as A}from"./chunk-TYUTKD3A.js";import{Xa as R,pa as s,uc as I,xc as S}from"./chunk-QWQGBYOY.js";import{o as u,pa as N}from"./chunk-5BQQ5BTM.js";import{f as w,m as p,o as f}from"./chunk-CS4SUKWE.js";p();f();N();R();S();var d=w(b());var z=(n,h)=>{let B=y(),a=h??B,l=T(a),i=(0,d.useCreation)(()=>l.find(t=>t.coinId===n?.coinId),[l,n?.coinId])?.childrenCoin??[],o=g(s,a),c=C(s,a);return(0,d.useCreation)(()=>{if(!n||!A(n)||!Array.isArray(i)||!Array.isArray(o)||!o.length)return[];let t=i.filter(r=>r.coinId===+n.coinId).map(r=>({...r})),m=[],e=u(t[0]||n),E=t.map(r=>c[r.addressType]);return o.forEach(({address:r,addressType:W})=>{E.includes(r)||(e.address=r,e.addressType=I[s][W],e.coinAmount=0,e.coinAmountInt=0,e.currencyAmount=0,e.currencyAmountUSD=0,m.push(u(e)))}),t.concat(m).filter(r=>Boolean(c[r.addressType]))},[n,i,o,c])};export{z as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-NMN2AWWK.js.map
