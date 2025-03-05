import{va as i,ya as n}from"./chunk-NC7RXVWZ.js";import{d as s,f as c}from"./chunk-DM24NLHH.js";import{G as o}from"./chunk-PLHFXPVU.js";import{m as a,o as d}from"./chunk-CS4SUKWE.js";a();d();c();n();async function p(e){try{return await s().addAddressBook(e)}catch(r){throw r?.message!==i&&o.error({title:r?.message}),r}}async function A(e,r){try{return await s().updateAddressBook(e,r)}catch(t){return o.error({title:t?.message}),t}}async function g(e){try{return await s().removeAddressBook(e)}catch(r){throw o.error({title:r?.message}),r}}async function k(e,r){try{return await s().addRecentlyAddress(e,r)}catch(t){return o.error({title:t?.message}),t}}export{p as a,A as b,g as c,k as d};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-VLSOWDRD.js.map
