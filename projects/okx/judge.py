import asyncio
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..','..'))
sys.path.append(project_root)
import json
import random
import time
from hashlib import md5

import httpx
from loguru import logger

from projects.okx.cryptio import Cbc, Rsa

k = [
    "textLength",
    "HTMLLength",
    "documentMode",
    "A",
    "ARTICLE",
    "ASIDE",
    "AUDIO",
    "BASE",
    "BUTTON",
    "CANVAS",
    "CODE",
    "IFRAME",
    "IMG",
    "INPUT",
    "LABEL",
    "LINK",
    "NAV",
    "OBJECT",
    "OL",
    "PICTURE",
    "PRE",
    "SECTION",
    "SELECT",
    "SOURCE",
    "SPAN",
    "STYLE",
    "TABLE",
    "TEXTAREA",
    "VIDEO",
    "screenLeft",
    "screenTop",
    "screenAvailLeft",
    "screenAvailTop",
    "innerWidth",
    "innerHeight",
    "outerWidth",
    "outerHeight",
    "browserLanguage",
    "browserLanguages",
    "systemLanguage",
    "devicePixelRatio",
    "colorDepth",
    "userAgent",
    "cookieEnabled",
    "netEnabled",
    "screenWidth",
    "screenHeight",
    "screenAvailWidth",
    "screenAvailHeight",
    "localStorageEnabled",
    "sessionStorageEnabled",
    "indexedDBEnabled",
    "CPUClass",
    "platform",
    "doNotTrack",
    "timezone",
    "canvas2DFP",
    "canvas3DFP",
    "plugins",
    "maxTouchPoints",
    "flashEnabled",
    "javaEnabled",
    "hardwareConcurrency",
    "jsFonts",
    "timestamp",
    "performanceTiming",
    "internalip",
    "mediaDevices",
    "DIV",
    "P",
    "UL",
    "LI",
    "SCRIPT",
    "deviceorientation",
    "touchEvent"
]


async def genKey(num) -> str:
    t = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    n = ''
    for i in range(num):
        n += random.choice(t)
    return n


async def judge():
    headers = {
        "authority": "dkapi-ga.geetest.com",
        "accept": "application/json",
        "accept-language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
        "cache-control": "no-cache",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://www.okx.com",
        "pragma": "no-cache",
        "connection": "clone",
        "referer": "https://www.okx.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    params = {
        'pt': '1',
        'app_id': 'f8553adb1e94368c52b9617f669a0227',
    }

    canvase = md5(str(random.randint(1000000000, 9999999999)).encode()).hexdigest()
    n = {
        "LINK": 48,
        "STYLE": 4,
        "SCRIPT": 49,
        "DIV": 311,
        "A": 169,
        "IMG": 2,
        "UL": 4,
        "LI": 61,
        "SPAN": 20,
        "P": 5,
        "INPUT": 2,
        "BUTTON": 1,
        "IFRAME": 1,
        "TEXTAREA": 1,
        "textLength": 42854 + random.randint(1, 10),
        "HTMLLength": 99587 + random.randint(1, 10),
        "documentMode": "CSS1Compat",
        "browserLanguage": "zh-CN",
        "browserLanguages": "zh-CN,en-GB,en-US,en",
        "devicePixelRatio": random.choice([1.25, 1]),
        "colorDepth": 24,
        "userAgent": headers["user-agent"],
        "cookieEnabled": 1,
        "netEnabled": 1,
        "innerWidth": 150 + random.randint(1, 10),
        "innerHeight": 670 + random.randint(1, 10),
        "outerWidth": 1536 + random.randint(1, 10),
        "outerHeight": 816 + random.randint(1, 10),
        "screenWidth": 1536 + random.randint(1, 10),
        "screenHeight": 864 + random.randint(1, 10),
        "screenAvailWidth": 1536 + random.randint(1, 10),
        "screenAvailHeight": 816 + random.randint(1, 10),
        "screenLeft": 0,
        "screenTop": 0,
        "screenAvailLeft": 0,
        "screenAvailTop": 0,
        "localStorageEnabled": 1,
        "sessionStorageEnabled": 1,
        "indexedDBEnabled": 1,
        "platform": "Win32",
        "doNotTrack": 0,
        "timezone": -8,
        "canvas2DFP": canvase,
        "canvas3DFP": 0,
        "plugins": "internal-pdf-viewer,mhjfbmdgcfjbbpaeojofohoefgiehjai,internal-nacl-plugin",
        "maxTouchPoints": 0,
        "flashEnabled": -1,
        "javaEnabled": 0,
        "hardwareConcurrency": random.choice([12, 8, 16, 32]),
        "jsFonts": "Arial,ArialBlack,ArialNarrow,BookAntiqua,BookmanOldStyle,Calibri,Cambria,CambriaMath,Century,CenturyGothic,CenturySchoolbook,ComicSansMS,Consolas,Courier,CourierNew,Garamond,Georgia,Helvetica,Impact,LucidaBright,LucidaCalligraphy,LucidaConsole,LucidaFax,LucidaHandwriting,LucidaSans,LucidaSansTypewriter,LucidaSansUnicode,MicrosoftSansSerif,MonotypeCorsiva,MSGothic,MSPGothic,MSReferenceSansSerif,MSSansSerif,MSSerif,PalatinoLinotype,SegoePrint,SegoeScript,SegoeUI,SegoeUILight,SegoeUISemibold,SegoeUISymbol,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings,Wingdings2,Wingdings3",
        "mediaDevices": -1,
        "timestamp": int(time.time() * 1000),
        "deviceorientation": -1,
        "touchEvent": -1,
        "performanceTiming": -1,
        "internalip": -1
    }
    insights_ = []
    for i in k:
        insights_.append(n[i] if n.get(i) is not None else -1)
    insights = "!!".join([str(i) for i in insights_])

    data = {
        "id": "f8553adb1e94368c52b9617f669a0227",
        "page_id": int(time.time() * 1000),
        "lang": "zh-cn",
        "data": {
            "insights": insights,
            "track_key": 1,
            "track": [],
            "ep": {
                "v": "2.5.0",
                "f": "406ec650",
                "em": {
                    "ph": 0,
                    "cp": 0,
                    "ek": "11",
                    "wd": 1,
                    "nt": 0,
                    "si": 0,
                    "sc": 0
                },
                "te": False,
                "me": False,
                "do": False,
                "ot": -1,
                "tm": {
                    "a": int(time.time() * 1000),
                    "b": int(time.time() * 1000),
                    "c": int(time.time() * 1000),
                    "d": 0,
                    "e": 0,
                    "f": int(time.time() * 1000),
                    "g": int(time.time() * 1000),
                    "h": int(time.time() * 1000),
                    "i": int(time.time() * 1000),
                    "j": int(time.time() * 1000),
                    "k": 0,
                    "l": int(time.time() * 1000),
                    "m": int(time.time() * 1000),
                    "n": int(time.time() * 1000),
                    "o": int(time.time() * 1000),
                    "p": int(time.time() * 1000),
                    "q": int(time.time() * 1000),
                    "r": int(time.time() * 1000),
                    "s": int(time.time() * 1000),
                    "t": int(time.time() * 1000),
                    "u": int(time.time() * 1000)
                },
                "action": "client",
                "iip": "",
                "ts": int(time.time() * 1000),
            },
            "ww3": ""
        }
    }
    eco = md5((await genKey(32) + str(int(time.time() * 1000))).encode()).hexdigest()
    data["data"]["eco"] = eco
    key = await genKey(16)
    cbc = Cbc(key, '0000000000000000')
    _1 = await cbc.encrypt(json.dumps(data, separators=(',', ':')), result="b64")
    rsa = Rsa()
    _2 = await rsa.Rencrypt(key)
    endata = str(_1) + str(_2)
    proxy = "http://127.0.0.1:7890"
    try:
        async with httpx.AsyncClient(
                verify=False,
                # http2=True,
                timeout=60,
                headers=headers,
                # proxies=proxy
        ) as session:
            resp = await session.post(
                url="https://dkapi-ga.geetest.com/deepknow/v2/judge",
                params=params,
                data=endata
            )
        return resp.json()
    except Exception as e:
        msg = str(e) if str(e) else type(e).__name__
        logger.error(f"judge接口错误: {msg}")
        return None


if __name__ == '__main__':
    print(asyncio.run(judge()))
