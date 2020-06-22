from selenium import webdriver
import time
import pandas as pd
import random
from selenium.webdriver.support.ui import WebDriverWait#用于导入显式等待代码
from selenium.webdriver.support import expected_conditions as EC#用于引入满足条件
from selenium.webdriver.common.by import By#用于设置条件

driver_path = r"E:\chromedriver.exe"

driver = webdriver.Chrome(executable_path=driver_path)

url = "https://news.qq.com/zt2020/page/beijing.htm?from=timeline&isappinstalled=0"

driver.get(url)
#模拟点击
date = driver.find_element_by_xpath('//div[@class="timeNum"]')
date = date.get_attribute('textContent').strip()[4:18] + "时"

provs = driver.find_elements_by_xpath('//div[@class="provGroup"]/div[@class="line way "]//div[@class="context"]')
jizhongs = driver.find_elements_by_xpath('//div[@class="provGroup"]/div[@class="line way "]/div[2]/div[@class="short"]')
jujias = driver.find_elements_by_xpath('//div[@class="provGroup"]/div[@class="line way "]/div[3]/div[@class="short"]')
hesuans = driver.find_elements_by_xpath('//div[@class="provGroup"]/div[@class="line way "]/div[4]/div[@class="short"]')
lvmas = driver.find_elements_by_xpath('//div[@class="provGroup"]/div[@class="line way "]/div[5]/div[@class="short"]')
provss = []
for prov in provs:
    prov_text = prov.get_attribute('textContent')
    provss.append(prov_text)
jizhongss = []
for jizhong in jizhongs:
    jizhong_text = jizhong.get_attribute('textContent')
    jizhongss.append(jizhong_text.strip())
jujiass = []
for jujia in jujias:
    jujia_text = jujia.get_attribute('textContent')
    jujiass.append(jujia_text.strip())
hesuanss = []
for hesuan in hesuans:
    hesuan_text = hesuan.get_attribute('textContent')
    hesuanss.append(hesuan_text.strip())
lvmass = []
for lvma in lvmas:
    lvma_text = lvma.get_attribute('textContent')
    lvmass.append(lvma_text.strip())

data = [jizhongss, jujiass, hesuanss, lvmass]    
df = pd.DataFrame(data,columns=provss,index=['集中隔离','居家隔离','核酸检测','绿码通行']).T
df.to_excel('北京出行管控一览{}.xlsx'.format(date))
