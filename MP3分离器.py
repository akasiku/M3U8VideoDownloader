import os
l=os.listdir()
for i in l:
    if i.endswith("mp4") or i.endswith("MP4"):
        k=i.replace("4","3").replace(" ","")
        os.system(f'ffmpeg -i "{i}" -vn {k}')
        print("***************************************************")
        print(i,"----->",k,"成功")
        print("***************************************************")
print("\n\n\n\n---------------------------全部分离成功--------------------------------------\n\n\n")
k=input()

