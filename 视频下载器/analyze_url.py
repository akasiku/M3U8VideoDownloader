import re
import requests

from common_func import remove_back_slash
from specific import get_xiaoya


def get_prefix_com(origenalUrl):
    return origenalUrl[:origenalUrl.find("com") + 3]

def get_subfix_com(origenalUrl):
    return origenalUrl[origenalUrl.find("com")+3:]

# 获取url，分析是页面的url还是视频流的url
def analyze(url, header, V_flag, encry_key):
    try:
        requests.get(url, header)
    except Exception as e:
        if requests.exceptions.SSLError == type(e):
            V_flag = False
    if url.endswith("m3u8"):
        return get_UrlList(url, header, V_flag, encry_key)
    else:
        return get_UrlList(get_m3u8_from_source(url, header, V_flag), header, V_flag, encry_key)

def get_UrlList(url_list, header, verify_flag, encry_key):
    li = []
    if url_list=="":
        return li,0
    f = requests.get(url_list, headers=header, verify=verify_flag).text
    x = re.finditer(",(?P<url>.*?)#", remove_ad(f), re.S)
    for i in x:
        sub_url = i.group("url").strip()
        if "http" not in str(sub_url):
            newsubrul = url_list[:url_list.rfind("/") + 1] + sub_url.split("/")[-1]
            li.append(newsubrul)
        else:
            li.append(sub_url)
    if requests.get(li[10], headers=header).status_code != 200:
        li = []
        x = re.finditer(",(?P<url>.*?)#", f, re.S)
        for i in x:
            sub_url = i.group("url").strip()
            newsubrul = get_prefix_com(url_list) + sub_url
            li.append(newsubrul)
    if ".key" in li[0]:
        xx = li[0].split('"')[-2]
        if xx.startswith("http"):
            encry_key = requests.get(xx, headers=header, verify=verify_flag).content
        else:
            encry_key = requests.get(url_list[:url_list.rfind("/") + 1] + xx, headers=header,
                                     verify=verify_flag).content
        li = li[1:]
    return li,encry_key

# 在源码获取查找m3u8连接
def get_m3u8_from_source(main_url, myhead, verify_flag):
    res = requests.get(main_url, headers=myhead)
    content = res.text
    pt1=get_m3u8_from_viode(content)
    if pt1 != False:
        return pt1
    pt2=get_xiaoya(main_url, myhead)
    if pt2!="":
        return pt2
    pt3=get_m3u8_from_common(content, myhead, verify_flag)
    if pt3!="":
        return pt3
    return ""

# 去除广告
def remove_ad(con):
    r=con.split("#EXT-X-DISCONTINUITY")
    result=""
    even=0
    for i in r:
        if (even%2)==0:
            result+=i
        even+=1
    return result

def get_m3u8_from_viode(content):
    # 放在json里面的话，直接获取
    pattern2key=r'"video":{"url":"https:\/\/'
    if pattern2key in content:
        pattern2=re.compile(r'"video":{"url":"(.*?)",')
        res1=pattern2.findall(content)
        if len(res1)!=0:
            return remove_back_slash(res1[0])
    return False

def get_m3u8_from_common(content,myhead,verify_flag):
    m3u8 = re.compile(r"http(?!.*http).*?\.m3u8")
    m3u8list = m3u8.findall(content)
    res_url = ""
    if m3u8list != None and len(m3u8list) != 0:
        res_url = remove_back_slash(m3u8list[0])
        abcs = res_url.split("/")
        prex = abcs[0] + "//" + abcs[2]
        m3 = requests.get(res_url, headers=myhead, verify=verify_flag).text
        real = m3.split("\n")
        if (len(real) > 10):
            return res_url
        for i in real:
            if "m3u8" in i:
                res_url = i
        res_url = prex + res_url
    return res_url