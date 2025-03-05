import{a as p}from"./chunk-CKRUHP35.js";import{a as m}from"./chunk-BKLQOL2X.js";import{f as o,m as i,o as f}from"./chunk-CS4SUKWE.js";i();f();var c=o(p()),u=o(m());function x(e){return(typeof e=="string"||typeof e=="number")&&/^(-)?0x[0-9a-f]*$/i.test(e)}function g(e){try{return c.default.apply(null,arguments)}catch(n){throw new Error(`${n} Given value: "${e}"`)}}var N=function(e,n=!1){if(!e)return e;if(typeof e=="string"&&!x(e))throw new Error(`Given value "${e}" is not a valid hex string.`);let t=g(e);return n&&(t>Number.MAX_SAFE_INTEGER||t<Number.MIN_SAFE_INTEGER)?BigInt(t):t.toNumber()},a=e=>{e=u.default.encode(e);let n="";e=e.replace(/^(?:\x00)*/,""),e=e.split("").reverse().join(""),e=e.replace(/^(?:\x00)*/,""),e=e.split("").reverse().join("");for(let t=0;t<e.length;t++){let r=e.charCodeAt(t).toString(16);n+=r.length<2?`0${r}`:r}return`0x${n}`};function E(e){return(typeof e=="string"||typeof e=="number")&&/^(-0x|0x)?[0-9a-f]*$/i.test(e)}export{x as a,N as b,a as c,E as d};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-LINATLLG.js.map
