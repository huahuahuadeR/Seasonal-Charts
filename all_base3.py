# Author: R
# Date: 2023-12-25

import pandas as pd
import numpy as np

# 改版6 添加未来时间的长度 添加均值
def all_base3(end, table, n0, n, want_list, year_list):
    """
    input:
    ======
    n0 = 未来时间的长度
    end = 最新数据的日期
    table =
    n = 向后需要的日期
    want_list = 基差需要的是一列数
    year_list = 指定要几年的数据 # 不要包含当年的年份

    output:
    ======
    table / plot
    """

    total_index = table.index  # 获得全部的时间
    # n0 = 20
    my_list = list(range(-n, n0))
    my_list = list(reversed(my_list))
    final_table = pd.DataFrame()

    # 将list添加到dataframe的第一列
    final_table.insert(0, 'Date', my_list)
    name_list = ["Date", want_list[0]]

    for code in want_list:
        # 获取当年的数据
        first_want_loc = total_index[0:n + 1]
        first_year_start = first_want_loc[0]
        first_year_end = first_want_loc[-1]

        # 获取对应同期时间的数据
        first_want = table.loc[first_year_start:first_year_end, code]  # 换成dataframe
        first_want.reset_index(drop=True, inplace=True)  # 把时间去掉
        first_want.columns = [code]

        df_nan = pd.DataFrame({code: [np.nan] * (n0 - 1)})  # 使用同样的列名

        # 将df_nan与df进行合并
        first_want2 = pd.concat([df_nan, first_want], axis=0, ignore_index=True)
        # 删除第一列
        first_want2.drop(first_want2.columns[0], axis=1, inplace=True)
        # 将剩余的一列重命名为code
        first_want2.rename(columns={0: code}, inplace=True)
        # 将今年的添加到final表的后面
        final_table = pd.concat([final_table.reset_index(drop=True), first_want2.reset_index(drop=True)], axis=1)

        for year in year_list:  # 假设是五年，就找五年同期的一个最大和最小值
            column_use = code  # 本身是字符串
            new_end = end.replace(year=year)  # 替换年份
            year_days = table[table.index.year == year][column_use]  # year本身是年

            days_diff = year_days.index - new_end
            seconds_list = [days.total_seconds() for days in days_diff]

            # 找到距离0秒最近的数的位置
            nearest_index = min(range(len(seconds_list)), key=lambda i: abs(seconds_list[i]))
            get_date = year_days.index[nearest_index]  # 得到去年中间的时间点

            # 日期在全序列中的位置 得到数字
            find_local = list(table.index).index(get_date)
            want_loc = total_index[find_local - n0:find_local + n]
            year_start = want_loc[0]
            year_end = want_loc[-1]

            # 获取对应同期时间的数据
            final_want = table.loc[year_start:year_end, code].to_frame()  # 换成dataframe
            final_want.reset_index(drop=True, inplace=True)  # 把时间去掉

            # 与最终表链接
            final_table = pd.concat([final_table, final_want], axis=1, ignore_index=True)
            name_list.append(code + " " + str(year))

        final_table.columns = name_list
        # 取后三列的买一行
        last_row = final_table.iloc[:, -3:].mean(axis=1).round(2)
        # 添加到新的一列命名为3y
        final_table["AVG"] = last_row

    return final_table