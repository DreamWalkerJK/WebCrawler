import time
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
import requests
from lxml import html
import re
import math
from multiprocessing import Pool
from CustomTool import GetRandomTime,FileOperation,DataOperation
from DangDang import BookDBOperator

# 抓取某个图书分类下的所有图书总数并获取页数
def getCategoryCount(dataList):
    categoryCountList = []
    for data in dataList:
        categoryNo = data[0]
        url = data[2]
        response = requests.get(url)
        urltext = response.text
        element = html.fromstring(urltext)
        total = int(element.xpath(r'//span[@class="sp total"]/em[@class="b"]/text()')[0])
        totalPage = math.ceil(total/60)
        print('category {0} has a total of {1} data, {2} pages of data'.format(categoryNo, total, totalPage))
        categoryCountList.append([categoryNo, url, total, totalPage])
        time.sleep(GetRandomTime.getFloatTime(min=2, max=2.5))
    return categoryCountList

# 获取处理好的可用分类
def getUsefulCategoryList():
    pattern = re.compile(r'(category.dangdang.com+)') 
    dataList = FileOperation.readCSV(r'./DangDang/Category.csv')
    if len(dataList) == 0:
        dataList = BookDBOperator.getDataList('Category')
    dataList = [item for item in dataList if pattern.search(item[2])] # 正则匹配筛选合适的分类
    return dataList

# 将分类统计写入到CSV文件中
def writeCategoryCountToCSV(categoryCountList):
    categoryCountHeader = ['categoryNo', 'categoryHref', 'total', 'totalPage']
    FileOperation.writeToCSV(r'./DangDang/CategoryCount.csv',header=categoryCountHeader, List = categoryCountList, operator='a+')


        
            
        
        