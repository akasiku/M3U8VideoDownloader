import ast
import base64
import re


def arcde(byte,enc):
    try:
        rs=bytes(ast.literal_eval(byte)).decode(enc)
        return rs
    except:
        return False
def to_Decode(x,input_string):
    other=[]
    posi=[]
    for i in input_string.split("\\x"):
        if len(i)>2:
            posi.append(int(input_string.split("\\x").index(i)/2))
            other.append(i[2:])
    ll=re.compile(r"\\x(..)",re.S)
    hexlist=ll.findall(input_string)
    if len(hexlist)==0:
        return ""
    bytes_string = bytes.fromhex("".join(hexlist))
    decoded_string = bytes_string.decode(x)

    for x in range(len(posi),0,-1):
        decoded_string=decoded_string[:posi[x-1]]+other[x-1]+decoded_string[posi[x-1]:]
    return decoded_string
def to_Decodehex(x,input_string):
    other=[]
    posi=[]
    for i in input_string.split("%"):
        if len(i)>3:
            posi.append(int(input_string.split("%").index(i)/2))
            other.append(i[2:])
    ll=re.compile(r"%(..)",re.S)
    hexlist=ll.findall(input_string)
    if len(hexlist)==0:
        return ""
    bytes_string = bytes.fromhex("".join(hexlist))
    decoded_string = bytes_string.decode(x)
    for x in range(len(posi),0,-1):
        decoded_string=decoded_string[:posi[x-1]]+other[x-1]+decoded_string[posi[x-1]:]
    return decoded_string
def to_Decodeuni1(input_string):
    other=[]
    posi=[]
    for i in input_string.split("&#x"):
        if len(i)>5:
            posi.append(int(input_string.split("&#x").index(i)))
            other.append(i[5:])
    ll=re.compile(r"&#x(.{4})",re.S)
    hexlist=ll.findall(input_string)
    decoded_string=""
    for i in hexlist:
        decoded_string+=chr(int(i,16))
    for x in range(len(posi),0,-1):
        decoded_string=decoded_string[:posi[x-1]]+other[x-1]+decoded_string[posi[x-1]:]
    return decoded_string
def to_Decodeuni2(input_string):
    other=[]
    posi=[]
    for i in input_string.split("\\u"):
        if len(i)>4:
            posi.append(int(input_string.split("\\u").index(i)))
            other.append(i[4:])
    ll=re.compile(r"\\u(.{4})",re.S)
    hexlist=ll.findall(input_string)
    decoded_string=""
    for i in hexlist:
        decoded_string+=chr(int(i,16))
    for x in range(len(posi),0,-1):
        decoded_string=decoded_string[:posi[x-1]]+other[x-1]+decoded_string[posi[x-1]:]
    return decoded_string
def to_Decodeuninum(input_string):
    decode=""
    ll=re.compile(r"&#(.*?);",re.S)
    hexlist=ll.findall(input_string)
    for i in hexlist:
        decode+=chr(int(i))
    return decode
def base64decode(li,text):
    for u in li:
        try:
            print(base64.b64decode(text).decode(u))
            print("Base64解码:"+u+"^")
        except:
            pass
while True:
    li=[]
    li.append("ISO-8859-1")
    li.append("utf-8")
    li.append("utf-16")
    li.append("utf-32")
    li.append("gbk")
    li.append("shift-jis")
    li.append("ascii")
    li.append("euc-jp")
    print("#######################################################################################")
    t=input("输入要解码的编码:")
    if ("%" in t):
        for i in li:
            try:
                result=to_Decodehex(i,t)
                if len(result)==0:
                    print("请输入正确的编码,例如\\xe1\\xa2")
                    break
                print("此编码的编码方式为<",i,">的解码结果:")
                print(result)
            except:
                pass
            print()
    elif("\\x" in t):
        for i in li:
            res=arcde(t,i)
            if res!=False:
                print("此编码的编码方式为<",i,">的解码结果:")
                print(res)
    if("\\x" in t):
        for i in li:
            try:
                result=to_Decode(i,t)
                if len(result)==0:
                    print("请输入正确的编码,例如\\xe1\\xa2,或%a1%c5")
                    break
                print("此编码的编码方式为<",i,">的解码结果:")
                print(result)
            except:
                pass
    elif("&#x" in t):
        try:
            print("此编码的编码方式为<Unicode>,解码结果:")
            print(to_Decodeuni1(t))
        except:
            pass
    elif("\\u" in t):
        try:
            print("此编码的编码方式为<Unicode>,解码结果:")
            print(to_Decodeuni2(t))
        except:
            pass
    elif("&#" in t):
        try:
            print("此编码的编码方式为<Unicode>,解码结果:")
            print(to_Decodeuninum(t))
        except:
            pass
    else:
        for i in range(20):
            x = f"ISO-8859-{i}"
            li.append(x)
        base64decode(li,t)
    print()