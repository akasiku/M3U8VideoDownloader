import os
from cryptography.fernet import Fernet
import base64
import hashlib
import re

#加密文件
def encrpt_File(path,key):
    with open(path,"rb") as readFile:
        data=readFile.read()
        readFile.close()
    encryData=Fernet(key).encrypt(data)
    with open(f"{path.split('.')[-2]}locked.{path.split('.')[-1]}","wb") as writeFile:
        writeFile.write(encryData)
        writeFile.close()
    print("\n***************************\n加密成功,请确认加密文件.\n***************************\n")


#输入任意字符串,并获取32位的key
def get_Key(passworld):
    md5=hashlib.md5()
    md5.update(passworld.encode("utf-8"))
    key=base64.urlsafe_b64encode(md5.hexdigest().encode("utf-8"))
    return key


#解密文件
def decrpt_File(path,key):
    with open(path,"rb") as f:
        enData=f.read()
        f.close()
    try:
        data=Fernet(key).decrypt(enData)
        with open(f"{path.split('.')[-2]}unlocked.{path.split('.')[-1]}","wb") as f2:
            f2.write(data)
            f2.close()
        print("\n***************************\n解密成功,请确认解密文件.\n***************************\n")
    except:
        print("密码错误")

#获取所有文件
def showDir():
    dirlist = os.listdir()
    for i, j in enumerate(dirlist):
        print(f"{i}  -------->  {j}")
    return dirlist

#筛选文件
def filter(target, li):
    swa=[]
    if target.isnumeric():
        target=int(target)
        if target>len(li):
            target=len(li)-1
        return li[target]
    else:
        for x in li:
            if re.search(f"(?i){target}",x)!=None:
                swa.append(x)
        if len(swa)==0:
            input("没有找到,任意点击返回")
            return filter("",li)
        elif len(swa)==1:
            return swa[0]
        else:
            x = 0
            print("\n\nvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n")
            for i in swa:
                print(f"{i}------------------{x}")
                x+=1
            print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            n=input("找到以上文件,请选择:")
            return filter(n,swa)

#输入字符串,获取各种加密后的哈希值
def hashcrypt():
    print("#############################################################################################")
    text=input("输入你要加密的内容:")
    md5=hashlib.md5()
    sha1=hashlib.sha1()
    sha256=hashlib.sha256()
    sha512=hashlib.sha512()
    sha224=hashlib.sha224()
    sha3=hashlib.sha3_512
    md5.update(text.encode("utf-8"))
    sha1.update(text.encode("utf-8"))
    sha224.update(text.encode("utf-8"))
    sha256.update(text.encode("utf-8"))
    sha512.update(text.encode("utf-8"))
    print("md5加密",md5.hexdigest())
    print("sha1加密",sha1.hexdigest())
    print("sha224加密",sha224.hexdigest())
    print("sha256加密",sha256.hexdigest())
    print("sha512加密",sha512.hexdigest())
    print("base64加密",base64.b64encode(text.encode('utf-8')))
    print("UTF-8编码",text.encode("utf-8"))
    print("gbk编码",text.encode("gbk"))
    print("unicode编码",end=" ")
    for i in text:
        print(ord(i),end=" ")
    print()



while True:
    print("##############################文件加密解密器####################################")
    option=input("选择操作: 1.加密文件    2.解密文件    3.加密文本: ")
    if option=="1":
        print("------------------------文件加密------------------------------")
        dirlist=showDir()
        while True:
            try:
                namenum=input("输入要加密的文件番号或名字:")
                name=filter(namenum,dirlist)
                password=input(f"现在准备加密<<{name}>>,请设置密码:")
                encrpt_File(name,get_Key(password))
                break
            except:
                print("出现错误!请重试!")
    elif option=="2":
        print("------------------------文件解密------------------------------")
        dirlist=showDir()
        while True:
            try:
                namenum=input("输入要加密的文件番号或名字:")
                name=filter(namenum,dirlist)
                password=input(f"现在准备解密<<{name}>>,请输入密码:")
                decrpt_File(name,get_Key(password))
                break
            except Exception as e:
                print(e)
    elif option == "3":
        hashcrypt()
    else:
        print("输入错误!再次输入")