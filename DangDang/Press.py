import os
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import FileOperation

# 字典转列表
def dictToList(dict):
    retList = []
    for key in dict.keys():
        item = [dict[key], key]
        retList.append(item)
    return retList

# 从Books文件夹中各个分类图书csv，抓取出版社并保存到csv文件中
def getPressList(bookDir):
    bookFiles = os.listdir(bookDir)
    pressDict = {}
    pressNo = 1
    for file in bookFiles:
        bookPath = "{0}\{1}".format(bookDir, file)
        bookContentList = FileOperation.readCSV(bookPath)
        for book in bookContentList:
            if len(book[-1]) > 0 and book[-1] not in pressDict.keys():
                pressDict[book[-1]] = "P{0}".format(pressNo)
                pressNo += 1
    pressList = dictToList(pressDict)
    pressList = sorted(pressList, key = lambda a:int(a[0][1:]), reverse=False) # 按照PressNo排序
    return pressList

pressHeader = ['pressNo', 'pressName']
pressList = getPressList("./DangDang/Books")
FileOperation.writeToCSV("./DangDang/Press.csv", header=pressHeader, List=pressList, operator='w')