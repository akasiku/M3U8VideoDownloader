import os
while True:
    url=input("输入Youtube视频地址:")
    os.system(f"you-get --itag=18 {url}")
    print("视频下载完成")