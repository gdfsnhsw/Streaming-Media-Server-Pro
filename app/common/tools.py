#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import re
import time

from app.common.diyEpg import return_diyepg
from app.modules.request import request
from app.settings import gdata, localhost, tvglogo


def generate_m3u(host, hd, name):
    """
    构造 m3u 数据
    :param host:
    :param hd:
    :param name: online | channel | channel2
    :return:
    """
    name += ".m3u8"
    yield '#EXTM3U x-tvg-url="https://github.com/239144498/Streaming-Media-Server-Pro"\n'
    for i in gdata:
        # tvg-ID="" 频道id匹配epg   fsLOGO_MOBILE 台标 | fsHEAD_FRAME 播放预览
        yield '#EXTINF:{} tvg-chno="{}" tvg-id="{}" tvg-name="{}" tvg-logo="{}" group-title="{}",{}\n'.format(
            -1, i['fs4GTV_ID'], i['fs4GTV_ID'], i['fsNAME'], i[tvglogo], i['fsTYPE_NAME'], i['fsNAME'])
        if not host:
            yield localhost + f"/{name}?fid={i['fs4GTV_ID']}&hd={hd}\n"
        else:
            yield localhost + f"/{name}?fid={i['fs4GTV_ID']}&hd={hd}&host={host}\n"
    yield return_diyepg()  # 返回自定义频道


def writefile(filename, content):
    with open(filename, "wb") as f:
        f.write(content)
        f.close()


def get_4gtv(url):
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
    }
    with request.get(url=url, headers=header) as res:
        return res.status_code, res.text


def solvelive(now, t1, t2, gap):
    x = now - t1
    seq = round(t2 + x // gap)
    return seq


def genftlive(data):
    seq = re.findall(r"#EXT-X-MEDIA-SEQUENCE:(\d+)\n", data).pop()
    gap = re.findall(r"#EXT-X-TARGETDURATION:(\d+)\n", data).pop()
    return int(seq), int(gap)


def generate_url(fid, host, hd, begin, seq, url):
    if "4gtv-4gtv" in fid or "-ftv10" in fid or "-longturn17" in fid or "-longturn18" in fid:
        return url.format(host, begin, seq)
    elif "4gtv-live" in fid:
        return url.format(host, fid, f"{hd}{seq}")
    else:
        return url.format(host, seq)


def now_time():
    return int(time.time())
