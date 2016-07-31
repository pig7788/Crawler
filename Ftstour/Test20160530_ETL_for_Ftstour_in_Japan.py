
# coding: utf-8

# In[20]:

import requests, math, re, time, json
from bs4 import  BeautifulSoup as bs


# ## 抓取連結資料

# In[22]:

rs = requests.session()
res = rs.get('http://group.ftstour.com.tw/FTS_Group_Index/IndexSearchG.aspx?ITN_AREA=0006&ITN_NATN=JP&ITN_CITY=&USE_BDT=2016/05/30&USE_EDT=2016/06/30&AIR_PT=&KEYWORD=')
soup = bs(res.text, "lxml")
with open('E:\\BigData\\Project\\Travel\\Ftstour\\Japan\\Link\\bid_list_for_Ftstour_in_Japan.txt', 'w') as fileWrite:
    for item in soup.select('div#tab td a'):
        if re.search('GroupDetail.*', item['href']) is not None:
            fileWrite.write('http://group.ftstour.com.tw/FTS_Group_Index/' + item['href'] + '\n')


# ## 檢查連結是否有重複

# In[23]:

def checkUrl(linkFilePath, areaName):
    check = {}
    num = 0
    checkedPathFormat = 'E:\\BigData\\Project\\Travel\\Ftstour\\Japan\\Link\\Checked\\checked_bid_list_for_Ftstour_in_{}.txt'
    checkedPath = checkedPathFormat.format(areaName)
    #上面兩行將路徑字串空格填入
    for bid_url in open(linkFilePath, 'r'): #讀取網頁
        num += 1
        strName = bid_url.strip().split('GRUP_CD=') #將最後的mgrupCd，切割成為獨立可判斷是否有重複的號碼
        firstGrupCD = re.search('\w*.\w*', strName[1].strip())
        secondGrupCD = re.search('\w*.\w*', strName[2].strip())
        linkName = firstGrupCD.group(0) + '_' + secondGrupCD.group(0)
        if linkName not in check: #判斷如果為true，則執行下列程式碼，並且存入檢查的字典
            print 'No.' + str(num) + ', ' + linkName +  ' is new, and added in check.'
            check[linkName] = bid_url
        else: #若false則印出重複的mgrupCd，以及網址
            print 'No.' + str(num) + ', ' + linkName + ' is existed, and not added in check.'
            print 'Url: ' + bid_url.strip()
    with open(checkedPath, 'w') as fileWrite: #將字典內的網址寫入檔案中
        for checked_linkName in check:
            fileWrite.write(check[checked_linkName])


# In[24]:

checkUrl('E:\\BigData\\Project\\Travel\\Ftstour\\Japan\\Link\\bid_list_for_Ftstour_in_Japan.txt', 'Japan')


# ## 計算檢查後加入的連結數量

# In[25]:

def countCheckedUrl(areaName): #輸入旅遊行程地區名稱
    linkFileFormat = 'E:\\BigData\\Project\\Travel\\Ftstour\\Japan\\Link\\Checked\\checked_bid_list_for_Ftstour_in_{}.txt'
    linkFilePath = linkFileFormat.format(areaName)
    #以上做字串的填入
    count = 0 #計算次數
    for lines in open(linkFilePath, 'r'): #計算有多少個數量
        count += 1
    return count #回傳值


# In[26]:

countCheckedUrl('Japan')


# ## 抓取旅遊方案細項資料

# In[27]:

def get_TourInfo(areaName):
    linkFileFormat = 'E:\\BigData\\Project\\Travel\\Ftstour\\Japan\\Link\\Checked\\checked_bid_list_for_Ftstour_in_{}.txt'
    linkFilePath = linkFileFormat.format(areaName)
    savedFileFormat = 'E:\\BigData\\Project\\Travel\\Ftstour\\Japan\\Data\\totalTravel_for_Ftstour_in_{}.json'
    savedFilePath = savedFileFormat.format(areaName)
    errorFileFormat = 'E:\\BigData\\Project\\Travel\\Ftstour\\Japan\\Data\\Error\\error_bid_list_for_Ftstour_in_{}.txt'
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
                itemDetail['title'] = soup.select('span#GroupTitle')[0].text.strip() #以下依照各個key、value丟入字典裡

                agency = re.search('\S.{5}', soup.select('title')[0].text.strip())
                itemDetail['agency'] = agency.group(0).strip()

                itemDetail['prodNo'] = soup.select('td.go-tour-td-color02')[2].text.strip()
                
                itemDetail['href'] = bid_url.strip()

                days = 0 #計算天數
                for tourContent in soup.select('td.go-everyday-td02a'): #行程內容
                    days += 1
                    daysTour['day{}'.format(days)] = tourContent.text.strip()
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


# In[28]:

get_TourInfo('Japan')

