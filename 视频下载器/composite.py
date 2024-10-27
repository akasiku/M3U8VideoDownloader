import os

def composite(video_name):
    print("\n#################################视频下载完成,正在合成切片###############################")
    videos = os.listdir(f"{video_name}切片文件夹")
    if len(videos) == 0:
        print("视频合成失败,文件夹没有视频切片")
        exit()
    with open(fr"{video_name}.mp4", "wb") as F:
        for a in videos:
            data = open(fr"{video_name}切片文件夹/{a}", "rb")
            F.write(data.read())
    print("\n _______________________________恭喜你!视频合成成功!!!!!!!!!_______________________________")
