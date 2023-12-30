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
# year_list=[2016,2017,2018,2019,2020,2021,2022]
#doc_path = r"C:\Users\Xujingran\Desktop\test.docx"

# # 期限结构
# # 调取数据 —— 期限结构部分
# # 豆粕期限结构
# use_sheet_name = "M"
# dfm = pd.read_excel(filepath, sheet_name=use_sheet_name)
# dfm.index = dfm.iloc[:, 0]
# dfm.index.name = None
# dfm = dfm.iloc[:, 1:]
# # 菜粕期限结构
# use_sheet_name = "RM"
# dfrm = pd.read_excel(filepath, sheet_name=use_sheet_name)
# dfrm.index = dfrm.iloc[:, 0]
# dfrm.index.name = None
# dfrm = dfrm.iloc[:, 1:]
# # 豆油期限结构
# use_sheet_name = "Y"
# dfy = pd.read_excel(filepath, sheet_name=use_sheet_name)
# dfy.index = dfy.iloc[:, 0]
# dfy.index.name = None
# dfy = dfy.iloc[:, 1:]
# # 棕榈油期限结构
# use_sheet_name = "P"
# dfp = pd.read_excel(filepath, sheet_name=use_sheet_name)
# dfp.index = dfp.iloc[:, 0]
# dfp.index.name = None
# dfp = dfp.iloc[:, 1:]
# # 菜籽油期限结构
# use_sheet_name = "OI"
# dfoi = pd.read_excel(filepath, sheet_name=use_sheet_name)
# dfoi.index = dfoi.iloc[:, 0]
# dfoi.index.name = None
# dfoi = dfoi.iloc[:, 1:]

# 期限结构的函数
# 月差的期限结构 版本2 适用所有油脂板块品种
def term(end, table):
    """
    inputs:
    =======
    end = 今天的日期
    table = 单品种的月交割Close

    output：
    =======
    table
    """
    str_date = end.strftime('%Y-%m-%d %H:%M:%S')

    # 提取月份部分
    month = str_date[5:7]

    for i in range(len(table.columns) - 1):
        if float(table.columns[i][:-5][-2:]) <= float(month) and float(table.columns[i + 1][:-5][-2:]) > float(month):
            table = table.iloc[:, i:].join(table.iloc[:, :i])
            new_name = [s[:-5][-2:] for s in list(table.columns)]
            table2 = table.copy()
            table2.columns = new_name
        elif i == (len(table.columns) - 2):
            if float(table.columns[i + 1][:-5][-2:]) == float(month):
                table = table.iloc[:, i + 1:].join(table.iloc[:, :i + 1])
                new_name = [s[:-5][-2:] for s in list(table.columns)]
                table2 = table.copy()
                table2.columns = new_name
            else:
                new_name = [s[:-5][-2:] for s in list(table.columns)]
                table2 = table.copy()
                table2.columns = new_name

    return table2

# 期限结构表
#table1 = term(end,dfm)
#print(table1)
