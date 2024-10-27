import base64
import hashlib
import random
import re

import base58
import requests
from ecdsa import SigningKey, SECP256k1
from bit import PrivateKeyTestnet,PrivateKey

#hash160
def hash160(pubkey):
    sha256 = hashlib.sha256(pubkey).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    return ripemd160

#double_sha256
def double_sha256(key):
    first_sha256=hashlib.sha256(bytes.fromhex(key)).digest()
    second_sha256=hashlib.sha256(first_sha256).hexdigest()
    return second_sha256

#私钥-->编码
def hex_to_encode_private_key(hex_private,net_flg):
    if(net_flg=="1"):
        a="80"+hex_private #主网,非压缩
        b="80"+hex_private+"01" #主网，压缩
    else:
        a="EF"+hex_private #测试网，非压缩
        b="EF"+hex_private+"01" #测试网，压缩

    #加入前缀后两次哈希256
    twice_hasha=double_sha256(a)#非压缩
    twice_hashb=double_sha256(b)

    # 取前四个字节作为校验和
    certificate_codea=twice_hasha[:8]
    certificate_codeab=twice_hashb[:8]

    #网络码+原16进制私钥+验校码
    final_codea=a+certificate_codea

    # 网络码+原16进制私钥+01+验校码
    final_codeb = b + certificate_codeab

    #非压缩格式的私钥WIF编码(用的少)
    akey=base58.b58encode(bytes.fromhex(final_codea)).decode("utf-8")
    # 压缩格式的私钥编码
    bkey = base58.b58encode(bytes.fromhex(final_codeb)).decode("utf-8")
    return bkey,akey

#编码-->私钥
def to_hex_private_key(encode_key):
    decode_key=base58.b58decode(encode_key).hex()
    #如果是74位说明是非压缩的编码：2位网络码+私钥hex+8位验校码
    if len(decode_key)==74:
        return decode_key[2:-8]
    # 如果是76位说明是压缩的编码：2位网络码+私钥hex+01+8位验校码
    elif len(decode_key)==76:
        return decode_key[2:-10]



#私钥-->公钥
def get_publickey(hex_private_key):
    # 生成ECDSA签名密钥
    sk = SigningKey.from_string(bytes.fromhex(hex_private_key), curve=SECP256k1)

    # 获取公钥
    vk = sk.get_verifying_key()

    public_key = b'\x02' + vk.to_string()[:32] if vk.to_string()[-1] % 2 == 0 else b'\x03' + vk.to_string()[:32]

    #获取未压缩的公钥
    umvk=sk.verifying_key

    # 获取非压缩格式的公钥 (04 + x坐标 + y坐标)
    uncompressed_public_key_bytes = b'\x04' + umvk.to_string()
    uncompressed_public_key=uncompressed_public_key_bytes.hex()

    return public_key.hex(),uncompressed_public_key

#私钥的base64表示
def private_to_base64(hex_private_key):
    f=base64.encodebytes(bytes.fromhex(hex_private_key)).decode("utf-8")
    return f

#公钥-->地址
def hex_public_to_address(hex_public_key):
    #hash160(先sha256再ripeMD160)
    h160=hash160(bytes.fromhex(hex_public_key))

    #添加00前缀
    res="00"+h160.hex()
    #将上面两次sha256，再取前4字节作为效验码
    hash2=double_sha256(res)

    #获取效验码
    certification_code=hash2[:8]

    #00+hash160的16进制+效验码
    resout=res+certification_code

    return base58.b58encode(bytes.fromhex(resout)).decode("utf-8")

#测试网地址
def get_test_umcompress_address(hex_puk):
    # 比特币测试网地址前缀
    prefix = b'\x6f'
    prefixed_pubkey_hash = prefix + hash160(bytes.fromhex(hex_puk))
    # 计算校验和
    checksum = double_sha256(prefixed_pubkey_hash.hex())[:8]
    # 生成最终地址
    test_address = base58.b58encode(prefixed_pubkey_hash + bytes.fromhex(checksum)).decode("utf-8")
    return test_address

#见证隔离地址生成
def pubkey_to_bech32_address(pubkey, prefix='bc'):
    # 从任意位大小转换为另一位大小的数据
    def convertbits(data, frombits, tobits, pad=True):
        acc = 0
        bits = 0
        ret = []
        maxv = (1 << tobits) - 1
        for value in data:
            acc = (acc << frombits) | value
            bits += frombits
            while bits >= tobits:
                bits -= tobits
                ret.append((acc >> bits) & maxv)
        if pad and bits:
            ret.append((acc << (tobits - bits)) & maxv)
        return ret

    # 计算SHA-256哈希值的RIPEMD-160哈希值
    ripemd160_hash = hash160(pubkey)

    # 将RIPEMD-160哈希值转换为5位块
    words = convertbits(ripemd160_hash, 8, 5)
    # 添加版本字节（0x00表示P2WPKH地址）
    words.insert(0, 0)

    # Bech32校验和计算
    def bech32_polymod(values):
        # Bech32校验和计算的常量
        GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
        chk = 1
        for v in values:
            b = chk >> 25
            chk = (chk & 0x1ffffff) << 5 ^ v
            for i in range(5):
                chk ^= GEN[i] if ((b >> i) & 1) else 0
        return chk

    def bech32_create_checksum(hrp, data):
        # 扩展人类可读部分（HRP）
        hrp_expanded = [ord(x) >> 5 for x in hrp]
        # 添加0字节和HRP的低5位
        values = hrp_expanded + [0] + [ord(x) & 31 for x in hrp] + data
        # 计算多项式并创建校验和
        polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
        return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

    def bech32_encode(hrp, data):
        # 创建完整的Bech32编码，附加校验和
        combined = data + bech32_create_checksum(hrp, data)
        # 使用字符集将数据转换为Bech32格式
        return hrp + '1' + ''.join('qpzry9x8gf2tvdw0s3jn54khce6mua7l'[d] for d in combined)

    # 生成给定公钥和前缀的Bech32地址
    return bech32_encode(prefix, words)

def get_radom_key():
    radom_pry=random.randbytes(32).hex()
    random_puk1,random_puk2=get_publickey(radom_pry)
    print("随机私钥: ",radom_pry)
    print("压缩公钥: ",random_puk1)
    print("非压缩公钥: ", random_puk2)
    print("压缩地址:",hex_public_to_address(random_puk1))
    print("非压缩地址:", hex_public_to_address(random_puk2))
    print("见证隔离地址:",pubkey_to_bech32_address(bytes.fromhex(random_puk1)))
he={"referer":"https://blockchair.com/",
"cookie":"_pk_ref.1.641f=%5B%22%22%2C%22%22%2C1724072219%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.1.641f=1; _bchr-cptch_challenge-mode=crypto; _bchr_valid_until_hash=172467722836f745a16d98fdba39e0d6f6d30a5289c2132078aa11c48c6c9541edf72100a8; XSRF-TOKEN=eyJpdiI6IjArSlRUcHM0WC96VWkxaytxT0d5VGc9PSIsInZhbHVlIjoiblBPa1Y2ekxWZXBtY2x3Vlg2SmE3T0xENGpRSy9TNkhJNkdJZlBwRmJNSUNRMzNSZlAwV1cwK2RGaTArVE01MldPcHNWcnBWVkJHK3J0VjRVVXByRlNFWWVwT0QvWVpkOFpnVGNpa2QrdFhlcnJYRm9ObmtZZWo1Tm1wSmdIVUIiLCJtYWMiOiI5N2I4MDc5YmMyOTcxZWVkODc3YWMxNjFmNzVmOTA5Y2QzYjVmNDBkMjU3NjMxMTk1MmM0NDRiYWU4YTU1ODY2IiwidGFnIjoiIn0%3D; whiskey_4_session=eyJpdiI6Ik91SWlsU1BIZnp3eHh3aUowU2RsbWc9PSIsInZhbHVlIjoiaW81bW5GNHo3Nk9NTG1HVmwyNTlOZVFmclZwczhmNmxWRThMOThXVWhSM1JjcjA3YURSSFRscmVrSHI3TlN2ZFprQUs0WlFFWHk5cHNVbmpjQVJNRTU0U3N6UllKb3ZjbG5mb1c1bnhsVDQxVFlaYlBMZTM4bGVhMFZNQUlobDMiLCJtYWMiOiJmMTIxMTJhNThmZDdmN2FmZjYzOWM4OGFmM2Q1ZWMzYTI3Mjc0ZWEwMGUwMmY2YTZlMzdiYjhlNDYzYjJiODA1IiwidGFnIjoiIn0%3D; _pk_id.1.641f=a6741cc149be085d.1722343970.13.1724072576.1724072219.",
    "user - agent":"Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 127.0.0.0 Safari / 537.36"}
def get_blance(adress):
    ur="https://blockchair.com/bitcoin/address/"+adress
    resa=requests.get(ur,headers=he)
    ress=resa.text
    f=re.search('<span class="color-text-success">(.*?)</span>\n                (.*?)\n        </span>',ress)
    if resa.status_code!=200:
        return "似乎cookie失效"
    if f!=None:
        ba=float(str(f[2]).strip())
        return ba
    else:
        return 0

while True:
    try:
        print("1:密钥解析 2:通过私钥查询地址余额 3:随机生成 4:通过地址查询余额")
        option=input("输入操作:")
        if option=="1":
            print("#######################################密钥解析########################################################################")
            PRK=""
            input_key=input("密钥:")
            key_length=len(input_key)
            flag=0
            if key_length==64 or key_length==51 or key_length==52:
                flag = 1
                hex_PRK=input_key
                if(key_length!=64):
                    print("输入的是编码后的私钥")
                    hex_PRK=to_hex_private_key(input_key)
                #输入的是16进制私钥
                PRK, uncompressPRK = hex_to_encode_private_key(hex_PRK,"1")
                TPRK, TuncompressPRK = hex_to_encode_private_key(hex_PRK, "2")
                PUK, uncompressPUC = get_publickey(hex_PRK)
                print("hex私钥: ", hex_PRK)
                #print("base64格式私钥:",private_to_base64(hex_PRK),end="")
                print("*压缩私钥:",PRK)
                print("未压缩私钥WIF:", uncompressPRK)
                print("*压缩公钥:",PUK)
                print("未压缩公钥:",uncompressPUC)
                print("*压缩地址:",hex_public_to_address(PUK))
                print("未压缩的地址:",hex_public_to_address(uncompressPUC))
                print("*见证隔离地址:",pubkey_to_bech32_address(bytes.fromhex(PUK)))
                print("压缩私钥(测试网):",TPRK)
                print("未压缩私钥(测试网):",TuncompressPRK)
                print("压缩地址(测试网):",get_test_umcompress_address(PUK))
                print("未压缩地址(测试网):",get_test_umcompress_address(uncompressPUC))
            elif key_length==66:
                flag = 2
                print("检测到你输入的是压缩公钥")
                print("压缩地址:", hex_public_to_address(input_key))
                print("见证隔离地址:", pubkey_to_bech32_address(bytes.fromhex(input_key)))
                print("压缩地址(测试网):", get_test_umcompress_address(input_key))
            elif key_length==130:
                flag = 3
                #输入的是未压缩的公钥
                print("检测到你输入的是非压缩公钥")
                print("未压缩地址:", hex_public_to_address(input_key))
                print("未压缩地址(测试网):", get_test_umcompress_address(input_key))
            if(flag==0):
                print("未检出出输入的密钥类型")
        elif option == "2":
            print("#######################################余额查询可能会花费几分钟########################################################################")
            input_key = input("密钥:")
            key_length = len(input_key)
            flag = 0
            if key_length == 64 or key_length == 51 or key_length == 52:
                flag = 1
                hex_PRK = input_key
                if (key_length != 64):
                    hex_PRK = to_hex_private_key(input_key)
                # 输入的是16进制私钥
                PRK, uncompressPRK = hex_to_encode_private_key(hex_PRK, "1")
                TPRK, TuncompressPRK = hex_to_encode_private_key(hex_PRK, "2")
                PUK, uncompressPUC = get_publickey(hex_PRK)

                # 只能输入编码后的私钥,压缩私钥控制压缩地址，非压缩私钥控制非压缩地址
                Balance1 = PrivateKey(PRK)
                print("*压缩私钥:", PRK)
                print("*压缩地址:", hex_public_to_address(PUK))
                print("余额:", Balance1.get_balance())
                Balance2 = PrivateKey(uncompressPRK)
                print("未压缩私钥WIF:", uncompressPRK)
                print("未压缩的地址:", hex_public_to_address(uncompressPUC))
                print("余额:", Balance2.get_balance())
                Balance3 = PrivateKeyTestnet(TPRK)
                print("压缩私钥(测试网):", TPRK)
                print("压缩地址(测试网):", get_test_umcompress_address(PUK))
                print("余额:", Balance3.get_balance())
                Balance4 = PrivateKeyTestnet(TuncompressPRK)
                print("未压缩私钥(测试网):", TuncompressPRK)
                print("未压缩地址(测试网):", get_test_umcompress_address(uncompressPUC))
                print("余额:", Balance4.get_balance())
            else:
                print("密钥错误")
        elif option == "4":
            adr=input("输入比特币地址:")
            print("该地址的余额为:",get_blance(adr))
        else:
            print("-------------------------随机生成密钥与地址---------------------------------")
            get_radom_key()
    except Exception as e:
        print(e)
