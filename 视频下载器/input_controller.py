def input_url():
    url=input("輸入url:")
    while not url.startswith("http"):
        url=input("输入错误，请输入http开头的连接:")
    return url
