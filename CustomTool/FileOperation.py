import csv 
import os.path

# 写入csv保存
def writeToCSV(path, header, List, operator = 'w'):
    isHeaderWrite = os.path.isfile(path)
    with open(path, operator, encoding='utf-8-sig', newline='')as f:
        csv_writer = csv.writer(f)
        if isHeaderWrite == False and len(header) > 0:
            csv_writer.writerow(header)
        csv_writer.writerows(List)


# 读取csv返回列表
def  readCSV(path, startIndex = 1, endIndex = -1):
    with open(path, 'r', encoding='utf-8-sig')as f:
        csv_reader = csv.reader(f)
        dataList = list(csv_reader)
    return dataList[startIndex:]

# 写入txt文件
def writeToTxt(path, contentList, operator = 'w'):
    with open(path, operator, encoding='utf-8-sig')as f:
        for content in contentList:
            f.writelines(content + '\n')


# 创建目录，先判断是否存在该目录
def makeDir(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
