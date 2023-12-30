# Author: R
# Date: 2023-12-25

# 价差波动率函数
# 价差与对应的三个油的波动率
# 改版2 三大油价差图
import pandas as pd
import numpy as np
import math
from volatility import mean0_std_dev

def spread_vol(end, table, n, n0, want_list, year_list):
    """
    input:
    ======
    end = 最新数据的日期
    table =
    n = 向后需要的日期
    want_list = 需要的列名 比如豆粽11月，看的就是豆粽11月的价差
    year_list = 指定要几年的数据 # 不要包含当年的年份

    output:
    ======
    table / plot
    """

    total_index = table.index  # 获得全部的时间
    #print(table.index)

    my_list = list(range(-n, n0))
    my_list = list(reversed(my_list))
    final_table = pd.DataFrame()

    # 将list添加到dataframe的第一列
    final_table.insert(0, 'Date', my_list)

    for code in want_list:
        # 获取当年的数据
        first_want_loc = total_index[0:n + 1]
        # print(want_loc)
        first_year_start = first_want_loc[0]
        first_year_end = first_want_loc[-1]

        # 获取对应同期时间的数据
        first_want = table.loc[first_year_start:first_year_end, code]  # 换成dataframe
        first_want.reset_index(drop=True, inplace=True)  # 把时间去掉
        first_want.columns = [code]
        # print(first_want.columns)

        df_nan = pd.DataFrame({code: [np.nan] * (n0-1)})  # 使用同样的列名
        # print(df_nan)

        # 将df_nan与df进行合并
        first_want2 = pd.concat([df_nan, first_want], axis=0, ignore_index=True)
        # 删除第一列
        first_want2.drop(first_want2.columns[0], axis=1, inplace=True)
        # 将剩余的一列重命名为code
        first_want2.rename(columns={0: code}, inplace=True)
        # print(first_want2)
        # 将今年的添加到final表的后面
        final_table = pd.concat([final_table.reset_index(drop=True), first_want2.reset_index(drop=True)], axis=1)
        # print(final_table)

        local_table = pd.DataFrame()

        for year in year_list:  # 假设是五年，就找五年同期的一个最大和最小值
            column_use = code  # 本身是字符串
            #print(year)
            #print(type(end))
            new_end = end.replace(year=year)  # 替换年份
            year_days = table[table.index.year == year][column_use]  # year本身是年

            days_diff = year_days.index - new_end
            # print(days_diff)

            seconds_list = [days.total_seconds() for days in days_diff]
            # 找到距离0秒最近的数的位置
            nearest_index = min(range(len(seconds_list)), key=lambda i: abs(seconds_list[i]))
            get_date = year_days.index[nearest_index]  # 得到去年中间的时间点
            #print(get_date)
            # 日期在全序列中的位置 得到数字
            find_local = list(table.index).index(get_date)
            #print(find_local)

            want_loc = total_index[find_local - n0:find_local + n]
            #print(want_loc)
            year_start = want_loc[0]
            year_end = want_loc[-1]

            # 获取对应同期时间的数据
            final_want = table.loc[year_start:year_end, code].to_frame()  # 换成dataframe
            final_want.reset_index(drop=True, inplace=True)  # 把时间去掉

            # 与最终表链接
            local_table = pd.concat([local_table, final_want], axis=1, ignore_index=True)
            # print(local_table)

        # 得到这个9月豆粽的同期历史数据以后 找到每一行的最大和最小值 将这部分添加到final表上
        final_table[code + ' MIN'] = local_table.apply(lambda x: x.min(), axis=1)
        final_table[code + ' MAX'] = local_table.apply(lambda x: x.max(), axis=1)
        final_table[code + ' Median'] = local_table.apply(lambda x: x.median(), axis=1)

    return final_table
