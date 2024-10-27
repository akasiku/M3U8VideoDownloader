def signal(percent):
    x = "-" * 100
    percent = int(percent * 100)
    x = ">" * percent + x[percent:]
    print("下载进度"+x)