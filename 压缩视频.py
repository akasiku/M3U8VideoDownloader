import re
import os
import time


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
    print("快速压缩，使用了NVIDIA硬件加速，因此要提前安装英伟达驱动")
    flag="2"
    while True:
        flag=input("\n 1:极限压缩(最快) 2:硬件加速压缩  3:cpu高质压缩(最慢) ")
        if (flag=="1" or flag=="2" or flag=="3"):
            break
    x=input("\n请输入文件名/番号:")
    target=filter(x,lis)
    print("##############################################################################")
    print(f"准备压缩:{target}")
    if(flag=="1"):
        newname = target[:target.rfind(".")] + f"压缩" + target[target.rfind("."):]
        os.system(f"ffmpeg -hwaccel cuda -i {target} -c:v hevc_nvenc -crf 25 -c:a copy -vtag hvc1 {newname}")
    elif(flag=="3"):
        quirty=int(input("输入压缩程度（0~51）值越大压缩程度越高："))
        newname = target[:target.rfind(".")] + f"压缩{quirty}" + target[target.rfind("."):]
        os.system(f"ffmpeg -i {target} -vcodec libx264 -crf {quirty} -preset medium -acodec aac -b:a 128k {newname}")
    else:
        quirty = int(input("输入压缩程度（0~51）值越大压缩程度越高："))
        newname = target[:target.rfind(".")] + f"压缩{quirty}" + target[target.rfind("."):]
        os.system(f"ffmpeg -i {target} -c:v h264_nvenc -preset slow -cq {quirty} -c:a aac -b:a 128k {newname}")
    print("\n\n————————————————————————————————压缩成功————————————————————————————————")
while True:
    try:
        test()
    except Exception as e:
        print(e)