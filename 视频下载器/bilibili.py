import os
import time

import requests
import re
def download_bilibili(url,name):
    head = {
        'origin': 'https://www.bilibili.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'referer': f'{url}'
    }
    res=requests.get(url,headers=head)
    content=res.text
    vido=re.findall('"mimeType":"video/mp4".*?"baseUrl":"(.*?)"',content)
    audio=re.findall('mimeType":"audio/mp4".*?"baseUrl":"(.*?)"',content)
    audio2 = re.findall(r'"audio":\[{"id".*?"baseUrl":"(.*?)"mimeType":"audio/mp4"', content)
    audio2l = re.findall(r'http.*?"', audio2[0])
    audio_list=[]
    for i in audio:
        audio_list.append(i)
    if len(audio_list)==0:
        for i in audio2l:
            ull = i[:-1]
            if requests.get(ull, head).status_code==200:
                audio_list.append(ull)
                break
    vido_list=[]
    for v in vido:
        vido_list.append(v)
    print(vido_list[0])
    print(audio_list[0])
    if len(vido_list)>0:
        with open(f"{name}.mp4","wb") as f1:
            videourl=vido_list[0]
            f1.write(requests.get(videourl,headers=head).content)
            print("------------------视频下载完成------------------")
            f1.close()
    else:
        print("没有找到视频url!!!!!!!!!!!!!")
        print("十秒后退出")
        time.sleep(10)
        exit()
    if len(audio_list)>0:
        with open(f"{name}.mp3","wb") as f2:
            audiourl=audio_list[0]
            f2.write(requests.get(audiourl,headers=head).content)
            print("-----------------视频声音下载完成-----------------")
            f2.close()
    else:
        print("没有找到声音url!!!!!!!!!!!!!!!!!!!!")
        print("十秒后退出")
        time.sleep(10)
        exit()
    print("下载完成准备把视频和声音合并")
    os.system(f'ffmpeg -i "{name}.mp4" -i "{name}.mp3" -vcodec copy -acodec copy [{name}].mp4')
    time.sleep(2)
    os.system(f"del {name}.mp4 {name}.mp3")
    print("合成成功!!!!!!!!!!!!!!!!!!!")
