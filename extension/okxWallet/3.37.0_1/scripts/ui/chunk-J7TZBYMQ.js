import{c as d,d as p}from"./chunk-XLNWZJIM.js";import{d as a}from"./chunk-ESXBSF3B.js";import{bc as v}from"./chunk-TYUTKD3A.js";import{H as r,o as m}from"./chunk-PLHFXPVU.js";import{N as g,w as e}from"./chunk-4IQZG47E.js";import{ca as o}from"./chunk-X62Q7VCJ.js";import{a as x}from"./chunk-WQYVBC56.js";import{f as s,m as _,o as c}from"./chunk-CS4SUKWE.js";_();c();var f=s(x()),t=s(v());g();function S(){let w=(0,t.useDispatch)(),{currentNetworkUniqueId:n}=(0,t.useSelector)(a),{deleteRpcNetwork:u}=p();return(0,f.useCallback)(({editRpcInfo:l,onDeleted:i})=>{if(d(l,{uniqueId:n})){r.error({title:e("developer_mode_network_toast_cannot_delete"),top:16});return}let k=m.warn({title:e("extension_wallet_network_modaltitle_delete_confirm"),text:e("extension_wallet_network_modaldesc_delete_confirm"),confirmText:e("extension_wallet_network_text_remove_network"),confirmBtnProps:{type:o.TYPE.red,size:o.SIZE.lg},cancelText:e("developer_mode_network_btn_botcancel"),alignBottom:!1,onConfirm:async()=>{await u(l),r.success(e("developer_mode_network_toast_delete_done")),k.destroy(),i&&i()}})},[w,n])}export{S as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-J7TZBYMQ.js.map
