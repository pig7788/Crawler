
# coding: utf-8

# In[2]:

import requests, math, re, time, json
from bs4 import  BeautifulSoup as bs


# ## 利用Selenium讀取網站資料，並且將網址寫入

# In[118]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

driver = webdriver.Firefox() #使用Firefox開啟網頁
driver.implicitly_wait(3) #等待秒數
base_url = "http://www.ggogo.com/" #基底網址
driver.verificationErrors = []
driver.accept_next_alert = True
driver.get(base_url + "/event/japan-tokyo-tour/index.htm") #取得目標網址

res = driver.page_source #取得目標網址內的程式碼
soup = bs(res, "lxml") #萃取程式碼
a_tag = soup.select('div.frame a')
with open('E:\\BigData\\Project\\Travel\\Ggogo\\Japan\\Link\\bid_list_for_Ggogo_in_Tokyo.txt', 'w') as fileWrite:
    for get_url in a_tag: #取得網址
        if len(get_url.text) > 0:
            fileWrite.write('http://www.ggogo.com' + get_url['href'] + '\n')
driver.close()


# ## 檢查連結是否有重複

# In[2]:

testUrl = 'http://www.ggogo.com/ggogoWeb/goProd.do?step=goStep1&mgrupCd=JFTP5R'
print testUrl.split('=')


# In[8]:

def checkUrl(linkFilePath, areaName):
    dicCheck = {} #宣告檢查的字典
    num = 0
    checkedPathFormat = 'E:\\BigData\\Project\\Travel\\Ggogo\\Japan\\Link\\Checked\\checked_bid_list_for_Ggogo_in_{}.txt'
    checkedPath = checkedPathFormat.format(areaName)
    #上面兩行將路徑字串空格填入
    for bid_url in open(linkFilePath, 'r'): #讀取網頁
        num += 1
        strName = bid_url.strip().split('=') #將最後的mgrupCd，切割成為獨立可判斷是否有重複的號碼
        linkName = strName[2].strip()
        if strName[2] not in dicCheck: #判斷如果為true，則執行下列程式碼，並且存入檢查的字典
            print 'No.' + str(num) + ', ' + linkName +  ' is new, and added in dicCheck.'
            dicCheck[linkName] = bid_url
        else: #若false則印出重複的mgrupCd，以及網址
            print 'No.' + str(num) + ', ' + linkName + ' is existed, and not added in dicCheck.'
            print 'Url: ' + bid_url.strip()
    with open(checkedPath, 'w') as fileWrite: #將字典內的網址寫入檔案中
        for checked_linkName in dicCheck:
            fileWrite.write(dicCheck[checked_linkName])


# In[9]:

checkUrl('E:\\BigData\\Project\\Travel\\Ggogo\\Japan\\Link\\bid_list_for_Ggogo_in_Tokyo.txt', 'Tokyo')


# ## 計算檢查後加入的連結數量

# In[10]:

def countCheckedUrl(areaName): #輸入旅遊行程地區名稱
    linkFileFormat = 'E:\\BigData\\Project\\Travel\\Ggogo\\Japan\\Link\\Checked\\checked_bid_list_for_Ggogo_in_{}.txt'
    linkFilePath = linkFileFormat.format(areaName)
    #以上做字串的填入
    count = 0 #計算次數
    for lines in open(linkFilePath, 'r'): #計算有多少個數量
        count += 1
    return count #回傳值


# In[11]:

countCheckedUrl('Tokyo')


# ## 抓取旅遊方案細項資料

# In[12]:

### 印出字典的key與value########
def PrintKeyValue(dic_in):
    for key, value in dic_in.iteritems():
        print key, ':', value


# In[3]:

def get_TourInfo(areaName):
    linkFileFormat = 'E:\\BigData\\Project\\Travel\\Ggogo\\Japan\\Link\\Checked\\checked_bid_list_for_Ggogo_in_{}.txt'
    linkFilePath = linkFileFormat.format(areaName)
    savedFileFormat = 'E:\\BigData\\Project\\Travel\\Ggogo\\Japan\\Data\\totalTravel_for_Ggogo_in_{}.json'
    savedFilePath = savedFileFormat.format(areaName)
    errorFileFormat = 'E:\\BigData\\Project\\Travel\\Ggogo\\Japan\\Data\\Error\\error_bid_list_for_Ggogo_in_{}.txt'
    errorFilePath = errorFileFormat.format(areaName)
    #以上皆是路徑的字串格式填入
    eachTravel = [] #放置所有細項資料於旅行方案集合
    totalTravel = {} #放置所有的旅行方案於總集合
    totalCount = 0
    errorCount = 0
    with open(errorFilePath, 'w') as errorFile:
        for bid_url in open(linkFilePath, 'r'):
            try:
                itemDetail = {} #放置所有細項資料集合
                daysTour = {} #放置day{}的value
                bid_detail = requests.get(bid_url.strip()) #將檔案中的網址，取得連線
                soup = bs(bid_detail.text, "lxml") #取得連線後，萃取取得的程式碼
                itemDetail['title'] = soup.select('span.t_b15')[0].text #以下依照各個key、value丟入字典裡

                agency = re.search('G\w*.{4}', soup.select('title')[0].text)
                itemDetail['agency'] = agency.group(0)

                strName = bid_url.strip().split('=')
                itemDetail['prodNo'] = strName[2].strip()
                
                itemDetail['href'] = bid_url.strip()

                i = 0 #因第X天，下一個td標籤內，就是放入行程細節，加上有同個階層的table、tbody、tr、td……
                      #因此需要找同個階層，但是第i個位置的行程細節內容
                days = 0 #計算天數
                for td in soup.select('table table table table table td'): #在第5層下的td開始搜尋
                    if re.search(u'第.*天', td.text.strip()) != None: #如果符合'第x天'的字串內容，且不為None，則為true
                        if len(td.text.strip()) == 5: #第X天的長度要剛好是5，則為true
                            days += 1
                            daysTour['day{}'.format(days)] = soup.select('table table table table table td')[i + 1].text.strip()
                            #在soup.select('table table table table table td')下找到第i+1個索引值，取出所對應到的內容
                    i += 1
                itemDetail['tour'] = daysTour #將每天不同的行程，以字典方式丟入itemDetail字典內，形成itemDetail[daysTour[days]]
                totalCount += 1 #計算數量
                print '----------------------------這是分隔線----------------------------'
                print 'days: ' + str(days) #印出天數
                print 'Url: ' + bid_url.strip() #印出網址
                eachTravel.append(itemDetail) #將每次完整個旅遊方案內容加入到，eachTravel的List內
                totalTravel['eachTravel'] = eachTravel #將全部的旅遊方案，一次加入到字典裡
                
            except:
                errorCount += 1 #計算出現錯誤的數量
                splitPID = bid_url.strip().split('=') #取得PID
                strPID = splitPID[2].strip()
                print '----------------' + strPID + ' is error!!----------------'
                errorFile.write(bid_url) #將出現錯誤的網址寫入

    with open(savedFilePath, 'w') as dataFile: #將最後的旅遊方案全部寫入
        json.dump(totalTravel, dataFile)
    
    print '----------------------------All datas are done!!!----------------------------'
    print 'Data Quantities: ' + str(totalCount)
    print 'Error Quantities: ' + str(errorCount)


# In[4]:

get_TourInfo('Tokyo')

