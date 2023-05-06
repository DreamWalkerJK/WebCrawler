# 抓取首页左侧图书分类 Demo
import requests
from lxml import html
import re
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import FileOperation

# 获取分类编号
startNo = 1 
def getCategoryNo():
    global startNo
    no = 'C' + str(startNo)
    startNo += 1
    return no

# 抓取书籍分类
def getBookCategroy():
    url = r'https://book.dangdang.com/'
    response = requests.get(url)
    urlText = response.text
    htmlElement = html.fromstring(urlText)

    bookBody = htmlElement.xpath('//div[@class="con flq_body"]/div')

    pattern = re.compile(r'_t9144$')

    bookCategory = {}
    # 第一层
    for firstItem in bookBody:
        tempStr = firstItem.xpath(r'./@name')[0]
        matchObj = pattern.search(tempStr) # 正则匹配符合条件的书籍分类
        if matchObj:
            first = {}
            firstChild = {}
            firstNo = getCategoryNo()
            first['no'] = firstNo
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

                    twiceNo = getCategoryNo()
                    twice['no'] = twiceNo
                    twice['href'] = twiceHref

                    # 第三层
                    for thirdItem in twiceItem.xpath(r'./dd/a'):
                        third = {}
                        third['no'] = getCategoryNo()
                        thirdName = thirdItem.xpath(r'./@title')[0]
                        third['href'] = thirdItem.xpath(r'./@href')[0]
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
        bookList.append([key1, value['no'], value['href'], value['parent']])
        if len(value['child']) > 0:
            bookList.extend(transferToList(value['child']))
    return bookList

bookCategory = getBookCategroy()
bookList = transferToList(bookCategory)
header = ['categoryName', 'categoryNo', 'categoryHref', 'parent']
FileOperation.writeToCSV(r'./DangDang/Category.csv', header, bookList)


