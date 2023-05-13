import time
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
import requests
from lxml import html
import random
import re
import traceback
from CustomTool import GetRandomTime,FileOperation,StringOperation
from DangDang import BookDBOperator

# 抓取图书
def getBook(dataList):
    csvHeader = ['bookNo', 'bookName', 'bookHref', 'bookPrice', 'bookPrePrice', 'author', 'press', 'bookStore', 'categoryNo']
    useAgentList = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.197.400 QQBrowser/11.7.5287.400",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36"
    ]

    pattern = re.compile('(pg[0-9]+-)+')
    patternBookName = re.compile(r'[【](.*)[】]')
    for data in dataList:
        categoryNo = data[0]
        url = data[1]
        totalPage = int(data[3])
        startPage = 1
        while startPage <= totalPage:
            startPage += 1
            bookList = []
            try:
                header = {'User-Agent': random.choice(useAgentList)}
                # response = requests.get(url, headers=header, timeout=(6.05, 27.05))
                response = requests.get(url, headers=header)
                response.encoding = response.apparent_encoding
                urlText = response.text
                element = html.fromstring(urlText)
                liList = element.xpath(r'//div[@id="search_nature_rg"]/ul/li')
                for li in liList:
                    bookName = li.xpath(r'./a/@title')[0]
                    bookName = patternBookName.sub('',bookName).strip() # 对图书名进行处理，去除广告
                    bookNo = str(li.xpath(r'./@id')[0])[1:]
                    bookHref = 'http:'+ li.xpath(r'./a/@href')[0]
                    price = li.xpath(r'./p[@class="price"]/span[@class="search_now_price"]/text()')
                    if not price:
                        price = li.xpath('./div[@class="ebook_buy"]/p[@class="price e_price"]/span[@class="search_now_price"]/text()')
                        if not price:
                            bookPrice = '0.0'
                            bookPrePrice = '0.0'
                        else:
                            bookPrice = price[0][1:]
                            bookPrePrice = '0.0'
                    else:
                        bookPrice = li.xpath(r'./p[@class="price"]/span[@class="search_now_price"]/text()')[0][1:]
                        prePrice = li.xpath(r'./p[@class="price"]/span[@class="search_pre_price"]/text()')
                        if not prePrice:
                            bookPrePrice = '0.0'
                        else:
                            bookPrePrice = li.xpath(r'./p[@class="price"]/span[@class="search_pre_price"]/text()')[0][1:]
                    firstSpan = li.xpath(r'./p[@class="search_book_author"]/span')[0]
                    if len(firstSpan) == 0:
                        author = ''
                    else:
                        a = firstSpan[0]
                        author = a.xpath(r'./@title')[0]
                    lastSpan = li.xpath(r'./p[@class="search_book_author"]/span')[-1]
                    if len(lastSpan) == 0:
                        press = ''
                    else:
                        press = lastSpan.xpath(r'./a/@title')[0]
                    bookStore = li.xpath(r'./p[@class="search_shangjia"]/a')
                    if not bookStore:
                        bookStore = '当当'
                    else:
                        bookStore = li.xpath(r'./p[@class="search_shangjia"]/a/@title')[0]
                    book = (bookNo, bookName, bookHref, bookPrice, bookPrePrice, author, press, bookStore, categoryNo)
                    bookList.append(book)
                if len(bookList) > 0:
                    # 写入csv
                    FileOperation.writeToCSV(r'./DangDang/Books/{0}.csv'.format(categoryNo), header=csvHeader, List=bookList, operator='a+')
                    # 插入到数据库中
                    BookDBOperator.insertDataListToDB('book', bookList)
            except Exception:
                print('Category{0}-Page:{1}-Exception:{2}'.format(categoryNo, startPage-1, traceback.format_exc()))
            finally:
                # 抓取下一页的数据
                addStr = 'pg' + str(startPage) + '-'
                if pattern.search(url):
                    url = pattern.sub(addStr, url, 1)
                else:
                    url = StringOperation.insertStr(url, 29, addStr)
                time.sleep(GetRandomTime.getFloatTime(min=1, max=3))


