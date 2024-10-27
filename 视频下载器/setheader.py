def set_header(header):
    def setheader1():
        he = input("")
        if he == "":
            pass
        else:
            k = he.split(": ")
            header[k[0]] = k[1].strip()
            setheader1()
    s=0
    while True:
        if s==2:
            break
        x = input("")
        if x.strip().endswith(":"):
            headerkey=x.strip()[:-1]
        if x.strip().endswith(":")==False and ": " in x:
            setheader1()
            break
        if x=="\n" or x=="":
            s+=1
        else:
            if x.startswith("\"") and x.endswith("\""):
                if headerkey.startswith(":"):
                    headerkey=headerkey[1:]
                header[headerkey] = x[1:-1]
            else:
                if headerkey.startswith(":"):
                    headerkey=headerkey[1:]
                header[headerkey]=x
            s=0