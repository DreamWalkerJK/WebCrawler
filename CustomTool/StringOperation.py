# 字符串指定位置新增字符串
def insertStr(str, pos, addStr):
    strList = list(str)
    strList.insert(pos, addStr)
    strOut = ''.join(strList)
    return strOut