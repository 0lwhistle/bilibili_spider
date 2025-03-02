import os
import re
import requests
import json
import subprocess
import ctypes
from ctypes import windll, wintypes
def video_spider(url, retain=False, root_path=None):
    global title

    url = url.replace("\"", "")
    if not root_path == None:
        if not os.path.exists(os.path.join(root_path, "Video")):
            os.mkdir(os.path.join(root_path, "Video"))
    else:
        def get_desktop_path():
            CSIDL_DESKTOP = 0
            SHGFP_TYPE_CURRENT = 0
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, SHGFP_TYPE_CURRENT, buf)
            return buf.value

        root_path = get_desktop_path()
        if not os.path.exists(os.path.join(root_path, "Video")):
            os.mkdir(os.path.join(root_path, "Video"))

    video_output_path = os.path.join(root_path, "Video")

    video_output_path = os.path.normpath(video_output_path)

    if not os.path.exists(video_output_path):
        os.mkdir(video_output_path)

    save_path = {"video_save_path": video_output_path, "audio_save_path": video_output_path}
    path_name = ["video_save_path", "audio_save_path"]

    for i in path_name:
        if not os.path.exists(save_path[i]):
            os.mkdir(save_path[i])

    try:

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",

            "cookie":"buvid3 = 54DE8D4B - 7E01 - 208E-72A7 - 293842FA24A628812infoc;b_nut = 1718171728;_uuid = 5F7DB4FD - A6910 - E2BF - 9BB6 - DF17E5ECFE6E29544infoc;enable_web_push = DISABLE;buvid4 = B8AE0146 - 440D - 9F23 - 9FD0 - 1B42B06DA2BB29482 - 024061205 - BzEY7UxVRo3wIkiPYXuQVH2pqFdPU9atYxJR7lxcBoI % 3D;header_theme_version = CLOSE;rpdid = 0zbfvWJqJk | 1cW1Wx584 | o | 3w1ShpKH;buvid_fp_plain = undefined;DedeUserID = 33019519;DedeUserID__ckMd5 = 23f2b683d371db99;CURRENT_BLACKGAP = 0;CURRENT_FNVAL = 4048;LIVE_BUVID = AUTO9017240572238477;PVID = 1;CURRENT_QUALITY = 80;fingerprint = 22459092ef139bc76334a66bc73d3dbe;buvid_fp = 22459092ef139bc76334a66bc73d3dbe;home_feed_column = 5;browser_resolution = 1536 - 730;bili_ticket = eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzMyMTkyODYsImlhdCI6MTczMjk2MDAyNiwicGx0IjotMX0.8xaPVzZymWDISIjIHB7_JgQrxv2t9h5pawz__v7Aonw;bili_ticket_expires = 1733219226;SESSDATA = 65d39618 % 2C1748512086 % 2C1a0de % 2Ab1CjDwqHVq7aOlMRLKvwlD9GRBH0wXi80vZpRjiuNBmXbU689_0lh2ikbJAIn_FF89kTsSVmhDYjE3dTNTNkVoUWVLOHBXRF9LNW52R2VaLWJ6dFVFZG52YmhBNGlzZGNHWlo1VG8wSHVZblJZWG9sQ0dMMlpzMjhtT3FXbUx1SWV4eXVEWTZWeVB3IIEC;bili_jct = 95feed91a67ef9acbe283cc9564fc31f;b_lsid = F71AA5AC_19381F71D45;sid = 4tm9g6df;bp_t_offset_33019519 = 1005941792387891200",
            "referer": "https://www.bilibili.com/video/BV141znY3EN5/?spm_id_from=333.1007.tianma.1-3-3.click&vd_source=ad050f79f8eb70b2667311307c5f54fc",
            }


        html = requests.get(url = url, headers = headers).text

        #print(html)

        title = ""

        title = re.findall("<h1 data-title=\"(.*?)\" title=.*?", html)[0]

        video_info = re.findall("<script>window.__playinfo__=(.*?)</script>", html)[0]
        # print(1)
        # print(video_info)

        json_data = json.loads(video_info)

        audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]

        video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
        # print(video_url)

        response_audio = requests.get(url=audio_url, headers=headers).content
        response_video = requests.get(url=video_url, headers=headers).content

        audio_path = save_path["audio_save_path"] + title + ".mp3"
        video_path = save_path["video_save_path"] + title + ".mp4"

        with open(audio_path, "wb") as fo:
            fo.write(response_audio)

        with open(video_path, "wb") as fo:
            fo.write(response_video)

        out_path = os.path.join(video_output_path, title + ".mp4")
        #ffmpeg -i ".mp4" -i ".mp3" -c:v copy -c:a aac -strict experimental -b:a 192k -af "volume=0.5" "outputvideo.mp4"

        # cmd = "D:\\ffmpeg\\bin\\ffmpeg -i \"{}\" -i \"{}\" -c:v copy -c:a aac -bsf:a aac_adtstoasc -af \"volume=0.2\" \"{}\"".format(
        #     video_path, audio_path, out_path)
        # cmd = ".\\ffmpeg -i \"{}\" -i \"{}\" -c:v copy -c:a aac -strict experimental -b:a 192k -af \"volume=0.6\" \"{}\"".format(
        #     video_path, audio_path, out_path)

        cmd = "D:\\ffmpeg\\bin\\ffmpeg -i \"{}\" -i \"{}\" -c:v copy -c:a aac -strict experimental -b:a 192k -af \"volume=0.6\" \"{}\"".format(
            video_path, audio_path, out_path)

        try:
            subprocess.run(cmd)

        except:
            print("merge error")
            print(video_path)
            print(audio_path)
            print(out_path)
            # os.remove(audio_path)
            # os.remove(video_path)
            print("视频 《{}》 爬取失败!".format(title))
            return


        if not retain:
            os.remove(save_path["audio_save_path"] + title + ".mp3")
            os.remove(save_path["video_save_path"] + title + ".mp4")

        print("视频 《{}》 爬取成功！！！".format(title))

    except:
        global t
        t = 1
        if not title == "":
            print("视频 《{}》 爬取失败!".format(title))
        else:
            print("所提供的url有错误，导致 {} 个视频爬取失败。".format(t))
            t += 1
        pass

if __name__ == '__main__':
    url = "https://www.bilibili.com/video/BV1uywdeMEMY/?spm_id_from=333.1387.favlist.content.click&vd_source=ad050f79f8eb70b2667311307c5f54fc"
    video_spider(url, retain=False)
