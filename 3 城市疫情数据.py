import requests
import re
import time


headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
           }

url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0'

datum = []
response = requests.get(url,headers=headers)
content = response.content.decode("utf8","ignore")

date = time.strftime('%Y-%m-%d', time.localtime())
time = time.strftime('%H-%M', time.localtime())

details = re.findall('(vinceName":".*?){"pro', content, re.DOTALL)[1:]

for detail in details:   

    prov = re.findall('vinceName":"(.*?)"', detail, re.DOTALL)
    cities = re.findall('{"cityName":"(.*?)"', detail, re.DOTALL)
    cities_currentconfirmeds = re.findall('{"cityName":".*?"currentConfirmedCount":(\d*?),', detail, re.DOTALL)
    cities_confirmeds = re.findall('{"cityName":".*?"confirmedCount":(\d*?),', detail, re.DOTALL)
    cities_cureds = re.findall('{"cityName":".*?"curedCount":(\d*?),', detail, re.DOTALL)
    cities_deads = re.findall('{"cityName":".*?"deadCount":(\d*?),', detail, re.DOTALL)

    for city,city_currentconfirmed,city_confirmed,city_cured,city_dead in zip(cities,cities_currentconfirmeds,cities_confirmeds,cities_cureds,cities_deads):
            data = {
                   "日期":date,
                   "时间":time,
                   "省份":prov[0],
                   "城市/区县":city,
                   "当前确诊":city_currentconfirmed,
                   "累计确诊":city_confirmed,
                   "累计治愈":city_cured,
                   "累计死亡":city_dead,
                    }
            datum.append(data)

detail = re.findall('({"provinceName":"西藏自治区".*?)catc', content, re.DOTALL)[0]
prov = '西藏自治区'
cities = re.findall('"cityName":"(.+?)"', detail, re.DOTALL)
cities_currentconfirmeds = re.findall('{"cityName":".*?"currentConfirmedCount":(\d*?),', detail, re.DOTALL)
cities_confirmeds = re.findall('{"cityName":".*?"confirmedCount":(\d*?),', detail, re.DOTALL)
cities_cureds = re.findall('{"cityName":".*?curedCount":(\d+?),"', detail, re.DOTALL)
cities_deads = re.findall('{"cityName":".*?"deadCount":(\d+?),"', detail, re.DOTALL)
for city,city_currentconfirmed,city_confirmed,city_cured,city_dead in zip(cities,cities_currentconfirmeds,cities_confirmeds,cities_cureds,cities_deads):
    data = {
           "日期":date,
           "时间":time,
           "省份":prov,
           "城市/区县":city,
           "当前确诊":city_currentconfirmed,
           "累计确诊":city_confirmed,
           "累计治愈":city_cured,
           "累计死亡":city_dead,
           }
    datum.append(data)

import xlwt

workbook = xlwt.Workbook(encoding='utf8')
#添加worksheet
sheet1 = workbook.add_sheet('{} {}'.format(date,time))

#写入keys代表的列名
keys = list(datum[0].keys())#取出hots内第1个字典的健值作为样例
for i,key in zip(range(len(keys)),keys):#range()和keys都是list，因此可以打包迭代
    sheet1.write(0,i,key)

#写入数据内容
for row in range(1,len(datum)+1,1):#定义写入的行数范围
    for col,key in zip(range(len(keys)),keys):
    #与写入列名逻辑一致,col既代表所需写入的列数，也代表zip打包后健值的序号
        sheet1.write(row,col,str(datum[row-1][key]))
        #需写入的内容为比需要写入行数小1位的[row-1]、满足健值要求的[key]对应内容
        #str是避免出现一些内容没来得及转化为str

workbook.save(r'D:\OneDrive\OneDrive - 上汽大众汽车有限公司\0 Recent\新型冠状病毒\1 全国数据\6 疫情数据Backup\3 城市\城市疫情数据{} {}.xls'.format(date,time))

