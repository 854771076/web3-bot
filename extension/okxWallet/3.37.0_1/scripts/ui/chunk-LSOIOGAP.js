import{c as g,m as u,n,o as B}from"./chunk-CS4SUKWE.js";var a=g(o=>{"use strict";u();B();Object.defineProperty(o,"__esModule",{value:!0});var f;function s(e){{let t=n.Buffer.from(e);t.reverse();let r=t.toString("hex");return r.length===0?BigInt(0):BigInt(`0x${r}`)}return f.toBigInt(e,!1)}o.toBigIntLE=s;function c(e){{let t=e.toString("hex");return t.length===0?BigInt(0):BigInt(`0x${t}`)}return f.toBigInt(e,!0)}o.toBigIntBE=c;function l(e,t){{let r=e.toString(16),i=n.Buffer.from(r.padStart(t*2,"0").slice(0,t*2),"hex");return i.reverse(),i}return f.fromBigInt(e,n.Buffer.allocUnsafe(t),!1)}o.toBufferLE=l;function I(e,t){{let r=e.toString(16);return n.Buffer.from(r.padStart(t*2,"0").slice(0,t*2),"hex")}return f.fromBigInt(e,n.Buffer.allocUnsafe(t),!0)}o.toBufferBE=I});export{a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-LSOIOGAP.js.map
