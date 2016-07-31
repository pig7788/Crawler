
# coding: utf-8

# In[1]:

import requests, math, re, sys, time, json
from bs4 import  BeautifulSoup as bs


# In[2]:

rs = requests.session()
res = rs.get('http://vacation.eztravel.com.tw/pkgfrn/results/TPE/93?fullStatus=NONE')
soup = bs(res.text, "lxml")


# In[3]:

count  = soup.select('.v-line')[0].text.split(' ')
print count[1]
page = int(math.ceil(float(count[1]) / 18))
print page


# In[4]:

urlFormat = 'http://vacation.eztravel.com.tw/pkgfrn/results/TPE/93/{}?&fullStatus=NONE'
with open('E:\\BigData\\Project\\Travel\\EZTravel\\Japan\\Link\\bid_list_for_EZtravel_in_Kanto.txt','w') as f:
    for pageNum in range(1, page + 1):
        url = urlFormat.format(pageNum)
        res2 = rs.get(url)
        soup1 = bs(res2.text, "lxml")
        list_table = soup1.select('div#listTable')[0]
        for items in list_table.select('div.list-box.mainLinkBox'):
            f.write('http://vacation.eztravel.com.tw/pkgfrn/' + items.select('a')[0]['href'].split('/pkgfrn/')[1] + '\n')


# In[5]:

dicCheck = {} #宣告一個dic，稍後會將檔名(Key)跟網址(Value)一一放入
num = 0
for bid_url in open('E:\\BigData\\Project\\Travel\\EZTravel\\Japan\\Link\\bid_list_for_EZtravel_in_Kanto.txt','r'): #讀連結檔
    num += 1
    splitStr = bid_url.split('/') #將網址切割，並且丟入splitStr這個List裡
    linkName = splitStr[5].strip() + "_" + splitStr[6].strip() #將List[index]對應到的元素，以字串型式組合成dataNmae
    #用商品編號當作檔名
    if linkName not in dicCheck:
        print 'No.' + str(num) + ', ' + linkName +  ' is new, and added in dicCheck.'
        dicCheck[linkName] = bid_url
    else:
        print 'No.' + str(num) + ', ' + linkName + ' is existed, and not added in dicCheck.'
        print linkName, dicCheck[linkName] #若有重複，則print出重複的Key跟Value


# In[6]:

### 印出字典的key與value########
def PrintKeyValue(dic_in):
    for key, value in dic_in.iteritems():
        print key, ':', value 


# In[8]:

itemDetail = {} #放置所有細項資料集合
eachTravel = [] #放置所有細項資料於旅行方案集合
totalTravel = {} #放置所有的旅行方案於總集合
totalCount = 0
errorCount = 0
with open('E:\\BigData\\Project\\Travel\\EZTravel\\Japan\\Data\\Error\\error_list_for_EZtravel_in_Kanto.txt', 'w') as errorFile:
    #寫error檔
    for bid_url in open('E:\\BigData\\Project\\Travel\\EZTravel\\Japan\\Link\\bid_list_for_EZtravel_in_Kanto.txt', 'r'):
        #讀連結檔
        try: #使用try-except
            itemDetail = {} #放置所有細項資料集合
            daysTour = {} #放置day{}的value
            bid_detail = requests.get(bid_url.strip()) #讀取檔案中的連結
            soup2 = bs(bid_detail.text, "lxml") #萃取資料
            row = soup2.select('div#pkgfrnVisitHistory')[0]
            agency = soup2.select('div.container.tbShow')[0].text.strip().split()
            price = re.search('\d+', row.select('.price')[0].text) #利用正規表示法抓取價格
            plane = re.search('.\W{2,4}', row.select('div#flight-block1 span')[3].text) #利用正規表示法抓取航空公司名稱
            dayBlock = soup2.select('ol.day-block')[0]
            
            itemDetail['title'] = row.select('div.pro-title.css-td h1')[0].text #將個別資料丟入itemDetail字典中，以下相同
            itemDetail['agency'] = agency[0]
            itemDetail['prodNo'] = row.select('div.pro-id-right.css-td span')[0].text.strip() + ' ' + row.select('div.pro-id-right.css-td span')[1].text.strip()
            itemDetail['href'] = bid_url.strip()
            #因為EZtravel的網站資料較鬆散，且只有旅館跟行程有規律性，故特別獨立出來寫加入的方法
            daysTourFormat = 'day{}' #建立字串格式
            for indexTour in range(0,len(dayBlock.select('div.title-circle.title-circle-green.nth-day span'))):
                daysTourInput = daysTourFormat.format(dayBlock.select('div.title-circle.title-circle-green.nth-day span')[indexTour]) #這邊是天數，day{1}_Tour、day{2}_Tour……
                daysTour[daysTourInput] = row.select('div.day-box h4')[indexTour].text.strip()
                #這邊是索引值，row.select('div.day-box h4')[1].text.strip()、row.select('div.day-box h4')[2].text.strip()……
            itemDetail['tour'] = daysTour
            totalCount += 1 #計算有多少筆資料丟入JSON檔中

            print '----------------------------這是分隔線----------------------------'
            print 'days: ' + dayBlock.select('div.title-circle.title-circle-green.nth-day span')[-1].text #印出當前旅行方案的旅行天數
            print 'Url: ' + bid_url.strip()
            eachTravel.append(itemDetail)
            totalTravel['eachTravel'] = eachTravel

        except:
            errorCount += 1
            splitPID = bid_url.strip().split('/')
            strPID = splitPID[5].strip() + "_" + splitPID[6].strip()
            #當錯誤訊息出現時，印出是哪一筆資料出現錯誤
            print '----------------' + strPID + ' is error----------------'
                #將出現錯誤的資料網址，寫入txt檔中
            errorFile.write(bid_url)

with open('E:\\BigData\\Project\\Travel\\EZTravel\\Japan\\Data\\totalTravel_for_EZtravel_in_Kanto.json', 'w') as dataFile:
    #寫最後全部資料檔
    json.dump(totalTravel, dataFile)

print '----------------------------All datas are done!!!----------------------------'
print 'Data Quantities: ' + str(totalCount)
print 'Error Quantities: ' + str(errorCount)


# In[ ]:



