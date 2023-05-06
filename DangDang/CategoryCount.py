import time
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
import requests
from lxml import html
import csv 
import re
import math
from multiprocessing import Pool
from CustomTool import GetRandomTime
from CustomTool import FileOperation

# 抓取某个图书分类下的所有图书总数并获取页数
def getCategoryCount(dataList):
    categoryCountList = []
    for data in dataList:
        categoryNo = data[1]
        url = data[2]
        response = requests.get(url)
        urltext = response.text
        element = html.fromstring(urltext)
        total = int(element.xpath(r'//span[@class="sp total"]/em[@class="b"]/text()')[0])
        totalPage = math.ceil(total/60)
        print('category {0} has a total of {1} data, {2} pages of data'.format(categoryNo, total, totalPage))
        categoryCountList.append([categoryNo, url, total, totalPage])
        time.sleep(GetRandomTime.getFloatTime(min=1, max=2))
    return categoryCountList

if __name__ == "__main__":
    pattern = re.compile(r'(category.dangdang.com+)') 
    dataList = FileOperation.readCSV(r'./DangDang/Category.csv')
    dataList = [item for item in dataList if pattern.search(item[2])] # 正则匹配筛选合适的分类
    categoryCountList = []

    index = 0
    dataDivide = []
    divide = len(dataList) // 8
    remainder = len(dataList) % 8
    for i in range(1, 9): # 对数据进行分组
            start = index
            if(index == 0):
                end = index + i * divide + remainder
            else:
                end = index + divide
            index = end
            data = [item for item in dataList[start: end]]
            dataDivide.append(data)

    p = Pool(8) # 多线程分批抓取
    with p:
        result = p.map(getCategoryCount, dataDivide)
    for item in result:
        categoryCountList.extend(item)
    categoryCountHeader = ['categoryNo', 'categoryHref', 'total', 'totalPage']
    FileOperation.writeToCSV(r'./DangDang/CategoryCount.csv',header=categoryCountHeader, List = categoryCountList)