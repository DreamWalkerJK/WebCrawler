import random 

# 返回指定范围内的整数，默认在1-3范围内
def getIntTime(min = 1, max =3):
    return random.random(min, max)

# 返回指定范围内的随机数，默认在1-3范围内取小数点后2位
def getFloatTime(min = 1, max = 3, limit = 2):
    return round(random.uniform(min, max), limit)