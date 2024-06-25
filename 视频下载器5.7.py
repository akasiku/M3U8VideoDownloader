import os
import re
import time
import Crypto.Cipher.AES
import requests
from concurrent.futures import ThreadPoolExecutor
import shutil
import warnings

warnings.filterwarnings("ignore")

def setheader():
    def setheader1():
        he = input("")
        if he == "":
            pass
        else:
            k = he.split(": ")
            header[k[0]] = k[1].strip()
            setheader1()
    s=0
    while True:
        if s==2:
            break
        x = input("")
        if x.strip().endswith(":"):
            headerkey=x.strip()[:-1]
        if x.strip().endswith(":")==False and ": " in x:
            setheader1()
            break
        if x=="\n" or x=="":
            s+=1
        else:
            if x.startswith("\"") and x.endswith("\""):
                header[headerkey] = x[1:-1]
            else:
                header[headerkey]=x
            s=0

def decryptor(key,video):
    de=Crypto.Cipher.AES.new(key,IV=b"0000000000000000",mode=Crypto.Cipher.AES.MODE_CBC)
    return de.decrypt(video)

def composite():
        print("\n#################################视频下载完成,正在合成切片###############################")
        videos = os.listdir(f"{video_name}切片文件夹")
        if len(videos)==0:
            print("视频合成失败,文件夹没有视频切片")
            exit()
        with open(fr"{video_name}.mp4", "wb") as F:
            for a in videos:
                data = open(fr"{video_name}切片文件夹/{a}", "rb")
                F.write(data.read())
        print("\n _______________________________恭喜你!视频合成成功!!!!!!!!!_______________________________")


def get_UrlList(url_list,header,verify_flag):
    global key
    key="0"
    li = []
    f = requests.get(url_list,headers=header,verify=verify_flag).text
    x = re.finditer(",(?P<url>.*?)#", f, re.S)
    for i in x:
        sub_url=i.group("url").strip()
        if "http" not in str(sub_url):
            newsubrul=url_list[:url_list.rfind("/")+1]+sub_url.split("/")[-1]
            li.append(newsubrul)
        else:
            li.append(sub_url)
    if "key" in li[0]:
        xx=li[0].split('"')[-2]
        if xx.startswith("http"):
            key=requests.get(xx,headers=header,verify=verify_flag).content
        else:
            key = requests.get( url_list[:url_list.rfind("/") + 1]+xx, headers=header, verify=verify_flag).content

        li=li[1:]
    return li

def signal(percent):
    x = "-" * 100
    percent = int(percent * 100)
    x = ">" * percent + x[percent:]
    print("下载进度"+x)

def dwonload_slice(slice_url, slicenum, leasttime,counturls,verify_flag):
    slicenum = f"{slicenum}".zfill(4)
    if leasttime == 0:
        with open(f"{video_name}切片文件夹/第{slicenum}个切片.mp4", "w") as f:
            f.write("")
            print(f"第{slicenum}个切片下载失败,保存为空切片#################################################")
            exit()
    try:
        res = requests.get(url=slice_url, headers=header, timeout=10,verify=verify_flag).content
        with open(f"{video_name}切片文件夹/第{slicenum}个切片.mp4", "wb") as f:
            if len(key)>3:
                f.write(decryptor(key,res))
            else:
                f.write(res)
        tt = int(slicenum)
        if tt % 10 == 0:
            signal(tt / counturls)
    except:
        print(f"第{slicenum}个切片下载失败,正在尝试再次下载...")
        leasttime = leasttime - 1
        time.sleep(2)
        dwonload_slice(slice_url, slicenum, leasttime,counturls,verify_flag)

def loop(thread_num):
    #获取m3U8视频切片的片段url
    V_flag=True
    try:
        requests.get(url_list,header)
    except Exception as e:
        if requests.exceptions.SSLError == type(e):
            V_flag=False
    try:
        urls = get_UrlList(url_list,header,V_flag)
    except Exception as e:
        print("\n!!!!!!!!!!!!!!输入的链接有误!无法获取M3U8视频切片文件!!!!!!!!!!!!!!!")
        print("错误原因:",e)
        print("将在3秒钟后自动关闭程序!")
        start=time.time()
        while True:
            time.sleep(1)
            now=time.time()
            if now-start>3:
                break
        exit()

    print("\n\n\n#####################################################################################################")
    os.mkdir(fr"{video_name}切片文件夹")
    print(fr"----------------------------------------{video_name}切片文件夹创建成功--------------------------------")
    print("是否是verifY连接?:", V_flag)
    print(f"M3U8请求地址:{url_list}")
    print(f"启用的线程数:{thread_num}")
    print("\n请求头:")
    print(header)
    if len(key)>3:
        print("这是一个加密视频:",key)
    counturls=len(urls)
    print(f"\n**********************获取切片数据完成,一共有{counturls}个切片*********************************")
    print("\n显示前10个切片url:")
    for i in range(10):
        print(urls[i])

    print("\n#####################################Downloading...##############################################\n\n")
    slice_num=1
    if counturls > 1000:
        thread_num=50
    with ThreadPoolExecutor(thread_num) as T:
        for i in urls:
            T.submit(dwonload_slice,slice_url=i,slicenum=slice_num,leasttime=5,counturls=counturls,verify_flag=V_flag)
            slice_num+=1
    composite()
    shutil.rmtree(fr"{video_name}切片文件夹")
    print(f"-----------------------------成功删除{video_name}切片文件夹--------------------------------------\n\n\n\n")
    input("是否继续?")

while True:
    try:
        print("########################################################################################")
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
        url_list = input("请输入M3U8视频切片链接:")
        while(not url_list.startswith("http")):
            url_list = input("输入有误,再次输入M3U8视频切片链接:")
        video_name = input("请输入要保存视频的名字:")
        if len(video_name) == 0:
            video_name = str(time.strftime("%Y年%m月%d日%H时%M分%S秒下载的视频",time.localtime()))
        ifhe = input("是否需要添加header?(如没有直接enter):")
        if len(ifhe) > 0:
            setheader()
        thread_num = input("请输入下载的线程数:")
        if len(thread_num) == 0:
            thread_num = 20
        else:
            thread_num = int(thread_num)
        loop(thread_num)
    except Exception as e:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("下载失败!出现下列错误:")
        print(e)
        lis=os.listdir()
        for i in lis:
            if video_name in i:
                shutil.rmtree(fr"{video_name}切片文件夹")
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

