import requests


def scanUrl(url):
    try:
        data = requests.get(url, timeout=1).text
    except:
        print("EXCEPTION")
        return []
    urls = []
    nextIndex = 0
    while nextIndex != -1:
        nextIndex = data.find("https://www")
        data = data[nextIndex:]
        v1 = data.find("\\")
        if v1 == -1:
            quotationIndex = data.find('"')
        else:
            quotationIndex = min(data.find('"'), v1)
        if len(data[:quotationIndex]) <= 100:
            urls.append(data[:quotationIndex])
        data = data[quotationIndex:]
    return urls


urls = {}
toScan = ["https://youtube.com"]
scanned = []
while True:
    nextURL = toScan[0]
    print(nextURL)
    toScan.pop(0)
    scanned.append(nextURL)
    newUrls = scanUrl(nextURL)
    for url in newUrls:
        if urls.get(url) is not None:
            urls[url] += 1
        else:
            urls[url] = 1
        if url not in scanned and url not in toScan:
            toScan.insert(0, url)
    if len(scanned) % 10:
        with open("out.json", "w", encoding='utf-8') as f:
            f.write(str(urls))
    print(f"To scan: {len(toScan)}")
    print(f"Scanned: {len(scanned)}")
