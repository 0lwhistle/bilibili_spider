import os
import re
import requests
import json
import subprocess
def audio_spider(url, root_path):
    global title
    save_path = {"audio_save_path": root_path}
    path_name = ["audio_save_path"]


    for i in path_name:
        if not os.path.exists(save_path[i]):
            os.mkdir(save_path[i])

    try:

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",

            "cookies":"buvid3=909E5729-EFAB-2F32-B3A1-34EB838A8A9602947infoc; b_nut=1710727402; i-wanna-go-back=-1; b_ut=7; _uuid=6489BD93-A865-5B94-D9A9-63F27378DA3602229infoc; buvid4=7139C569-132D-9577-D68D-007AB173BD6803357-024031802-BzEY7UxVRo3wIkiPYXuQVKYh7UKtfs%2F%2BhXtzsY6CXhs%3D; buvid_fp=3631420f387de85622c8fd0affddcd2c; enable_web_push=DISABLE; FEED_LIVE_VERSION=V8; CURRENT_FNVAL=4048; rpdid=0zbfAGOYl1|960q0JkK|GNj|3w1SaIt4; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgxNjU5MzksImlhdCI6MTcxNzkwNjY3OSwicGx0IjotMX0.b7wdvjfV5Bc1P3xQ3fyOAfCOTo_LeA9fNeY3JJOI4rk; bili_ticket_expires=1718165879; SESSDATA=2742f725%2C1733462055%2C1149e%2A61CjA5MD5J-jnl1st6QO6Nv9OjsD3QRB_WCRgka-2ImQ7vBp996yvwcVDg4P9Gf2LwGNISVjJ1ZlBQTmZzT0d0aXF4Yk1sNkRERnJpaEszUTFGeG5valFUZ21NeHBiYjJqUzZ6M0xqVU42QlBMaWdIZ05EdTVEX2FYZVEtSFE2TDBEQjV6S2p3eDVnIIEC; bili_jct=48a13a6cc4212023e417593063946aae; DedeUserID=33019519; DedeUserID__ckMd5=23f2b683d371db99; header_theme_version=CLOSE; CURRENT_QUALITY=64; b_lsid=8546B25E_19005CA5304; bsource=search_baidu; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; home_feed_column=4; browser_resolution=762-714; sid=7qs21k59",

            "referer": "https://www.bilibili.com/video/BV1YM4m1U7vo/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=ad050f79f8eb70b2667311307c5f54fc",
            }


        html = requests.get(url = url, headers = headers).text


        title = re.findall("<h1 data-title=\"(.*?)\" title=.*?", html)[0]

        audio_info = re.findall("<script>window.__playinfo__=(.*?)</script>", html)[0]

        json_data = json.loads(audio_info)

        audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]

        response_audio = requests.get(url=audio_url, headers=headers).content

        audio_path = os.path.join(save_path["audio_save_path"], title + ".mp3")

        with open(audio_path, "wb") as fo:
            fo.write(response_audio)

        print("音频 《{}》 爬取成功！！！".format(title))

    except:
        global t
        t = 1

        if not title == "":
            print("音频 《{}》 爬取失败!".format(title))
        else :
            print("所提供的url有错误，导致 {} 个音频爬取失败。".format(t))
            t+=1
        pass

if __name__ == '__main__':

