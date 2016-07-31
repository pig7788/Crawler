
# coding: utf-8


import codecs, re, time
from bs4 import BeautifulSoup as bs
from datetime import datetime


def codesFile(linkPath, commonPath):
    codesPath = commonPath + '\CleanedData\Codes\Codes.txt'
    with open(codesPath, 'w') as codesWrite:
        for codes in open(linkPath, 'r'):
            newCodes = codes.strip().split('/')[6].split('.html')[0]
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
    removeTags(soup.select('div#main-content')[0], 'div.article-metaline')
    removeTags(soup.select('div#main-content')[0], 'span.article-meta-tag')
    removeTags(soup.select('div#main-content')[0], 'span.article-meta-value')
    removeTags(soup.select('div#main-content')[0], 'div.article-metaline-right')
    removeTags(soup.select('div#main-content')[0], 'div.push')
    removeTags(soup.select('div#main-content')[0], 'span.f2')
    rawArticle = soup.select('div#main-content')[0].text
    article = re.sub('--', '', rawArticle)
    article = re.sub(u'◆ From: (((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))', '', article)
    return article

def getPush(soup):
    pushes = ''
    for push in soup.select('div.push'):
        pushes += push.text
    return pushes


def articleFile(commonPath, codes, article):
    articlePath = commonPath + '\CleanedData\Article\%s_article.txt' % codes.strip()
    with codecs.open(articlePath, 'w', 'utf-8') as articleWrite:
        for setences in article:
            articleWrite.write(setences)

def pushFile(commonPath, codes, pushes):
    pushPath = commonPath + '\CleanedData\Push\%s_push.txt' % codes.strip()
    with codecs.open(pushPath, 'w', 'utf-8') as pushWrite:
        for push in pushes:
            pushWrite.write(push)


def getCleanedFile(commonPath):
    dataCount = 0
    start = time.time()
    with open(commonPath + '\CleanedData\CleanedFileLog_TourAgency.txt', 'w') as logWrite:
        codesPath = commonPath + '\CleanedData\Codes\Codes.txt'
        for codes in open(codesPath, 'r'):
            try:
                soup = getRawData(commonPath, codes)
                pushes = getPush(soup)
                article = getArticle(soup)
                articleFile(commonPath, codes, article)
                pushFile(commonPath, codes, pushes)
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