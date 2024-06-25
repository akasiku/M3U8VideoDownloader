import os
import re

from PIL import Image

#获取所有文件
def showDir():
    dirlist = os.listdir()
    li=[]
    for i in dirlist:
        if i.endswith(("png","PNG","JPG","jpg","jepg","JEPG","webp","WEBP")):
            li.append(i)
    if len(li)>0:
        for i, j in enumerate(li):
            print(f"{i}  -------->  {j}")
        return li
    else:
        print("没能找到图片文件(jpg,png,jepg)")

def compress_image(input_path, output_path, quality):
    # 打开图像
    img = Image.open(input_path)

    # 保存图像并指定质量
    img.save(output_path, "WebP", quality=quality)

while True:
    try:
        li=showDir()
        ta=int(input("输入压缩目标："))
        pa=li[ta]
        print("压缩图片：",pa)
        name=str(pa)[:pa.find(".")]
        subfix=str(pa)[pa.rfind("."):]
        quaali=int(input("输入压缩后质量(1~100)："))
        compress_image(pa, name+"压缩"+subfix, quality=quaali)
        print("压缩成功，输出名:"+name+"压缩"+subfix)
    except Exception as e:
        print(e)
