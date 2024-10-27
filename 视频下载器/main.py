import os
import shutil
import time
import warnings
from analyze_url import analyze
from bilibili import download_bilibili
from composite import composite
from download import download_threadpool
from input_controller import input_url
from setheader import set_header
from youtube import download_youtube

warnings.filterwarnings("ignore")
V_flag = True
encry_key="0"
base_header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
video_name = str(time.strftime("%Y年%m月%d日%H时%M分%S秒下载的视频",time.localtime()))

while True:
    try:
        print("########################################################################################")
        url = input_url()
        if "https://www.bilibili.com/" in url:
            name=input("为视频命名:")
            print("bilibili视频下载，正在下载，请不要关闭窗口")
            if len(name)==0:
                name=video_name
            download_bilibili(url,name)
            continue
        if "https://www.youtube.com" in url:
            download_youtube(url)
            continue
        setheade=input("是否设置请求头?（enter直接忽视）")
        if setheade!="":
            set_header(base_header)
        url_list,encry_key=analyze(url,base_header,V_flag,encry_key)
        total_urls=len(url_list)
        if total_urls==0:
            print("获取切片失败")
            continue
        print(f"######################获取切片成功，一共{total_urls}个切片 ######################")
        temp_name = input("请输入要保存视频的名字:")
        if len(temp_name) != 0:
            video_name=temp_name
        thread_num = input("请输入下载的线程数:")
        if len(thread_num) == 0:
            thread_num = 20
        else:
            thread_num = int(thread_num)
        os.mkdir(fr"{video_name}切片文件夹")
        print(fr"----------------------------------------{video_name}切片文件夹创建成功--------------------------------")
        print("是否是verifY连接?:", V_flag)
        print(f"启用的线程数:{thread_num}")
        print("\n请求头:")
        print(base_header)
        if len(encry_key) > 3:
            print("这是一个加密视频,密钥:", encry_key)
        print("\n显示前10个切片url:")
        for i in range(10):
            print(url_list[i])
        print("\n#####################################Downloading...##############################################\n\n")
        download_threadpool(url_list,thread_num,total_urls,V_flag,video_name,base_header,encry_key)
        composite(video_name)
        shutil.rmtree(fr"{video_name}切片文件夹")
        print(f"-----------------------------成功删除{video_name}切片文件夹--------------------------------------\n\n\n\n")
        input("是否继续?")
    except Exception as e:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("下载失败!出现下列错误:")
        print(e)
        lis = os.listdir()
        for i in lis:
            if video_name in i:
                shutil.rmtree(fr"{video_name}切片文件夹")
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
