# 抓取首页左侧图书分类 Demo
import requests
from lxml import html
import re
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import WriteToFile

# 抓取书籍分类
def getBookCategroy():
    url = r'https://book.dangdang.com/'
    response = requests.get(url)
    urlText = response.text
    htmlElement = html.fromstring(urlText)

    bookBody = htmlElement.xpath('//div[@class="con flq_body"]')

    pattern = re.compile(r'_t9144$')

    bookCategory = {}
    i = 1
    # 第一层
    for firstItem in bookBody[0].xpath(r'./div'):
        tempStr = firstItem.xpath(r'./@name')[0]
        matchObj = pattern.search(tempStr) # 正则匹配符合条件的书籍分类
        if matchObj:
            first = {}
            firstChild = {}
            firstNo = 'B' + str(i)
            first['no'] = firstNo
            i += 1
            if len(firstItem.xpath(r'./dl/dt/a')) == 0:
                name = firstItem.xpath(r'./dl/dt/text()')[0].strip()
                first['href'] = ''
            else:
                name = firstItem.xpath(r'./dl/dt/a/@title')[0]
                first['href'] = firstItem.xpath(r'./dl/dt/a/@href')[0]

            # 第二层
            for twiceItem in firstItem.xpath(r'./div/div/div/dl'):
                twice = {}
                twiceChild = {}
                if len(twiceItem.xpath(r'./dt/a')) > 0:
                    twiceName = twiceItem.xpath(r'./dt/a/@title')[0]
                    twiceHref = twiceItem.xpath(r'./dt/a/@href')[0]

                    twiceNo = 'B' + str(i)
                    twice['no'] = twiceNo
                    twice['href'] = twiceHref
                    i += 1

                    # 第三层
                    for thirdItem in twiceItem.xpath(r'./dd'):
                        third = {}
                        third['no'] = 'B' + str(i)
                        i += 1
                        thirdName = thirdItem.xpath(r'./a/@title')[0]
                        third['href'] = thirdItem.xpath(r'./a/@href')[0]
                        third['child'] = {}
                        third['parent'] = twiceNo
                        twiceChild[thirdName] = third
                    
                    twice['child'] = twiceChild
                    twice['parent'] = firstNo
                    firstChild[twiceName] = twice

            first['child'] = firstChild
            first['parent'] = '0'
            bookCategory[name] = first
        else:
            continue
    return bookCategory

# 字典转列表
def transferToList(bookCategory):
    bookList = []
    for key1 in bookCategory:
        value = bookCategory[key1]
        bookList.append([key1, value['no'],value['href'], value['parent']])
        if len(value['child']) > 0:
            bookList.extend(transferToList(value['child']))
    return bookList

bookCategory = getBookCategroy()
bookList = transferToList(bookCategory)
header = ['name', 'no', 'href', 'parent']
WriteToFile.writeToCSV(r'./DangDang/BookCategory.csv', header, bookList)


