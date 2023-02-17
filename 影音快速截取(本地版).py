import re
import os
import time
import cv2
import eyed3


def settime(x):
    if x<60:
        return f"{x}"
    elif 60<=x<3600:
        m=str(x//60).zfill(2)
        s=str(x%60).zfill(2)
        return f"{m}{s}"
    else:
        h=str(x//3600).zfill(2)
        m=str(x%3600//60).zfill(2)
        s=str(x%3600%60%60).zfill(2)
        return f"{h}{m}{s}"
def totime(x):
    s = re.compile("\d{1,2}:\d{1,2}:\d{1,2}", re.S)
    res=s.match(x)
    if res != None:
        return s.match(x).group()
    elif x.isnumeric():
        x=x.zfill(6)
        x=x[:2]+":"+x[2:4]+":"+x[4:6]
        return x
    else:
        s=input("你输入的有错误,请再次输入:")
        return totime(s)
def filter(target, li):
    swa=[]
    if target.isnumeric():
        target=int(target)
        if target>len(li):
            target=len(li)-1
        return li[target]
    else:
        for x in li:
            if re.search(f"(?i){target}",x)!=None:
                swa.append(x)
        if len(swa)==0:
            input("没有找到,任意点击返回")
            return filter("",li)
        elif len(swa)==1:
            return swa[0]
        else:
            x = 0
            print("\n\nvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n")
            for i in swa:
                print(f"{i}------------------{x}")
                x+=1
            print("\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            n=input("找到以上文件,请选择:")
            return filter(n,swa)

def test():
    li=os.listdir()
    lis=[]
    end=["mp4","mp3","avi","mov","flv","MP4","MP3","AVI","MOV","FLV"]
    index=0
    for i in range(len(li)):
        if(li[i].split(".")[-1] in end):
            lis.append(li[i])
            print(f"{li[i]}---------------->{index}\t")
            index+=1
    if len(lis)==0:
        print("没有扫描可用文件,请把文件放置到有音/视频文件的文件夹内!")
        print("目前支持剪切MP4,MP3,AVI,MOV,FLV文件")
        input("点击Enter键退出")
        exit()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    x=input("\n\n请输入文件名/番号:")
    target=filter(x,lis)
    if target.endswith("mp4") or target.endswith("MP4"):
        video=cv2.VideoCapture(f"{target}")
        length=int(video.get(7)/video.get(5))
        video.release()
    if target.endswith("mp3") or target.endswith("MP3"):
        xx = eyed3.load(target)
        length=int(xx.info.time_secs/2)-2
    length=settime(length)
    print(f"准备剪切文件:{target}")
    print(length)
    start=input("输入开始时间:")
    if len(start)==0:
        start="00:00:00"
    start=totime(start)
    end=input("输入结束时间:")
    if len(end)==0:
        end=length
    end=totime(end)
    origin=target.split(".")[-2]+"(原版)."+target.split(".")[-1]
    try:
        os.system(f'copy "{target}" "{origin}')
        os.system(f'del "{target}"')
        time.sleep(1)
        os.system(f'ffmpeg -i "{origin}" -ss {start} -to {end} -codec copy "{target}"')
        print(f'执行命令 ffmpeg -i "{origin}" -ss {start} -to {end} -codec copy "{target}"\n\n')
    except Exception as e:
        print("截取失败,出现以下原因:")
        print(e)
while True:
    test()