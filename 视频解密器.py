import Crypto.Cipher.AES
import requests

k=input("输入密码URL:")
t=input("输入文件准确地址:")
name=input("为解密文件的命名：")
key=requests.get(k).content
print(f"密码为{key}")
print("正在解密中，请等待")
def decryptor(key,text):
    de=Crypto.Cipher.AES.new(key,IV=b"0000000000000000",mode=Crypto.Cipher.AES.MODE_CBC)
    return de.decrypt(text)
f=open(fr"{t}","rb")
k=open(fr"{name}.mp4","wb")
k.write(decryptor(key,f.read()))
print("解密完成！")
a=input()