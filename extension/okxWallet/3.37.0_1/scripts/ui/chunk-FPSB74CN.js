import{e as L}from"./chunk-METSMHFB.js";import{c as y,m as x,o as I}from"./chunk-CS4SUKWE.js";var v=y((f,w)=>{"use strict";x();I();var a=L().Buffer,l=9007199254740991;function d(t){if(t<0||t>l||t%1!==0)throw new RangeError("value out of range")}function n(t,e,i){if(d(t),e||(e=a.allocUnsafe(U(t))),!a.isBuffer(e))throw new TypeError("buffer must be a Buffer instance");return i||(i=0),t<253?(e.writeUInt8(t,i),n.bytes=1):t<=65535?(e.writeUInt8(253,i),e.writeUInt16LE(t,i+1),n.bytes=3):t<=4294967295?(e.writeUInt8(254,i),e.writeUInt32LE(t,i+1),n.bytes=5):(e.writeUInt8(255,i),e.writeUInt32LE(t>>>0,i+1),e.writeUInt32LE(t/4294967296|0,i+5),n.bytes=9),e}function r(t,e){if(!a.isBuffer(t))throw new TypeError("buffer must be a Buffer instance");e||(e=0);var i=t.readUInt8(e);if(i<253)return r.bytes=1,i;if(i===253)return r.bytes=3,t.readUInt16LE(e+1);if(i===254)return r.bytes=5,t.readUInt32LE(e+1);r.bytes=9;var E=t.readUInt32LE(e+1),s=t.readUInt32LE(e+5),c=s*4294967296+E;return d(c),c}function U(t){return d(t),t<253?1:t<=65535?3:t<=4294967295?5:9}w.exports={encode:n,decode:r,encodingLength:U}});export{v as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-FPSB74CN.js.map
