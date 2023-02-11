import os
import re
import time

import requests
from concurrent.futures import ThreadPoolExecutor
import shutil

def setheader():
    he = input("")
    if he == "":
        pass
    else:
        k = he.split(": ")
        header[k[0]] = k[1].strip()
        setheader()

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

def get_UrlList(url_list,header):
    li = []
    f = requests.get(url_list,headers=header).text
    x = re.finditer(",(?P<url>.*?)#", f, re.S)
    for i in x:
        li.append(i.group("url").strip())
    return li

def signal(percent):
    x = "-" * 50
    percent = int(percent * 50)
    x = ">" * percent + x[percent:]
    print("下载进度"+x)

def dwonload_slice(slice_url, slicenum, leasttime,counturls,x):
    slicenum = f"{slicenum}".zfill(4)
    if leasttime == 0:
        with open(f"{video_name}切片文件夹/第{slicenum}个切片.mp4", "w") as f:
            f.write("")
            print(f"第{slicenum}个切片下载失败,保存为空切片#################################################")
            exit()
    try:
        res = requests.get(url=slice_url, headers=header, timeout=10).content
        with open(f"{video_name}切片文件夹/第{slicenum}个切片.mp4", "wb") as f:
            f.write(res)
        tt = int(slicenum)
        if tt % x == 0:
            signal(tt / counturls)
    except:
        print(f"第{slicenum}个切片下载失败,正在尝试再次下载................................................")
        leasttime = leasttime - 1
        dwonload_slice(slice_url, slicenum, leasttime,counturls)

def loop():
    #获取m3U8视频切片的片段url

    try:
        urls = get_UrlList(url_list,header)
    except Exception as e:
        print("\n!!!!!!!!!!!!!!输入的链接有误!无法获取M3U8视频切片文件!!!!!!!!!!!!!!!")
        print("错误原因:",e)
        print("将在十秒钟后自动关闭程序!")
        start=time.time()
        while True:
            time.sleep(1)
            now=time.time()
            if now-start>10:
                break
        exit()

    print("#######################################################################################")
    os.mkdir(fr"{video_name}切片文件夹")
    print(fr"--------------------------------{video_name}切片文件夹创建成功--------------------------")
    print(f"\n请求地址:{url_list}")
    print(f"\n启用的线程数:{thread_num}")
    print("\n请求头:")
    print(header)
    swap_urls = urls.copy()
    if len(prefix) > 0:
        urls.clear()
        for i in swap_urls:
            sub = prefix + i
            urls.append(sub)
    counturls=len(urls)

    print(f"\n**********************获取切片数据完成,一共有{counturls}个切片*********************************")
    sli=10
    if counturls<=200:
        sli=5
    print("\n显示前10个切片url:")
    for i in range(10):
        print(urls[i])

    print("\n#####################################开始下载##############################################\n\n")
    slice_num=1
    with ThreadPoolExecutor(thread_num) as T:
        for i in urls:
            T.submit(dwonload_slice,slice_url=i,slicenum=slice_num,leasttime=3,counturls=counturls,x=sli)
            slice_num+=1

    composite()
    shutil.rmtree(fr"{video_name}切片文件夹")
    print(f"-----------------------------成功删除{video_name}切片文件夹--------------------------------------\n\n\n\n")
    input("是否继续?")

while True:
    try:
        print("########################################################################################")
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        url_list = input("请输入M3U8视频切片链接:")
        video_name = input("请输入要保存视频的名字:")
        if len(video_name) == 0:
            video_name = str(time.time())
        ifhe = input("是否需要添加header?(如没有直接enter):")
        if len(ifhe) > 0:
            setheader()
        thread_num = input("请输入下载的线程数:")
        if len(thread_num) == 0:
            thread_num = 20
        else:
            thread_num = int(thread_num)
        prefix = input("如果有前缀,请输入前缀:")
        loop()
    except Exception as e:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("下载失败!出现下列错误:")
        print(e)
        lis=os.listdir()
        for i in lis:
            if video_name in i:
                shutil.rmtree(fr"{video_name}切片文件夹")
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
