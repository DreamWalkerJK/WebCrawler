import os
import shutil
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import FileOperation

# 合并两个文件夹的图书
def MergeDir(bookPath1, bookPath2, newPath):
    bookDir1 = os.listdir(bookPath1) # 读取文件名
    bookDir2 = os.listdir(bookPath2)

    bookSet = set.union(set(bookDir1), set(bookDir2)) # 获取两个文件夹中文件名的并集

    bookDict1 = {}
    bookDict2 = {}
    for file in bookDir1:
        bookDict1[file] = os.path.getsize(r"{0}\{1}".format(bookPath1, file)) # 获取文件大小并加入字典中
    for file in bookDir2:
        bookDict2[file] = os.path.getsize(r"{0}\{1}".format(bookPath2, file))

    FileOperation.makeDir(newPath)
    for item in bookSet: # 合并筛选文件
        if item in bookDict1.keys() and item in bookDict2.keys():
            if bookDict1[item] > bookDict2[item]:
                filePath = "{0}\{1}".format(bookPath1, item)
            else:
                filePath = "{0}\{1}".format(bookPath2, item)
        elif item in bookDict1.keys() and item not in bookDict2.keys():
            filePath = "{0}\{1}".format(bookPath1, item)
        else:
            filePath = "{0}\{1}".format(bookPath2, item)
        fileNewPath = "{0}\{1}".format(newPath, item)
        shutil.copyfile(filePath, fileNewPath)

# 字典转列表
def dictToList(dict):
    retList = []
    for key in dict.keys():
        item = [dict[key], key]
        retList.append(item)
    return retList

# 合并所有分类的图书CSV到一个CSV文件中
def MergeBooks(path, newBookCSV, pressCSV):
    header = ['bookName','bookNo','bookHref','bookPrice','bookPrePrice','author','press','CategoryNo']
    pressHeader = ['pressNo', 'pressName']

    bookDir = os.listdir(path)
    pressDict = {}
    pressNo = 1
    for item in bookDir:
        bookPath = "{0}\{1}".format(path, item)
        bookContentList = FileOperation.readCSV(bookPath)
        for content in bookContentList:
            if len(content[-1]) > 0:
                if content[-1] not in pressDict.keys(): # 对出版社进行处理
                    pressDict[content[-1]] = 'P{0}'.format(pressNo)
                    pressNo += 1
                content[-1] = pressDict[content[-1]]
            content.append(item[:-4]) # 新增图书分类列
        FileOperation.writeToCSV(newBookCSV, header=header, List=bookContentList, operator='a+')
    pressList = dictToList(pressDict)
    FileOperation.writeToCSV(pressCSV, header=pressHeader, List=pressList, operator='w')
        

bookPath1 = "D:\Desktop\Book1"
bookPath2 = "D:\Desktop\Book2"
newPath = "D:\Desktop\Books"
newBookCSV = "./DangDang/AllBooks.csv"
pressCSV = "./DangDang/Press.csv"
# MergeDir(bookPath1, bookPath2, newPath) # 合并两个文件夹中的分类书籍
MergeBooks(newPath, newBookCSV, pressCSV)

