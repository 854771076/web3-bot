function z(e) {
    var t = (new Date).getTime() % 10
      , n = (new TextEncoder).encode(e)
      , r = n.length + 4
      , o = new Uint8Array(r);
    o[0] = r >> 16 & 255,
    o[1] = r >> 8 & 255,
    o[2] = 255 & r,
    o[3] = t;
    for (var i = 0; i < n.length; i++)
        o[4 + i] = n[i] - t;
    return o
}
function G(e) {
    var t = new Array(4);
    return t[0] = e >> 24 & 255,
    t[1] = e >> 16 & 255,
    t[2] = e >> 8 & 255,
    t[3] = 255 & e,
    t
}
q = function(e) {
    var t = (new Date).getTime()
      , n = [].concat((0,
    O.A)(function(e) {
        var t = new Array(2);
        return t[0] = e >> 8 & 255,
        t[1] = 255 & e,
        t
    }(0)), (0,
    O.A)(G(Math.floor(t / 1e3))))
      , r = e.uuid
      , o = e.deviceInfo
      , i = [].concat((0,
    O.A)(z("".concat(r, "o0"))), (0,
    O.A)(z("".concat(o, "v5"))))
      , a = function(e, t) {
        for (var n = 0, r = 0; r < e.length; r++)
            n += e[r];
        return n & t
    }(i, 4095);
    return n.push.apply(n, (0,
    O.A)(G(a))),
    n.push.apply(n, (0,
    O.A)(G(i.length))),
    n.push(4),
    n.push(0, 0, 0, 0, 0, 0, 0, 0, 0),
    n.push.apply(n, (0,
    O.A)(i)),
    n
}
var B = function(e, t, n) {
    (function() {
        return j.apply(this, arguments)
    }
    )().then((function(r) {
        var o = e.length
          , i = r._malloc(o);
        r.HEAPU8.set(e, i);
        var a = r.cwrap("getDataV2", null, ["number", "number", "number"])(i, o)
          , c = Module.UTF8ToString(a);
        r._free(i),
        r._free(a),
        n && n(e, c, t)
    }
    )).catch((function(e) {
        var n = t.devId;
        W.v.info("[FP_ID][Refresh_ERROR][LOAD_WASM_ERROR]:".concat(n), {
            err: e,
            customConfig: F.Xz
        })
    }
    ))
}
X = function(e, t, n) {
    var r = n.tmxSessionId
      , o = n.devId
      , i = JSON.parse(t)
      , a = (new Date).getTime()
      , s = c.A.init({
        project: "nav"
    })
      , u = s.get("reTmxSession") || {};
    if (s.get("postFpPending"))
        W.v.info("[FP_ID][Refresh_Pending]:".concat(o), {
            tmx_session_id: r,
            customConfig: F.Xz
        });
    else {
        s.set("postFpPending", 1, 40);
        var f = 2
          , g = function() {
            m.post("/priapi/v1/dis/dim", {
                st: i.timestamp,
                et: i.data,
                sid: r,
                pm: "3"
            }, {
                timeout: 15e3
            }).then((function(e) {
                var t = e.data
                  , n = t.fingerprintId
                  , i = t.status
                  , g = t.efp
                  , h = void 0 === g ? "" : g;
                w.A.set("fingerprint_id", n, (0,
                d.A)({}, _(7))),
                l().fp && l().fp.setEfpid && h && l().fp.setEfpid(h),
                w.A.set("fp_s", i, (0,
                d.A)({}, _(1))),
                u.inHouseDone = !0,
                s.set("reTmxSession", u),
                c.A.g.set("lastDevId", o);
                var v = s.get("inHouseData") || [];
                0 === v.length ? (v[0] = o,
                s.set("inHouseData", v)) : v[0] !== o && (W.v.info("[FP_ID][Refresh]:".concat(o), {
                    tmx_session_id: r,
                    retry_count: 2 - f,
                    request_at: a,
                    response_at: (new Date).getTime(),
                    customConfig: F.Xz
                }),
                v[0] = o,
                s.set("inHouseData", v))
            }
            )).catch((function(e) {
                f > 0 ? (f--,
                setTimeout(g, 1e3)) : (W.v.info("[FP_ID][Refresh_ERROR]:".concat(o), {
                    err: e,
                    customConfig: F.Xz
                }),
                w.A.set("fp_s", 3, (0,
                d.A)({}, _(1))))
            }
            )).finally((function() {
                s.remove("postFpPending")
            }
            ))
        };
        g()
    }
}
H = function() {
    var e = (0,
    i.A)((0,
    o.A)().mark((function e() {
        var t, r, a, u, f, g = arguments;
        return (0,
        o.A)().wrap((function(e) {
            for (; ; )
                switch (e.prev = e.next) {
                case 0:
                    return t = g.length > 0 && void 0 !== g[0] ? g[0] : "",
                    r = c.A.g.get("lastDevId"),
                    e.next = 4,
                    l().getDevId();
                case 4:
                    a = e.sent,
                    u = r === a,
                    (f = localStorage.getItem(M.C.FOT)) || (f = Date.now(),
                    localStorage.setItem(M.C.FOT, f)),
                    Promise.all([n.e(5271), n.e(4121), n.e(9665)]).then(n.bind(n, 9665)).then((function(e) {
                        (0,
                        e.default)(a).then(function() {
                            var e = (0,
                            i.A)((0,
                            o.A)().mark((function e(n) {
                                var r, i, s, u, f;
                                return (0,
                                o.A)().wrap((function(e) {
                                    for (; ; )
                                        switch (e.prev = e.next) {
                                        case 0:
                                            return i = (null === (r = c.A.g.get("profile")) || void 0 === r ? void 0 : r.uuid) || "",
                                            e.next = 3,
                                            l().crypto.jwt.getPublicKey();
                                        case 3:
                                            s = e.sent,
                                            u = {
                                                uuid: i,
                                                platform: "browser",
                                                deviceInfo: JSON.stringify((0,
                                                d.A)((0,
                                                d.A)({}, n), {}, {
                                                    pk: s
                                                }))
                                            },
                                            f = q(u),
                                            B(f, {
                                                tmxSessionId: t,
                                                devId: a
                                            }, X);
                                        case 7:
                                        case "end":
                                            return e.stop()
                                        }
                                }
                                ), e)
                            }
                            )));
                            return function(t) {
                                return e.apply(this, arguments)
                            }
                        }()).catch((function(e) {
                            W.v.info("[fingerprint][Get_Data_Error] ".concat(a), {
                                err: e,
                                customConfig: F.Xz
                            })
                        }
                        )),
                        u !== !s.A.refreshDevId && W.v.info("[devId register]", {
                            localEqual: u,
                            fromNode: s.A.refreshDevId,
                            customConfig: F.Xz
                        })
                    }
                    )).catch((function() {}
                    ));
                case 9:
                case "end":
                    return e.stop()
                }
        }
        ), e)
    }
    )));
    return function() {
        return e.apply(this, arguments)
    }
}()
J = function() {
    var e = (0,
    i.A)((0,
    o.A)().mark((function e(t) {
        var n, r, i, a, s, u, d, f, g;
        return (0,
        o.A)().wrap((function(e) {
            for (; ; )
                switch (e.prev = e.next) {
                case 0:
                    return n = c.A.init({
                        project: "nav"
                    }),
                    r = w.A.get("tmx_session_id") || "",
                    i = w.A.get("fingerprint_id") || "",
                    a = w.A.get("fp_s"),
                    s = n.get("tmx_id") || "",
                    u = c.A.g.get("lastDevId"),
                    e.next = 8,
                    l().getDevId();
                case 8:
                    return d = e.sent,
                    f = u !== d,
                    g = function(e, t) {
                        var r = K();
                        n.set("tmx_id", r),
                        n.set("reTmxSession", {
                            inHouseDone: !1,
                            tmxDone: !1
                        }),
                        $(r).then((function() {
                            e(r)
                        }
                        )).catch((function() {
                            t()
                        }
                        )),
                        H(r).then((function() {}
                        )).catch((function() {}
                        ))
                    }
                    ,
                    e.abrupt("return", new Promise((function(e, o) {
                        f ? (s && n.remove("tmx_id"),
                        g(e, o)) : r && Y(r) ? t && Z(r) ? g(e, o) : (i && 0 === Number(a) || H(r).then((function() {}
                        )).catch((function() {}
                        )),
                        e(r)) : t && Z(s) || !s || !i || 0 !== Number(a) ? (s && n.remove("tmx_id"),
                        g(e, o)) : s && $(s).then((function() {
                            e(s)
                        }
                        )).catch((function() {
                            o()
                        }
                        ))
                    }
                    )));
                case 12:
                case "end":
                    return e.stop()
                }
        }
        ), e)
    }
    )));
    return function(t) {
        return e.apply(this, arguments)
    }
}()
K = function() {
    var e = c.A.init({
        project: "nav"
    })
      , t = e.get("tmx_id");
    return t || (t = "".concat(N.o.mathRandom().toString(36).substring(2), "_").concat(Date.now()),
    e.set("tmx_id", t)),
    t
}
