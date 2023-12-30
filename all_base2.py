# Author: R
# Date: 2023-12-18

# 导入需要的包
from datetime import datetime
import pandas as pd
import numpy as np

# 基础变量 初始设置
# today = "2023-12-15"
# end = datetime.strptime(today, '%Y-%m-%d')
# filepath = r"C:\Users\Xujingran\Desktop\季节性图表\三大油价差数据.xlsx"
# year_list = [2016,2017,2018,2019,2020,2021,2022]
#doc_path = r"C:\Users\Xujingran\Desktop\test.docx"

# 调取数据 —— 基差部分
# use_sheet_name = "基差"
# df2 = pd.read_excel(filepath, sheet_name=use_sheet_name)
# # 价差表格处理
# df2.index = df2.iloc[:, 0]
# df2.index.name = None
# df2 = df2.iloc[:, 1:]
#

# df2
# print(df2)
# 改版5 添加未来时间的长度
def all_base2(end, table, n0, n, want_list, year_list):
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

    return final_table

#b1_table = all_base2(end = end, table = df2, n0 = 20, n = 40, want_list = ["M01"], year_list = year_list)
#print(b1_table)

# series = QLineSeries()
# for i in range(len(b1_table)):
#     date = b1_table.loc[i, 'date']
#     value = b1_table.loc[i, 'M01']
#     series.append(date, value)


