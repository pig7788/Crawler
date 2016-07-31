
# coding: utf-8

import requests, uniout, re, time
from bs4 import BeautifulSoup as bs
from requests.exceptions import ConnectionError
from datetime import datetime


def pageLink(writtenFilePath, BoardName, startPageNum, endPageNum):
    with open(writtenFilePath, 'w') as linkWrite:
        url = 'https://www.ptt.cc/bbs/{}/index{}.html'
        for pageNum in range(startPageNum, endPageNum + 1):
            bid_url = url.format(BoardName, pageNum)
            linkWrite.write(bid_url + '\n')

            
def detailedLink(readFilePath, writtenFilePath):
    with open(writtenFilePath, 'w') as dataLinkWrite:
        for bid_url in open(readFilePath, 'r'):
            try:
                res = requests.get(bid_url.strip())
                soup = bs(res.text, "lxml")
                for index in range(0, len(soup.select('div.r-ent'))):
                    dataLinkWrite.write('https://www.ptt.cc/' + soup.select('div.title a')[index]['href'] + '\n')
                print '-' * 10 + bid_url.strip() + ' is done!!' + '-' * 10
                time.sleep(2)
            except:
                print '-' * 10 + bid_url.strip() + ' is error!!' + '-' * 10
                continue

                
def linkCount(filePath):
    count = 0
    for lines in open(filePath):
        count += 1
    print count

    
def getRawData(readFilePath, writtenFilePath, errorFilePath):
    with open(writtenFilePath + '\CrawlerLog.txt', 'a') as logWrite:
        with open(errorFilePath, 'a') as errorDataWrite:
            start = time.time()
            dataCount = 0
            for bid_url in open(readFilePath):
                try:
                    urlName = bid_url.strip().split('/')[6].split('.html')
                    newWrittenFilePath = (writtenFilePath + '\{}.txt').format(urlName[0])
                    res = requests.get(bid_url.strip())
                    soup = bs(res.text, "lxml")
                    with open(newWrittenFilePath, 'w') as dataWrite:
                        dataWrite.write(str(soup))
                    logTime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                    logWrite.write('-' * 10 + urlName[0] + ' is done at %s' % logTime + '-' * 10 + '\n')
                    dataCount += 1
                    time.sleep(2)
                except:
                    errorDataWrite.write(bid_url)
                    errorTime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                    print '-' * 10 + urlName[0] + ' is error at %s' % errorTime + '-' * 10
                    time.sleep(30)
                    continue
            end = time.time()
    finishTtime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
    print 'Data Quantites：%i' % dataCount
    print '完成時間：%s' % finishTtime
    print '總耗時：%f 秒' % (end - start)