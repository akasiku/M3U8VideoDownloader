import os
p=r"C:\Users\13498\Desktop\油管"
l=os.listdir(p)
for i in l:
    if i.endswith("mp4") or i.endswith("MP4"):
        k=i.replace("4","3").replace(" ","")
        os.system(f'ffmpeg -i "{i}" -vn {k}')
        print(i,"----->",k,"成功")
print("----------------------------------------------------------------------")
k=input()

