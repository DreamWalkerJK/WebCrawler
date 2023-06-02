import math

# 对列表进行分组
def divideDataList(dataList, groupNum):
    if groupNum <= 1:
        return dataList
    index = 0
    dataDivide = []
    divide = len(dataList) // groupNum
    ceilDivide = math.ceil(len(dataList) / groupNum)
    remainder = len(dataList) % groupNum
    flag = 0 if remainder == 0 else 1
    for i in range(1, groupNum + 1): # 对数据进行分组
        start = index
        if(flag <= remainder):
            end = index + ceilDivide
        else:
            end = index + divide
        index = end
        data = [item for item in dataList[start: end]]
        dataDivide.append(data)
        flag += 1
    return dataDivide