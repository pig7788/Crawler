
# coding: utf-8


import requests, re, codecs, time
from bs4 import BeautifulSoup as bs
from datetime import datetime



def getUrl(commonPath, startPage, endPage):
    savePath = commonPath + '\Link\\total_DetailedLink_Backpackers_TourAgency.txt'
    with open(savePath, 'w') as urlWrite:
        urlCheck = dict()
        headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'bbkz_sessionhash=f39d8c4b118aeb99de5f0553eb2fb124; bbkz_lastvisit=1466571591; __gads=ID=c2e4e7d026b9391b:T=1466571591:S=ALNI_MZTLqiuW_BNy_hbxtByyDRN6qAkaw; bbkz_infobar=10; bbkz_forum_view=59fc056aae1260d440f242df848c73e87fa9533ba-3-%7Bi-4_i-1466571663_i-57_i-1466571671_i-108_i-1466571904_%7D; bbkz_lastactivity=0; _ga=GA1.3.1874273447.1466571590',
        'Host':'www.backpackers.com.tw',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        for page in range(startPage, endPage + 1):
            try:
                url = 'http://www.backpackers.com.tw/forum/forumdisplay.php?f=108&order=desc&page={}'
                res = requests.get(url.format(page), headers = headers)
                soup = bs(res.text, "lxml")
                for bid_url in soup.select('tbody#threadbits_forum_108 td.alt1 a'):
                    if bid_url['href'] == '#' or re.search('newpost', bid_url['href']) is not None:
                        pass
                    elif bid_url['href'] not in urlCheck:
                        urlCheck[bid_url['href']] = bid_url['href']
                        urlWrite.write('http://www.backpackers.com.tw/forum/' + bid_url['href'] + '\n')
                    else:
                        print bid_url['href'], urlCheck[bid_url['href']]
                time.sleep(2)
            except:
                errorTime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                print '-' * 10 + bid_url['href'] + ' is error at %s' % errorTime + '-' * 10
                time.sleep(20)
                continue


def getRawData(commonPath):
    dataCount = 0
    start = time.time()
    readPath = commonPath + '\Link\\total_DetailedLink_Backpackers_TourAgency.txt'
    errorDataPath = commonPath + '\Data\TourAgency\errorRawDataLink\errorDataLink_Backpackers_TourAgency.txt'
    with open(errorDataPath, 'w') as errorWrite:
        for bid_url in open(readPath, 'r'):
            try:
                headers = {
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Cookie':'bbkz_sessionhash=f39d8c4b118aeb99de5f0553eb2fb124; bbkz_lastvisit=1466571591; __gads=ID=c2e4e7d026b9391b:T=1466571591:S=ALNI_MZTLqiuW_BNy_hbxtByyDRN6qAkaw; bbkz_infobar=10; bbkz_forum_view=59fc056aae1260d440f242df848c73e87fa9533ba-3-%7Bi-4_i-1466571663_i-57_i-1466571671_i-108_i-1466571904_%7D; bbkz_lastactivity=0; _ga=GA1.3.1874273447.1466571590',
                    'Host':'www.backpackers.com.tw',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
                }
                res = requests.get(bid_url.strip(), headers = headers)
                soup = bs(res.text, "lxml")
                if re.search('page=', bid_url.strip().split('/')[4].split('t=')[1]) is not None:
                    newFileName = re.sub('=', '_', bid_url.strip().split('/')[4].split('t=')[1])
                else:
                    newFileName = bid_url.strip().split('/')[4].split('t=')[1]
                savePath = commonPath + '\Data\TourAgency\RawData\%s.txt' % newFileName
                with open(savePath, 'w') as rawDataWrite:
                    rawDataWrite.write(str(soup))
                dataCount += 1
                time.sleep(2)
            except:
                errorWrite.write(bid_url)
                errorTime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                print '-' * 10 + bid_url.strip() + ' is error at %s' % errorTime + '-' * 10
                time.sleep(20)
                continue
    end = time.time()
    finishTtime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
    print '-' * 20
    print 'Data Quantites：%i' % dataCount
    print '完成時間：%s' % finishTtime
    print '總耗時：%f 秒' % (end - start)