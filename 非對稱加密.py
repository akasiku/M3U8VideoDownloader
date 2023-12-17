import os
import re

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
def getnum():
    star=input("输入操作:")
    try:
        star=int(star)
        if(star not in [1,2]):
            print("只能輸入1或2")
            return getnum()
        return star
    except:
        print("输入錯誤!!!!")
        return getnum()
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

while True:
    try:
        print("##############################非對稱加密########################################")
        print("1:加密     2:解密 ")
        op=getnum()
        if(op==1):
            dirlist=showDir()
            chose=input("選擇要加密的文件:")
            file_name=filter(chose,dirlist)
            print("####################生成公鑰和私鑰####################")
            # 生成RSA密钥对,key_size常见的密钥长度包括2048位、3072位和4096位等。长度越长越安全,但是加密时间长
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            public_key = private_key.public_key()
            #讀取文本
            with open(f"{file_name}","rb") as origin:
                 #加密文本
                encrypted_message = public_key.encrypt(origin.read(),padding.PKCS1v15())
            print("加密成功，創建加密文件")
            target = open(f"(lock){file_name}","wb")
            target.write(encrypted_message)
            target.close()
            with open("private_key.pem", "wb") as pri:
                pri.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8,
                                  encryption_algorithm=serialization.NoEncryption()))
                print("保存私鑰成功")

            # 保存公鑰字節到文件
            with open("public_key.pem", "wb") as pub:
                pub.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo))
                print("保存公鑰成功")

            print("######加密成功！！！請妥善保存密鑰，一旦遺失無法永遠無法解密#########")
        else:
            dirlist=showDir()
            chose = input("選擇要解密的文件:")
            file_name = filter(chose,dirlist)
            dirlist=showDir()
            chose_key = input("選擇解密的私鑰密鑰（pem文件）:")
            key_name = filter(chose_key, dirlist)
            # #讀取密鑰文件，並生成密鑰對象
            with open(f"{key_name}", "rb") as key:
                with open(f"{file_name}", "rb") as lock:
                    private_key = serialization.load_pem_private_key(key.read(), password=None,
                                                                     backend=default_backend())
                    file_content = lock.read()

                    # padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()),algorithm=hashes.SHA512(), label=None)
                    decrypted_message = private_key.decrypt(file_content,padding.PKCS1v15())
                    with open(f"(unlock){file_name}", "wb") as tar:
                        tar.write(decrypted_message)
            print("解密成功！！！！！！！")
    except Exception as e:
        print("失败！！！！！！")
        print(e)
