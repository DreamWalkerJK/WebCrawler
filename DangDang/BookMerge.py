import os
import shutil
import sys
sys.path.append(r'D:\Documents\Code\WebCrawler')
from CustomTool import FileOperation

# 合并两个文件夹的图书
def mergeDir(bookPath1, bookPath2, newPath):
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

# 求交集，方便后续继续抓取不同分类数据
def intersectionOfBooks():
    categoryCountPath = 'D:\Desktop\CategoryCount.csv'
    categoryCountList = FileOperation.readCSV(categoryCountPath)
    compareSet = set([item[0] for item in categoryCountList])
    compareSet.intersection
    bookFileList = os.listdir('D:\Desktop\Books')
    bookSet = set([item.split('.')[0] for item in bookFileList])
    result = compareSet - bookSet

    newCategoryCountList = []
    for item in categoryCountList:
        if item[0] in result:
            newCategoryCountList.append(item)

    categoryCountHeader = ['categoryNo', 'categoryHref', 'total', 'totalPage']
    FileOperation.writeToCSV(categoryCountPath, header=categoryCountHeader, List=newCategoryCountList)

# 扫描目录获取图书的总和
def getBooksTotalNum(booksDir):
    bookFileList = os.listdir(booksDir)
    total = 0
    for file in bookFileList:
        bookPath = "{0}\{1}".format(newPath, file)
        bookList = FileOperation.readCSV(bookPath)
        total += len(bookList)
    return total

bookPath1 = "D:\Desktop\Book1"
bookPath2 = "D:\Desktop\Book2"
newPath = "D:\Desktop\Books"
# mergeDir(bookPath1, bookPath2, newPath) # 合并两个文件夹中的分类书籍

# intersectionOfBooks()

total = getBooksTotalNum(newPath)
print("total : {0}".format(total))


