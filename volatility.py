# Author: R
# Date: 2023-12-28

import numpy as np

# 自己定义一个求标准差的函数
def mean0_std_dev(numbers):
    if len(numbers) < 2:
        return 0

    # 计算平均值
    #mean = sum(numbers) / len(numbers)
    mean = 0

    # 计算每个数字与平均值的差的平方和
    sum_of_squares = sum((x - mean) ** 2 for x in numbers)

    # 计算方差
    variance = sum_of_squares / len(numbers)

    # 计算标准差
    std_dev = np.sqrt(variance)

    return std_dev