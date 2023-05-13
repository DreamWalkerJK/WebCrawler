# 对列表进行分组
def divideDataList(dataList, groupNum):
    if groupNum <= 1:
        return dataList
    index = 0
    dataDivide = []
    divide = len(dataList) // groupNum
    remainder = len(dataList) % groupNum
    for i in range(1, groupNum + 1): # 对数据进行分组
        start = index
        if(index == 0):
            end = index + i * divide + remainder
        else:
            end = index + divide
        index = end
        data = [item for item in dataList[start: end]]
        dataDivide.append(data)
    return dataDivide