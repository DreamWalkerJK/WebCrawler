# 抓取首页左侧图书分类 Demo
import requests
from lxml import html
import re
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import FileOperation
from DangDang import BookDBOperator

# 抓取书籍分类
def getCategroyDict():
    url = r'https://book.dangdang.com/'
    response = requests.get(url)
    urlText = response.text
    htmlElement = html.fromstring(urlText)

    bookBody = htmlElement.xpath('//div[@class="con flq_body"]/div')

    pattern = re.compile(r'_t9144$')
    patternCategoryNo = re.compile(r'book-')

    bookCategory = {}
    startNo = 1
    # 第一层
    for firstItem in bookBody:
        tempStr = firstItem.xpath(r'./@name')[0]
        matchObj = pattern.search(tempStr) # 正则匹配符合条件的书籍分类
        if matchObj:
            first = {}
            firstChild = {}
            
            if len(firstItem.xpath(r'./dl/dt/a')) == 0:
                firstNo = 'C{0}'.format(startNo) # 抓取不到分类编号时，生成分类编号
                startNo += 1
                firstName = firstItem.xpath(r'./dl/dt/text()')[0].strip()
                first['href'] = ''
            else:
                firstNo = firstItem.xpath(r'./dl/dt/a/@nname')[0].strip()
                firstNo = patternCategoryNo.sub('C',firstNo).strip() # 对分类编号进行处理替换
                firstName = firstItem.xpath(r'./dl/dt/a/@title')[0].strip()
                first['href'] = firstItem.xpath(r'./dl/dt/a/@href')[0]
            
            first['no'] = firstNo

            # 第二层
            for twiceItem in firstItem.xpath(r'./div/div/div/dl'):
                twice = {}
                twiceChild = {}
                if len(twiceItem.xpath(r'./dt/a')) > 0:
                    twiceName = twiceItem.xpath(r'./dt/a/@title')[0]
                    twiceHref = twiceItem.xpath(r'./dt/a/@href')[0]

                    twiceNo = twiceItem.xpath(r'./dt/a/@nname')[0]
                    twiceNo = patternCategoryNo.sub('C',twiceNo).strip()
                    twice['no'] = twiceNo
                    twice['href'] = twiceHref

                    # 第三层
                    for thirdItem in twiceItem.xpath(r'./dd/a'):
                        third = {}
                        thirdNo = thirdItem.xpath(r'./@nname')[0]
                        thirdNo = patternCategoryNo.sub('C',thirdNo).strip()
                        third['no'] = thirdNo
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
            bookCategory[firstName] = first
        else:
            continue
    return bookCategory

# 分类字典转为列表
def transferToList(categoryDict):
    bookList = []
    for key1 in categoryDict:
        value = categoryDict[key1]
        bookList.append((value['no'], key1, value['href'], value['parent']))
        if len(value['child']) > 0:
            bookList.extend(transferToList(value['child']))
    return bookList

# 获取分类列表
def getCategoryList():
    categoryDict = getCategroyDict()
    categoryList = transferToList(categoryDict)
    return categoryList

# 获取分类列表写入文件或者数据库
def writeCategoryList(categoryList, isWriteToDB = 0):
    match isWriteToDB:
        case 0:
            header = ['categoryNo', 'categoryName', 'categoryHref', 'parent']
            FileOperation.writeToCSV(r'./DangDang/Category.csv', header, categoryList)
        case 1:
            BookDBOperator.insertDataListToDB('category', categoryList)
    


