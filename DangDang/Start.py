import sys
import numpy
sys.path.append(r'D:\Documents\Code\WebCrawler')
from DangDang import BookDBOperator,Category,CategoryCount,Book
from CustomTool import DataOperation,FileOperation
from multiprocessing import Pool

# 第一步 先抓取分类，写入CSV或者数据库都可
# BookDBOperator.createDataBaseAndTable()
# categoryList = Category.getCategoryList()
# Category.writeCategoryList(categoryList, isWriteToDB=0);
# Category.writeCategoryList(categoryList, isWriteToDB=1); # 写入到数据库，如果不需要就注释掉
if __name__ == "__main__":
    # 第二步 统计可用的分类并写入新的文件
    # categoryCountList = []
    # usefulCategoryList = CategoryCount.getUsefulCategoryList()
    # dataDivide = DataOperation.divideDataList(usefulCategoryList, 8)
    # p = Pool(8) # 多线程分批抓取
    # with p:
    #     result = p.map(CategoryCount.getCategoryCount, dataDivide)
    # for item in result:
    #     categoryCountList.extend(item)
    # CategoryCount.writeCategoryCountToCSV(categoryCountList)

    # 第三步抓取图书
    FileOperation.makeDir(r'./DangDang/Books')
    categoryCountList = FileOperation.readCSV(r'./DangDang/CategoryCount.csv')
    numpy.random.shuffle(categoryCountList) # 随机打乱次序
    dataDivide = DataOperation.divideDataList(categoryCountList, 8) # 将数据分成8份
    for data in dataDivide:
        data = sorted(data, key = lambda a:int(a[2]), reverse=False) # 每份数据按照页数排序
    with Pool(processes=8) as p:
        p.map(Book.getBook, dataDivide) 
