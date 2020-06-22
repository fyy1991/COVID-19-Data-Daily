from selenium import webdriver
import time
import random
import re
from selenium.webdriver.support.ui import WebDriverWait#用于导入显式等待代码
from selenium.webdriver.support import expected_conditions as EC#用于引入满足条件
from selenium.webdriver.common.by import By#用于设置条件



driver_path = r"E:\chromedriver.exe"

driver = webdriver.Chrome(executable_path=driver_path)

url = "http://bmfw.www.gov.cn/yqfxdjcx/index.html"

driver.get(url)
time.sleep(random.uniform(1,2))
#模拟点击
datum = []

provs = driver.find_elements_by_xpath('//div[@class="choose-con"]//ul[@class="province"]//li')
for prov in provs:
    driver.execute_script("arguments[0].click();", prov)
    time.sleep(random.uniform(3,4))
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,'timeDate')))
    provtext = prov.get_attribute('textContent')
    cities = driver.find_elements_by_xpath('//div[@class="choose-con"]//ul[@class="city"]//li')
    for city in cities:
        driver.execute_script("arguments[0].click();", city)
        time.sleep(random.uniform(1,2)) 
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,'timeDate')))
        citytext = city.get_attribute('textContent')
        blocks = driver.find_elements_by_xpath('//div[@class="choose-con"]//ul[@class="block"]//li')
        for block in blocks:
            driver.execute_script("arguments[0].click();", block)
            time.sleep(random.uniform(1,2))
            WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,'timeDate')))
            blocktext = block.get_attribute('textContent')
#            risk = ""
#            times = ""
            risk = driver.find_element_by_xpath('//div[@class="search-content"]/div/span')
            times = driver.find_element_by_xpath('//div[@class="search-content"]/div/p')
            data = {
                    "省份":provtext,
                    "城市":citytext,                       
                    "地区":blocktext,
                    "风险等级":risk.get_attribute('textContent'),
                    "时间":times.get_attribute('textContent'),
                    }
            datum.append(data)
            
import xlwt
import time

date = time.strftime('%Y-%m-%d', time.localtime())
workbook = xlwt.Workbook(encoding='utf8')
#添加worksheet
sheet1 = workbook.add_sheet('sheet1')
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

workbook.save(r'F:\全国风险数据{}.xls'.format(date))