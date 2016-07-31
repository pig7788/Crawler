
# coding: utf-8

import codecs, re, time
from bs4 import BeautifulSoup as bs
from datetime import datetime


def codesFile(linkPath, commonPath):
    codesPath = commonPath + '\CleanedData\Codes\Codes.txt'
    with open(codesPath, 'w') as codesWrite:
        for codes in open(linkPath, 'r'):
            if re.search('page=', codes.strip().split('/')[4].split('t=')[1]) is not None:
                    newCodes = re.sub('=', '_', codes.strip().split('/')[4].split('t=')[1])
            else:
                newCodes = codes.strip().split('/')[4].split('t=')[1]
            codesWrite.write(newCodes + '\n')
    print '-' * 10 + 'Codes are done!!' + '-' * 10


def removeTags(soup, removedTag):
    for tags in soup.select(removedTag):
        tags.extract()


def getRawData(commonPath, codes):
    rawDataPath = commonPath + '\RawData\%s.txt' % codes.strip()
    with codecs.open(rawDataPath, 'r', 'utf-8') as articleRead:
        soup = bs(articleRead.read(), "lxml")        
    return soup


def getArticle(soup):
    article = ''
    for context in soup.select('div.vb_postbit'):
        if len(soup.select('td.alt2.inner-quote')) > 0:
            removeTags(context, 'td.alt2.inner-quote')
            removeTags(context, 'div.smallfont')
        article += context.text.strip()
    return article


def articleFile(commonPath, codes, article):
    articlePath = commonPath + '\CleanedData\Article\%s_article.txt' % codes.strip()
    with codecs.open(articlePath, 'w', 'utf-8') as articleWrite:
        articleWrite.write(article)


def getCleanedFile(commonPath):
    dataCount = 0
    start = time.time()
    with open(commonPath + '\CleanedData\CleanedFileLog_TourAgency.txt', 'w') as logWrite:
        codesPath = commonPath + '\CleanedData\Codes\Codes.txt'
        for codes in open(codesPath, 'r'):
            try:
                soup = getRawData(commonPath, codes)
                article = getArticle(soup)
                articleFile(commonPath, codes, article)
                logTime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                logWrite.write('-' * 10 + codes.strip() + ' is done at %s' % logTime + '-' * 10 + '\n')
                dataCount += 1
            except:
                errorTime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                print '-' * 10 + codes.strip() + ' is error at %s' % errorTime + '-' * 10
    end = time.time()
    finishTtime = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
    print 'Data Quantites：%i' % dataCount
    print '完成時間：%s' % finishTtime
    print '總耗時：%f 秒' % (end - start)