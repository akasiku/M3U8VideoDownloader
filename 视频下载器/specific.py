import re
import requests

from common_func import remove_back_slash


def get_xiaoya(url,head):
    res = requests.get(url,headers=head)
    cont = res.text
    com = re.compile(r'"source":\[(.*?)]]}')
    d = com.findall(cont)
    all_line = []
    for i in d:
        temp = []
        line = str(i).split(",")
        for episode in line:
            if "http" in episode or "m3u8" in episode:
                temp.append(remove_back_slash(episode))
        all_line.append(temp)
    ep=url.split("-")[-1]
    if str(ep).isnumeric():
        ep=int(ep)
    else:
        return ""
    return all_line[2][ep].replace('"',"").replace("]","")