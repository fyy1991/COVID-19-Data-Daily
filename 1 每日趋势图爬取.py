import requests
import re
import time

url = "https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0"
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        }

response = requests.get(url, headers=headers)
content = response.content.decode('utf8')

date = time.strftime('%Y-%m-%d', time.localtime())
time = time.strftime('%H-%M', time.localtime())

trends_quanguo = re.findall('"quanguoTrendChart":(.*?),"hbFeiHbTrendChart"', content, re.DOTALL)[0]
trends_feiHB = re.findall('"hbFeiHbTrendChart":(.*?)catch', content, re.DOTALL)[0]
urls_quanguo = re.findall('"imgUrl":"(.*?\.png)"', trends_quanguo, re.DOTALL)
titles_quanguo = re.findall('"title":"(.*?)"', trends_quanguo, re.DOTALL)
urls_feiHB = re.findall('"imgUrl":"(.*?\.png)"', trends_feiHB, re.DOTALL)
titles_feiHB = re.findall('"title":"(.*?)"', trends_feiHB, re.DOTALL)

#以下为创建当天文件夹函数代码
def mkdir(path):
    import os# 引入模块
    path = path.strip()# 去除首尾空格
    path = path.rstrip("\\")# 去除尾部 \ 符号    
    isExists = os.path.exists(path)# 判断path是否存在，结果输出布尔值Ture/False
    if not isExists:# 判断结果
        os.makedirs(path)# 如果不存在则按照path创建目录
        print(path + ' 创建成功')
        return True
    else:        
        print(path + ' 目录已存在')# 如果目录存在则不创建，并提示目录已存在
        return False

mkdir("D:\\OneDrive\\OneDrive - 上汽大众汽车有限公司\\0 Recent\\新型冠状病毒\\1 全国数据\\6 疫情数据Backup\\趋势图\\" + date)#运行函数，\\表示绝对引用


for url_quanguo,title_quanguo in zip(urls_quanguo,titles_quanguo):
    response = requests.get(url_quanguo, headers=headers)
    content = response.content#变为bytes流数据
    title_quanguo = re.sub('/','&',title_quanguo)
    with open("D:\\OneDrive\\OneDrive - 上汽大众汽车有限公司\\0 Recent\\新型冠状病毒\\1 全国数据\\6 疫情数据Backup\\趋势图\\" + date + "\\" + date + " " + time + "全国" + "{}.png".format(title_quanguo), 'wb') as f:#wb表示为bytes流数据，w表示常规数据
            f.write(content)


for url_feiHB,title_feiHB in zip(urls_feiHB,titles_feiHB):
    response = requests.get(url_feiHB, headers=headers)
    content = response.content#变为bytes流数据
    title_feiHB = re.sub('/','&',title_feiHB)
    with open("D:\\OneDrive\\OneDrive - 上汽大众汽车有限公司\\0 Recent\\新型冠状病毒\\1 全国数据\\6 疫情数据Backup\\趋势图\\" + date + "\\" + date + " " + time + "非湖北"+ "{}.png".format(title_feiHB), 'wb') as f:#wb表示为bytes流数据，w表示常规数据
            f.write(content)
