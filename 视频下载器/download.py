import time
from concurrent.futures import ThreadPoolExecutor

import requests
from decryptor import decryptor
from process_table import signal


def download_threadpool(url_list, thread_num, total_urls, V_flag, video_name, header, key):
    slice_num = 1
    with ThreadPoolExecutor(thread_num) as T:
        for i in url_list:
            T.submit(dwonload_slice, slice_url=i, slicenum=slice_num, left_time=5, total_urls=total_urls,
                     video_name=video_name, header=header, verify_flag=V_flag, key=key)
            slice_num += 1


def dwonload_slice(slice_url, slicenum, left_time, total_urls, video_name, header, verify_flag, key):
    slicenum = f"{slicenum}".zfill(4)
    if left_time == 0:
        with open(f"{video_name}切片文件夹/第{slicenum}个切片.mp4", "w") as f:
            f.write("")
            print(f"第{slicenum}个切片下载失败,保存为空切片#################################################")
            exit()
    try:
        res = requests.get(url=slice_url, headers=header, timeout=10, verify=verify_flag).content
        with open(f"{video_name}切片文件夹/第{slicenum}个切片.mp4", "wb") as f:
            if len(key) > 3:
                f.write(decryptor(key, res))
            else:
                f.write(res)
        tt = int(slicenum)
        if tt % 10 == 0:
            signal(tt / total_urls)
    except:
        print(f"第{slicenum}个切片下载失败,正在尝试再次下载...")
        left_time = left_time - 1
        time.sleep(3)
        dwonload_slice(slice_url, slicenum, left_time, total_urls, verify_flag)
