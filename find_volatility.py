# Author: R
# Date: 2023-12-24

# 最初版 指定合约
# v2 更新波动率的算法 均值设置为0 $$$$ 待更新
def get_hv2(sym, y1, end, EX, window):
    # sym,y1,end,EX,w
    """
    inputs:
    =======
    sym = M2311 字符串
    y1 = 比end提前一年的时间 1 = 一年时间，2 = 两年时间
    w：时间窗口
    EX = 交易所 字符串

    output:
    =======

    """
    # date_str = '2023-08-25'
    date_end = datetime.strptime(end, '%Y-%m-%d')
    start = date_end - timedelta(days=365 * y1)
    # print(start)
    contract = str(sym + EX)
    # print(contract)
    #error, table = w.wsd(contract, "close,trade_hiscode", start, end, "Fill=Previous", usedf=True)
    print(table)

    table['LN'] = 0.0  # 设置的时候一定要设置成浮点
    table['SD'] = 0.0
    table = table.fillna(method='ffill')

    # 核心代码
    pd.set_option('display.precision', 4)
    for i in range(len(table) - 1):
        a = round(np.log(table.iloc[i + 1][0] / table.iloc[i][0]), 8)
        table.at[table.index[i + 1], "LN"] = a
        if table.iloc[i + 1][1] != table.iloc[i][1]:
            print(table.iloc[i + 1][1])
            table.at[table.index[i + 1], "LN"] = 0.0  # 用at的方式才能赋值

    # window_size = 20
    # table["SD"] = table["LN"].rolling(window=window).std()*np.sqrt(245)
    table["SD"] = table["LN"].rolling(window=window).apply(mean0_std_dev) * np.sqrt(245)

    # 画图看看
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(table.index, table.SD)
    ax.set_title(str(sym))

    return table