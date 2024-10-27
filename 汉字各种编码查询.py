while True:
    print("##################################汉字各种编码查询#################################################")
    a=input("输入你想查询的汉字：")
    print(f"“{a}”的国际码（Unicode（16进制））:{hex(ord(a))[2:]}H \t（10进制）:{ord(a)}")
    b=str(a.encode("gbk")).replace("\\x","")[2:-1]
    c=bin(int(b,16))[2:]
    w=hex(int(str(c[:8]),2)-128)[2:]
    x=hex(int(str(c[8:]),2)-128)[2:]
    q=int(f"{w}{x}",16)


    y=int(w,16)-32
    z=int(x,16)-32
    if len(str(y))==2 and len(str(w))==2:
        print(f"”{a}“的区位码：区码：{hex(y)}                 位码:{hex(z)}")
    elif len(str(y))==1 and len(str(w))==2:
        print(f"”{a}“的区位码：区码：0{hex(y)}                 位码{hex(z)}")
    elif len(str(y))==2 and len(str(w))==1:
        print(f"”{a}“的区位码：区码：0{hex(y)}                 位码{hex(z)}")
    print("-----------------区位码+2020H=国标码(旧)-----------------")
    print(f"”{a}“的国标码（旧）:{w}{x}H              （10进制）:{q}")
    print("-------------国标码(旧)+8080H=新的国标码(GBK编码,机内码)-----------------")
    print(f"”{a}“的gbk编码(16进制)H:{b} \t        (10进制):{int(b,16)}")
    b=str(a.encode("utf-8")).replace("\\x","")[2:-1]
    print(f"”{a}“的utf-8编码(16进制)H:{b} \t     (10进制):{int(b,16)}")

    try:
        b=str(a.encode("shift-jis")).replace("\\x","")[2:-1]
        print(f"”{a}“的shift-jis编码(16进制)H:{b} \t    (10进制):{int(b,16)}")
        b=str(a.encode("EUC-JP")).replace("\\x","")[2:-1]
        print(f"”{a}“的EUC-JP编码(16进制)H:{b} \t         (10进制):{int(b,16)}")
    except:
        pass