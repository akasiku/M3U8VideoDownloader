import os
import re


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
    x=input("请输入的文件名/番号:")
    target1=filter(x,lis)
    x2 = input("请输入要结合的文件名/番号:")
    target2=filter(x2,lis)
    try:
        print("-----------------------------------------------------------------------")
        os.system(f'ffmpeg -i "{target1}" -vcodec copy -acodec copy -vbsf h264_mp4toannexb "{target1.split(".")[:-1]}.ts"')
        os.system(f'ffmpeg -i "{target2}" -vcodec copy -acodec copy -vbsf h264_mp4toannexb "{target2.split(".")[:-1]}.ts"')
        print(target1.split(".")[:-1])
        print(target2.split(".")[:-1])
        print(f'ffmpeg -i "concat:{target1.split(".")[:-1]}.ts|{target2.split(".")[:-1]}.ts" -acodec copy -vcodec copy -absf aac_adtstoasc "{target1.split(".")[:-1]}(合成).mp4"')
        print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
        os.system(f'ffmpeg -i "concat:{target1.split(".")[:-1]}.ts|{target2.split(".")[:-1]}.ts" -acodec copy -vcodec copy -absf aac_adtstoasc "{target1.split(".")[:-1]}(合成).mp4"')

        os.system(f'del [{target1.split(".")[:-1]}].ts [{target2.split(".")[:-1]}].ts')
        print("-----------------------------------------------------------------------")
    except Exception as e:
        print("截取失败,出现以下原因:")
        print(e)
while True:
    test()