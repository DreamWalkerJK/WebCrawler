# 抓取首页左侧图书分类 Demo
import requests
from lxml import html
import re

url = r'https://book.dangdang.com/'
response = requests.get(url)
urlText = response.text
htmlElement = html.fromstring(urlText)

bookBody = htmlElement.xpath('//div[@class="con flq_body"]')

pattern = re.compile(r'_t9144$')

bookCategory = {}
for item in bookBody[0].xpath(r'./div'):
    tempStr = item.xpath(r'./@name')[0]
    matchObj = pattern.search(tempStr) # 正则匹配符合条件的书籍分类
    if matchObj:
        if len(item.xpath(r'./dl/dt/a')) == 0:
            name = item.xpath(r'./dl/dt/text()')[0].strip()
            href = ''
        else:
            name = item.xpath(r'./dl/dt/a/@title')[0]
            href = item.xpath(r'./dl/dt/a/@href')[0]
        bookCategory[name] = href
    else:
        continue

for key in bookCategory.keys():
    print('[{0}]---{1}'.format(key, bookCategory[key]))