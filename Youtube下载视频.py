import os
import re
import subprocess

def main():
    url=input("输入YOUTUBE视频的url:")

    def print_video_message(text):
        temp=re.compile("    - itag:          (.*?)\n      container:     (.*?)\n      quality:       (.*?)\n      size:          (.*?)M(.*?)\n",re.S)
        alldata=temp.findall(text)
        print("#####################解析成功,请选择视频质量##########################")
        for i in alldata:
            print(f"Itag番号:{i[0]}\t  视频格式:{i[1]}  \t清晰度{i[2]}\t  \t视频大小:{i[3]}M")
        print(f"Itag番号:18\t  视频格式:mp4 \t清晰度:medium")


    def select_quality(url):
        command = f'you-get -i "{url}"'
        try:
            # 执行命令并捕获输出
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True, shell=True, encoding="utf-8")
            print_video_message(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败：{e}")

    def download_video(itag):
        os.system(f"you-get --itag={itag} {url}")
    select_quality(url)
    itag=input("输入下载视频的Itag番号:")
    download_video(itag)
while True:
    try:
        print("------------------------------下载YOUTUBE视频----------------------------------")
        main()
    except Exception as e:
        print("似乎出错,错误原因:")
        print(e)
    # https: // www.youtube.com / watch?v = GCgvpwLNvtY & ab_channel = LiangRainnerdxddxc