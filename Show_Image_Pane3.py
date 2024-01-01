# Author: R
# Date: 2023-12-24


from PyQt5.Qt import *
#from resource.show_image2 import Ui_Form
from resource.show_image3 import Ui_MainWindow
#from PyQt5.QtChart import QChartView, QChart, QLineSeries, QValueAxis
from matplotlib.backends.backend_qt5agg import FigureCanvas
#from matplotlib import FigureCanvas
#, NavigationToolbar2QT as NavigationToolbar
import math
import matplotlib as mpl
import matplotlib.pylab as plt
#import numpy as np
import pandas as pd
from datetime import datetime
import re

from all_base2 import all_base2
from all_base3 import all_base3
from term_stracture import term
from spread import spread
from volatility import mean0_std_dev
#from spread_vol import spread_vol
import seaborn as sns

from WindPy import *

class ShowImagePane3(QMainWindow,Ui_MainWindow):

    #to_show_image_pane_singal = pyqtSignal()  # 为了链接其它界面 定义一个新的信号

    def __init__(self,parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) # 调用了父类 QWidget里面的方法
        self.setAttribute(Qt.WA_StyledBackground,True) # 继承背景 否则没有背景
        self.setupUi(self)

        # #self.today = "2023-12-22"
        # self.today = self.date.currentText()
        # self.end = datetime.strptime(self.today, '%Y-%m-%d')
        self.year_list = [2016, 2017, 2018, 2019, 2020, 2021, 2022] # 将self year list 放到表格后面 @

        # Seasonal
        self.setWindowTitle("Seasonal Charts")

        # 设置画布
        self.fig = plt.figure()
        self.figCanvas = FigureCanvas(self.fig)
        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)

        # 子图提前
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)

        # # 创建工具栏
        # naviToolbar = NavigationToolbar(figCanvas, self)
        # actList = naviToolbar.actions()
        # count = len(actList)
        # lastAction = actList[count - 1]
        #
        # labCurAxes = QLabel("当前图")
        # naviToolbar.inserWidget(lastAction,labCurAxes)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(self.toolBox)
        splitter.addWidget(self.figCanvas)
        # 设置QSplitter为主窗口的中心部件
        self.setCentralWidget(splitter)

        # 表格的初始设置
        self.df2 = pd.DataFrame() # df2 == 基差表格
        self.df_close2 = pd.DataFrame()
        self.dfm = pd.DataFrame()
        self.dfrm = pd.DataFrame()
        self.dfy = pd.DataFrame()
        self.dfoi = pd.DataFrame()
        self.dfp = pd.DataFrame()
        self.dfc = pd.DataFrame()
        self.dfcs = pd.DataFrame()

    # 补充函数

    # 第二版 链接API的版本
    def read_table(self):
        w.start()

        # 得到时间
        use_date = self.date.text()
        self.today = use_date
        print(self.today)
        pattern = r"\d{4}-\d{2}-\d{2}"
        last_element = self.year_list[-1]

        if re.match(pattern, self.today) and int(last_element) < int(use_date[:4]):
            print("日期格式正确")
            self.end = datetime.strptime(self.today, '%Y-%m-%d')
        else:
            print("日期格式错误")
            self.end = datetime.now().date()
            print(datetime.now().date())

        # 产生list
        # 提取年份并转换为int类型
        year = int(self.end.year)

        # 生成包含四个元素的一列数的列表
        year_list = [year - i - 1 for i in range(6)]
        print(type(year_list))
        self.year_list = list(reversed(year_list))

        print(self.year_list)  # 输出：[2020, 2021, 2022, 2023]

        # 豆粕数据
        m_list = ["M01M.DCE", "M03M.DCE", "M05M.DCE", "M07M.DCE", "M08M.DCE", "M09M.DCE", "M11M.DCE", "M12M.DCE", "W00058SPT.NM"]
        error, m_df = w.wsd(m_list, "close", "2016-01-01", self.end, "Sort=D", "Fill=Previous", usedf=True)
        m_df.index = pd.to_datetime(m_df.index)
        print("m ok")

        # 菜粕数据
        rm_list = ["RM01M.CZC", "RM03M.CZC", "RM05M.CZC", "RM07M.CZC", "RM08M.CZC", "RM09M.CZC", "RM11M.CZC",
                  "W00216SPT.NM"]
        error, rm_df = w.wsd(rm_list, "close", "2016-01-01", self.end, "Sort=D", "Fill=Previous", usedf=True)
        rm_df.index = pd.to_datetime(rm_df.index)
        print("rm ok")

        # 豆油数据
        y_list = ["Y01M.DCE", "Y03M.DCE", "Y05M.DCE", "Y07M.DCE", "Y08M.DCE", "Y09M.DCE", "Y11M.DCE", "Y12M.DCE",
                   "W00059SPT.NM"]
        error, y_df = w.wsd(y_list, "close", "2016-01-01", self.end, "Sort=D", "Fill=Previous", usedf=True)
        y_df.index = pd.to_datetime(y_df.index)
        print("y ok")

        # 棕榈油数据
        p_list = ["P01M.DCE", "P02M.DCE", "P03M.DCE", "P04M.DCE", "P05M.DCE",
                  "P06M.DCE", "P07M.DCE", "P08M.DCE", "P09M.DCE", "P10M.DCE", "P11M.DCE", "P12M.DCE",
                  "W00060SPT.NM"]
        error, p_df = w.wsd(p_list, "close", "2016-01-01", self.end, "Sort=D", "Fill=Previous", usedf=True)
        p_df.index = pd.to_datetime(p_df.index)
        print("p ok")

        # 菜籽油数据
        oi_list = ["OI01M.CZC", "OI03M.CZC", "OI05M.CZC", "OI07M.CZC", "OI09M.CZC", "OI11M.CZC",
                  "W00064SPT.NM"]
        error, oi_df = w.wsd(oi_list, "close", "2016-01-01", self.end, "Sort=D", "Fill=Previous", usedf=True)
        oi_df.index = pd.to_datetime(oi_df.index)
        print("oi ok")

        # 玉米数据
        c_list = ["C01M.DCE", "C03M.DCE", "C05M.DCE", "C07M.DCE", "C09M.DCE", "C11M.DCE",
                   "W00142SPT.NM"]
        error, c_df = w.wsd(c_list, "close", "2016-01-01", self.end, "Sort=D", "Fill=Previous", usedf=True)
        c_df.index = pd.to_datetime(c_df.index)
        print("c ok")

        # 淀粉数据
        cs_list = ["CS01M.DCE", "CS03M.DCE", "CS05M.DCE", "CS07M.DCE", "CS09M.DCE", "CS11M.DCE",
                   "W00062SPT.NM"]
        error, cs_df = w.wsd(cs_list, "close", "2016-01-01", self.end, "Sort=D", "Fill=Previous", usedf=True)
        cs_df.index = pd.to_datetime(cs_df.index)
        print("cs ok")

        # dfx == 期限结构
        df_copy = m_df.copy()
        self.dfm = df_copy.iloc[:, :-1]
        df_copy = rm_df.copy()
        self.dfrm = df_copy.iloc[:, :-1]
        df_copy = y_df.copy()
        self.dfy = df_copy.iloc[:, :-1]
        df_copy = p_df.copy()
        self.dfp = df_copy.iloc[:, :-1]
        df_copy = oi_df.copy()
        self.dfoi = df_copy.iloc[:, :-1]
        df_copy = c_df.copy()
        self.dfc = df_copy.iloc[:, :-1]
        df_copy = cs_df.copy()
        self.dfcs = df_copy.iloc[:, :-1]

        # df_close == 收盘价
        self.df_close2 = pd.concat([self.dfm, self.dfrm, self.dfy, self.dfp, self.dfoi, self.dfc, self.dfcs], axis=1)

        # df1 == 价差表格 C-CS Y-P-OI M-RM Y/M OI/RM
        self.df1 = pd.DataFrame()
        # 将两个DataFrame的列1相减得到新的列
        self.df1["Y&P 01"] = y_df["Y01M.DCE"] - p_df["P01M.DCE"]
        self.df1["Y&P 05"] = y_df["Y05M.DCE"] - p_df["P05M.DCE"]
        self.df1["Y&P 09"] = y_df["Y09M.DCE"] - p_df["P09M.DCE"]

        self.df1["OI&Y 01"] = oi_df["OI01M.CZC"] - y_df["Y01M.DCE"]
        self.df1["OI&Y 05"] = oi_df["OI05M.CZC"] - y_df["Y05M.DCE"]
        self.df1["OI&Y 09"] = oi_df["OI09M.CZC"] - y_df["Y09M.DCE"]

        self.df1["OI&P 01"] = oi_df["OI01M.CZC"] - p_df["P01M.DCE"]
        self.df1["OI&P 05"] = oi_df["OI05M.CZC"] - p_df["P05M.DCE"]
        self.df1["OI&P 09"] = oi_df["OI09M.CZC"] - p_df["P09M.DCE"]

        self.df1["CS&C 01"] = cs_df["CS01M.DCE"] - c_df["C01M.DCE"]
        self.df1["CS&C 03"] = cs_df["CS03M.DCE"] - c_df["C03M.DCE"]
        self.df1["CS&C 05"] = cs_df["CS05M.DCE"] - c_df["C05M.DCE"]
        self.df1["CS&C 07"] = cs_df["CS07M.DCE"] - c_df["C07M.DCE"]
        self.df1["CS&C 09"] = cs_df["CS09M.DCE"] - c_df["C09M.DCE"]

        self.df1["M&RM 01"] = m_df["M01M.DCE"] - rm_df["RM01M.CZC"]
        self.df1["M&RM 05"] = m_df["M05M.DCE"] - rm_df["RM05M.CZC"]
        self.df1["M&RM 09"] = m_df["M09M.DCE"] - rm_df["RM09M.CZC"]

        self.df1["Y/M 01"] = y_df["Y01M.DCE"] / m_df["M01M.DCE"]
        self.df1["Y/M 05"] = y_df["Y05M.DCE"] / m_df["M05M.DCE"]
        self.df1["Y/M 09"] = y_df["Y09M.DCE"] / m_df["M09M.DCE"]

        self.df1["OI/RM 01"] = oi_df["OI01M.CZC"] / rm_df["RM01M.CZC"]
        self.df1["OI/RM 05"] = oi_df["OI05M.CZC"] / rm_df["RM05M.CZC"]
        self.df1["OI/RM 09"] = oi_df["OI09M.CZC"] / rm_df["RM09M.CZC"]

        # df2 == 基差表格
        self.df2 = pd.DataFrame()
        for i in range(len(m_df.columns) - 1):
            use_col = m_df.columns[i]
            use_s = m_df.columns[-1]
            self.df2[use_col[:-5]] = m_df[use_s] - m_df[use_col]

        for i in range(len(rm_df.columns) - 1):
            use_col = rm_df.columns[i]
            use_s = rm_df.columns[-1]
            self.df2[use_col[:-5]] = rm_df[use_s] - rm_df[use_col]

        for i in range(len(y_df.columns) - 1):
            use_col = y_df.columns[i]
            use_s = y_df.columns[-1]
            self.df2[use_col[:-5]] = y_df[use_s] - y_df[use_col]

        for i in range(len(p_df.columns) - 1):
            use_col = p_df.columns[i]
            use_s = p_df.columns[-1]
            self.df2[use_col[:-5]] = p_df[use_s] - p_df[use_col]

        for i in range(len(oi_df.columns) - 1):
            use_col = oi_df.columns[i]
            use_s = oi_df.columns[-1]
            self.df2[use_col[:-5]] = oi_df[use_s] - oi_df[use_col]

        for i in range(len(c_df.columns) - 1):
            use_col = c_df.columns[i]
            use_s = c_df.columns[-1]
            self.df2[use_col[:-5]] = c_df[use_s] - c_df[use_col]

        for i in range(len(cs_df.columns) - 1):
            use_col = cs_df.columns[i]
            use_s = cs_df.columns[-1]
            self.df2[use_col[:-5]] = cs_df[use_s] - cs_df[use_col]

        print(self.df2)

        # df3 月差表格
        # 油脂油料部分
        self.df3 = pd.DataFrame()
        self.df3["M15"] = m_df["M01M.DCE"] - m_df["M05M.DCE"]
        self.df3["M59"] = m_df["M05M.DCE"] - m_df["M09M.DCE"]
        self.df3["M91"] = m_df["M09M.DCE"] - m_df["M01M.DCE"]

        self.df3["RM15"] = rm_df["RM01M.CZC"] - rm_df["RM05M.CZC"]
        self.df3["RM59"] = rm_df["RM05M.CZC"] - rm_df["RM09M.CZC"]
        self.df3["RM91"] = rm_df["RM09M.CZC"] - rm_df["RM01M.CZC"]

        self.df3["Y15"] = y_df["Y01M.DCE"] - y_df["Y05M.DCE"]
        self.df3["Y59"] = y_df["Y05M.DCE"] - y_df["Y09M.DCE"]
        self.df3["Y91"] = y_df["Y09M.DCE"] - y_df["Y01M.DCE"]

        self.df3["P15"] = p_df["P01M.DCE"] - p_df["P05M.DCE"]
        self.df3["P59"] = p_df["P05M.DCE"] - p_df["P09M.DCE"]
        self.df3["P91"] = p_df["P09M.DCE"] - p_df["P01M.DCE"]

        self.df3["OI15"] = oi_df["OI01M.CZC"] - oi_df["OI05M.CZC"]
        self.df3["OI59"] = oi_df["OI05M.CZC"] - oi_df["OI09M.CZC"]
        self.df3["OI91"] = oi_df["OI09M.CZC"] - oi_df["OI01M.CZC"]

        # 玉米淀粉部分
        self.df3["C15"] = c_df["C01M.DCE"] - c_df["C05M.DCE"]
        self.df3["C59"] = c_df["C05M.DCE"] - c_df["C09M.DCE"]
        self.df3["C91"] = c_df["C09M.DCE"] - c_df["C01M.DCE"]

        self.df3["CS15"] = cs_df["CS01M.DCE"] - cs_df["CS05M.DCE"]
        self.df3["CS59"] = cs_df["CS05M.DCE"] - cs_df["CS09M.DCE"]
        self.df3["CS91"] = cs_df["CS09M.DCE"] - cs_df["CS01M.DCE"]

        QMessageBox.information(self, "＼(`Δ’)／", "   (●'◡'●)   " + "t0 = " + str(self.end)[:10])

    def date_change(self):
        a = self.get_date.text()
        print(a)
        print(type(a))

    def term_code_change(self):
        print("切换代码")

    def b_axis_change(self):
        a = self.axis_box.currentText()
        print(a)
        print(type(a))

    def b_code_change(self):
        a = self.code_box.currentText()
        print(a)
        print(type(a))

    def b_n0_change(self):
        a = self.b_n0_box.currentText()
        print(a)
        print(type(a))

    def b_n_change(self):
        a = self.b_n_box.currentText()
        print(a)
        print(type(a))

    def vol_code_change(self):
        a = self.vol_code.currentText()
        print(a)
        print(type(a))

    def close_code_change(self):
        a = self.close_code.currentText()
        print(a)
        print(type(a))

    def spread_change(self):
        a = self.close_spread_box.currentText()
        print(a)
        print(type(a))
        pass

    def window_change(self):
        a = self.w_box.currentText()
        print(a)
        print(type(a))

    def get_plot(self): # 第二版 全局版

        if self.df2.empty:
            pass
        else:
            term_code = str(self.term_box.currentText())

            if term_code == "M":
                term_df = term(self.end, self.dfm)
            elif term_code == "RM":
                term_df = term(self.end, self.dfrm)
            elif term_code == "P":
                term_df = term(self.end, self.dfp)
            elif term_code == "OI":
                term_df = term(self.end, self.dfoi)
            elif term_code == "Y":
                term_df = term(self.end, self.dfy)
            elif term_code == "C":
                term_df = term(self.end, self.dfc)
            elif term_code == "CS":
                term_df = term(self.end, self.dfcs)

            use_axis = self.axis_box.currentText()

            if use_axis == "图1":
                ax1 = self.ax1
            elif use_axis == "图2":
                ax1 = self.ax2
            elif use_axis == "图3":
                ax1 = self.ax3
            elif use_axis == "图4":
                ax1 = self.ax4

            ax1.clear()

            # 画期限结构的图
            colorlist = ["#CD5555"]
            colorlist2 = sns.color_palette("Blues", 4)
            colorlist2.reverse()
            colorlist.extend(colorlist2)
            week_range = "#FFC125"
            linew = 1.2
            print("b")
            for i in range(5):
                row = term_df.iloc[i * 3]
                print(row)
                ax1.plot(row.index, row.values, color=colorlist[i], linewidth=linew, label=str(term_df.index[i * 3])[:10])
            print("c")
            # 画布基础设置
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            # ax.spines['left'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
            # 修改坐标轴颜色
            ax1.spines['bottom'].set_edgecolor('gray')
            ax1.spines['left'].set_edgecolor('gray')
            ax1.tick_params(axis='both', colors='#404040')
            ax1.grid(True, linestyle='--', color='gray', linewidth='0.3')
            # 设置图例 去掉边框
            ax1.legend(frameon=False, loc="upper right")

            # 设置标题
            ax1.set_title(term_code + " - " + "Term Structure", color="#014189", loc="left", fontsize=10, pad=15)
            self.figCanvas.draw()
            #ax1.show()
            #print("显示图像")

    # 第一版 表格版本
    def get_basis_plot(self):

        use_axis = self.axis_box.currentText()

        if use_axis == "图1":
            ax3 = self.ax1
        elif use_axis == "图2":
            ax3 = self.ax2
        elif use_axis == "图3":
            ax3 = self.ax3
        elif use_axis == "图4":
            ax3 = self.ax4

        if self.df2.empty:
            pass
        else:
            ax3.clear()

            print("1")

            # 通过接收参数 创建出表格
            b_code = [str(self.code_box.currentText())]  # 获取到合约
            n0 = int(self.b_n0_box.currentText())  # 获取到【未来】的时间长度
            n = int(self.b_n_box.currentText())  # 获取到【过去】的时间长度
            b1_table = all_base2(end=self.end, table=self.df2, n0=n0, n=n, want_list=b_code, year_list=self.year_list)
            print(b1_table)

            # 基础参数
            cofco_blue = "#013B89"
            cofco_orange = "#F7A501"
            long_range = "#FFF8DC"
            week_range = "#FFC125"
            linew = 1.2
            colorlist = ["#CD5555"]
            colorlist2 = sns.color_palette("Blues", 7)
            colorlist.extend(colorlist2)

            for i in range(len(b1_table.columns) - 1):
                ax3.plot(b1_table["Date"], b1_table[b1_table.columns[1 + i]], label=b1_table.columns[1 + i],
                         color=colorlist[i], linewidth=linew)
                print("4")
                ax3.fill_between(b1_table["Date"], b1_table[b1_table.columns[1 + i]], 0,
                                 where=(b1_table[b1_table.columns[1 + i]] < 0),
                                 color=colorlist[i], alpha=0.4)

            ax3.axvspan(b1_table["Date"][n0 - 1], b1_table["Date"][n0 - 1 + 5], facecolor=week_range, alpha=0.1)
            ax3.axvspan(b1_table["Date"][n0 - 1], b1_table["Date"][n0 - 1 + 15], facecolor=long_range, alpha=0.2)

            ax3.scatter(b1_table["Date"][n0 - 1], b1_table[b1_table.columns[1]][n0 - 1], s=60, c=colorlist[0])
            ax3.axvline(b1_table["Date"][n0 - 1], color='orange', linestyle='--', linewidth=2)

            # 画布基础设置
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.spines['left'].set_visible(False)
            ax3.spines['bottom'].set_visible(False)

            # 显示零轴
            ax3.axhline(0, color='gray', linewidth=1)

            # 修改坐标轴颜色
            ax3.spines['bottom'].set_edgecolor('gray')
            ax3.spines['left'].set_edgecolor('gray')
            plt.tick_params(axis='both', colors='#404040')

            # 设置图例 去掉边框
            ax3.legend(frameon=False, loc="upper right")

            # 设置坐标轴标签
            ax3.set_xlabel('Time Line')

            # 设置标题
            ax3.set_title(b1_table.columns[1] + " " + 'Cash Premium', color=cofco_blue, loc="left", fontsize=10, pad=15)
            self.figCanvas.draw()

    # 调取数据 独立于其它的表格
    def get_sigma(self):

        w.start()

        # # 抓取时间
        # use_date = self.date.text()
        # self.today = use_date
        # pattern = r"\d{4}-\d{2}-\d{2}"
        #
        # if re.match(pattern, self.today):
        #     print("日期格式正确")
        #     self.end = datetime.strptime(self.today, '%Y-%m-%d')
        # else:
        #     print("日期格式错误")
        #     self.end = datetime.now().date()
        #     print(datetime.now().date())

        # 得到时间
        use_date = self.date.text()
        self.today = use_date
        pattern = r"\d{4}-\d{2}-\d{2}"
        last_element = self.year_list[-1]

        if re.match(pattern, self.today) and int(last_element) < int(use_date[:4]):
            print("日期格式正确")
            self.end = datetime.strptime(self.today, '%Y-%m-%d')
        else:
            print("日期格式错误")
            self.end = datetime.now().date()
            print(datetime.now().date())

        # 产生list
        year = int(self.end.year)

        # 生成包含四个元素的一列数的列表
        year_list = [year - i - 1 for i in range(6)]
        print(type(year_list))
        self.year_list = list(reversed(year_list))

        print(self.year_list)  # 输出：[2020, 2021, 2022, 2023]

        # 获取到合约的合约
        use_code = self.vol_code.currentText()
        window = int(self.w_box.currentText())

        error, vol_table = w.wsd(use_code, "close, trade_hiscode", "2016-01-01", self.end, "Fill=Previous",
                             usedf=True)
        vol_table.index = pd.to_datetime(vol_table.index)

        # 得到结果的表格
        vol_table['LN'] = 0.0  # 设置的时候一定要设置成浮点
        vol_table['SD'] = 0.0
        vol_table = vol_table.fillna(method='ffill')

        pd.set_option('display.precision', 4)
        for i in range(len(vol_table) - 1):
            a = round(math.log(vol_table.iloc[i + 1][0] / vol_table.iloc[i][0]), 8)
            vol_table.at[vol_table.index[i + 1], "LN"] = a
            if vol_table.iloc[i + 1][1] != vol_table.iloc[i][1]:
                vol_table.at[vol_table.index[i + 1], "LN"] = 0.0  # 用at的方式才能赋值

        vol_table["SD"] = vol_table["LN"].rolling(window=window).apply(mean0_std_dev) * math.sqrt(245)
        vol_result = vol_table.drop(vol_table.columns[:3], axis=1).dropna()
        vol_result = vol_result[::-1]

        # 得到标准季节性表格
        n0 = int(self.b_n0_box.currentText())  # 获取到【未来】的时间长度
        n = int(self.b_n_box.currentText())  # 获取到【过去】的时间长度
        df_vol = all_base3(end=self.end, table=vol_result, n0=n0, n=n, want_list=['SD'], year_list=self.year_list)

        use_axis = self.axis_box.currentText()

        if use_axis == "图1":
            ax_vol = self.ax1
        elif use_axis == "图2":
            ax_vol = self.ax2
        elif use_axis == "图3":
            ax_vol = self.ax3
        elif use_axis == "图4":
            ax_vol = self.ax4

        ax_vol.clear()

        # 基础参数
        cofco_blue = "#013B89"
        cofco_orange = "#F7A501"
        long_range = "#FFF8DC"
        week_range = "#FFC125"
        linew = 1.2

        colorlist = ["#CD5555"]
        colorlist2 = sns.color_palette("Blues", 7)
        colorlist.extend(colorlist2)

        for i in range(len(df_vol.columns) - 2):
            ax_vol.plot(df_vol["Date"], df_vol[df_vol.columns[1 + i]],
                          label=df_vol.columns[1 + i], color=colorlist[i], linewidth=linew)

        ax_vol.plot(df_vol["Date"], df_vol[df_vol.columns[-1]],
                      label=df_vol.columns[-1], color="#FFE4E1", linewidth=2, alpha=0.8, linestyle='--')  # 粉色

        ax_vol.axvspan(df_vol["Date"][n0 - 1], df_vol["Date"][n0 - 1 + 5], facecolor=week_range, alpha=0.1)
        ax_vol.axvspan(df_vol["Date"][n0 - 1], df_vol["Date"][n0 - 1 + 15], facecolor=long_range, alpha=0.2)
        ax_vol.scatter(df_vol["Date"][n0 - 1], df_vol[df_vol.columns[1]][n0 - 1], s=60, c=colorlist[0])
        ax_vol.axvline(df_vol["Date"][n0 - 1], color='orange', linestyle='--', linewidth=2)
        print("3")

        # 画布基础设置
        ax_vol.spines['top'].set_visible(False)
        ax_vol.spines['right'].set_visible(False)
        ax_vol.spines['left'].set_visible(False)
        ax_vol.spines['bottom'].set_visible(False)

        print("4")

        # 修改坐标轴颜色
        ax_vol.spines['bottom'].set_edgecolor('gray')
        ax_vol.spines['left'].set_edgecolor('gray')
        ax_vol.tick_params(axis='both', colors='#404040')

        # 显示横向网格线
        ax_vol.grid(axis='y', linewidth='0.3')

        # 设置图例 去掉边框
        ax_vol.legend(frameon=False, loc="upper right")
        print("5")

        # 设置坐标轴标签
        ax_vol.set_xlabel('Time Line')

        ax_vol.set_title(use_code + " " + 'Volatility', color=cofco_blue, loc="left", fontsize=10, pad=15)
        self.figCanvas.draw()

    def get_close(self):

        if self.df2.empty:
            pass
        else:
            use_axis = self.axis_box.currentText()
            if use_axis == "图1":
                ax_close = self.ax1
            elif use_axis == "图2":
                ax_close = self.ax2
            elif use_axis == "图3":
                ax_close = self.ax3
            elif use_axis == "图4":
                ax_close = self.ax4

            ax_close.clear()
            # 得到价格的表格
            # 内置year_list
            close_code = [str(self.close_code.currentText())]  # 获取到合约
            n0 = int(self.b_n0_box.currentText())  # 获取到【未来】的时间长度
            n = int(self.b_n_box.currentText())  # 获取到【过去】的时间长度

            # df_close = all_base3(end=self.end, table=self.df_close2, n0=n0, n=n, want_list=close_code,
            #                      year_list=[2020, 2021, 2022])
            df_close = all_base3(end=self.end, table=self.df_close2, n0=n0, n=n, want_list=close_code,
                                 year_list=self.year_list)

            # 基础参数
            cofco_blue = "#013B89"
            cofco_orange = "#F7A501"
            long_range = "#FFF8DC"
            week_range = "#FFC125"
            linew = 1.2

            colorlist = ["#CD5555"]
            colorlist2 = sns.color_palette("Blues", 7)
            colorlist.extend(colorlist2)

            for i in range(len(df_close.columns) - 2):
                ax_close.plot(df_close["Date"], df_close[df_close.columns[1 + i]],
                              label=df_close.columns[1 + i], color=colorlist[i], linewidth=linew)

            ax_close.plot(df_close["Date"], df_close[df_close.columns[-1]],
                          label=df_close.columns[-1], color="#FFE4E1", linewidth=2, alpha=0.8, linestyle='--')  # 粉色

            ax_close.axvspan(df_close["Date"][n0 - 1], df_close["Date"][n0 - 1 + 5], facecolor=week_range, alpha=0.1)
            ax_close.axvspan(df_close["Date"][n0 - 1], df_close["Date"][n0 - 1 + 15], facecolor=long_range, alpha=0.2)
            ax_close.scatter(df_close["Date"][n0 - 1], df_close[df_close.columns[1]][n0 - 1], s=60, c=colorlist[0])
            ax_close.axvline(df_close["Date"][n0 - 1], color='orange', linestyle='--', linewidth=2)
            print("3")

            # 画布基础设置
            ax_close.spines['top'].set_visible(False)
            ax_close.spines['right'].set_visible(False)
            ax_close.spines['left'].set_visible(False)
            ax_close.spines['bottom'].set_visible(False)

            # 修改坐标轴颜色
            ax_close.spines['bottom'].set_edgecolor('gray')
            ax_close.spines['left'].set_edgecolor('gray')
            ax_close.tick_params(axis='both', colors='#404040')

            # 显示横向网格线
            ax_close.grid(axis='y', linewidth='0.3')

            # 设置图例 去掉边框
            ax_close.legend(frameon=False, loc="upper right")
            print("5")

            # 设置坐标轴标签
            ax_close.set_xlabel('Time Line')

            # 将横坐标轴标签写到坐标轴右边
            use_name = str(self.close_code.currentText())

            ax_close.set_title(df_close.columns[1] + " " + 'Close', color=cofco_blue, loc="left", fontsize=10, pad=15)
            self.figCanvas.draw()

    # 画价差季节性的图
    # 更新到 05合约【三大油价差】【玉米淀粉利润】【两粕价差】【豆油粕比】【菜籽油粕比】
    def close_spread(self):

        if self.df2.empty:
            pass
        else:
            use_axis = self.axis_box.currentText()
            if use_axis == "图1":
                ax_spread = self.ax1
                print("get")
            elif use_axis == "图2":
                ax_spread = self.ax2
            elif use_axis == "图3":
                ax_spread = self.ax3
            elif use_axis == "图4":
                ax_spread = self.ax4

            ax_spread.clear()

            close_spread_list = self.close_spread_box.currentText()
            if close_spread_list == "Y&P&OI 05":
                want_list = ["Y&P 05", "OI&Y 05", "OI&P 05"]
            elif close_spread_list == "Y&P&OI 01":
                want_list = ["Y&P 01", "OI&Y 01", "OI&P 01"]
            elif close_spread_list == "Y&P&OI 09":
                want_list = ["Y&P 09", "OI&Y 09", "OI&P 09"]
            else:
                want_list = [str(self.close_spread_box.currentText())]  # 获取到合约
            # elif close_spread_list == "CS&C-05":
            #     want_list = ["CS&C 05"]
            # elif close_spread_list == "M&RM-05":
            #     want_list = ["M&RM 05"]
            # elif close_spread_list == "Y/M-05":
            #     want_list = ["Y/M 05"]
            # elif close_spread_list == "OI&RM-05":
            #     want_list = ["OI/RM 05"]

            #want_list = [str(self.close_spread_box.currentText())]  # 获取到合约

            print(want_list)
            print(self.df1)

            # print(self.df1["OI/RM 05"])
            # print(self.df1["Y/M 05"])

            n0 = int(self.b_n0_box.currentText())  # 获取到【未来】的时间长度
            n = int(self.b_n_box.currentText())  # 获取到【过去】的时间长度
            print("yes")

            table2 = spread(end = self.end, table = self.df1, n = n, n0 = n0, want_list = want_list, year_list = self.year_list)
            print(table2)

            # 基础参数
            cofco_blue = "#013B89"
            cofco_orange = "#F7A501"
            long_range = "#FFF8DC"
            week_range = "#FFC125"
            linew = 1.2

            colorlist = ["#CD5555"]
            colorlist2 = sns.color_palette("Blues", 7)
            colorlist.extend(colorlist2)
            # 三大油主线
            colorlist = ["#475387", "#E4882E", "#D5DED9"]

            print("3")

            #for i in range(3):
            for i in range(len(want_list)):
                ax_spread.plot(table2["Date"], table2[table2.columns[1 + i * 4]], label=table2.columns[1 + i * 4],
                            color=colorlist[i], linewidth=linew)
                ax_spread.scatter(table2["Date"][n0-1], table2[table2.columns[1 + i * 4]][n0-1], s=60, c=colorlist[i])
                ax_spread.fill_between(table2["Date"], table2[table2.columns[1 + i * 4]], 0,
                                    where=(table2[table2.columns[1 + i * 4]] < 0),
                                    color=colorlist[i], alpha=0.4)
                ax_spread.plot(table2["Date"], table2[table2.columns[4 + i * 4]], label=table2.columns[4 + i * 4],
                            linestyle="--", color=colorlist[i])

            ax_spread.axvline(table2["Date"][n0 - 1], color='orange', linestyle='--', linewidth=0.8)

            print("4")

            # 画布基础设置
            ax_spread.spines['top'].set_visible(False)
            ax_spread.spines['right'].set_visible(False)
            ax_spread.spines['left'].set_visible(False)
            ax_spread.spines['bottom'].set_visible(False)

            # 修改坐标轴颜色
            ax_spread.spines['bottom'].set_edgecolor('gray')
            ax_spread.spines['left'].set_edgecolor('gray')
            ax_spread.tick_params(axis='both', colors='#404040')

            # 设置图例 去掉边框
            ax_spread.legend(frameon=False, loc="lower right")

            # 设置坐标轴标签
            ax_spread.set_xlabel('Time Line')

            # 设置标题
            ax_spread.set_title(close_spread_list + " " + "Spread", color=cofco_blue, loc="left", fontsize=10, pad=15)
            self.figCanvas.draw()

    # 画月差季节性的图
    # 更新到159主要合约间的月差
    def get_m_plot(self):

        use_axis = self.axis_box.currentText()

        if use_axis == "图1":
            ax3 = self.ax1
        elif use_axis == "图2":
            ax3 = self.ax2
        elif use_axis == "图3":
            ax3 = self.ax3
        elif use_axis == "图4":
            ax3 = self.ax4

        if self.df2.empty:
            pass
        else:
            ax3.clear()

            # 通过接收参数 创建出表格
            b_code = [str(self.m_box.currentText())]  # 获取到合约
            n0 = int(self.b_n0_box.currentText())  # 获取到【未来】的时间长度
            n = int(self.b_n_box.currentText())  # 获取到【过去】的时间长度
            b1_table = all_base2(end=self.end, table=self.df3, n0=n0, n=n, want_list=b_code, year_list=self.year_list)
            print(b1_table)

            # 基础参数
            cofco_blue = "#013B89"
            cofco_orange = "#F7A501"
            long_range = "#FFF8DC"
            week_range = "#FFC125"
            linew = 1.2
            colorlist = ["#CD5555"]
            colorlist2 = sns.color_palette("Blues", 7)
            colorlist.extend(colorlist2)

            for i in range(len(b1_table.columns) - 1):
                ax3.plot(b1_table["Date"], b1_table[b1_table.columns[1 + i]], label=b1_table.columns[1 + i],
                         color=colorlist[i], linewidth=linew)
                print("4")
                ax3.fill_between(b1_table["Date"], b1_table[b1_table.columns[1 + i]], 0,
                                 where=(b1_table[b1_table.columns[1 + i]] < 0),
                                 color=colorlist[i], alpha=0.4)

            ax3.axvspan(b1_table["Date"][n0 - 1], b1_table["Date"][n0 - 1 + 5], facecolor=week_range, alpha=0.1)
            ax3.axvspan(b1_table["Date"][n0 - 1], b1_table["Date"][n0 - 1 + 15], facecolor=long_range, alpha=0.2)

            ax3.scatter(b1_table["Date"][n0 - 1], b1_table[b1_table.columns[1]][n0 - 1], s=60, c=colorlist[0])
            ax3.axvline(b1_table["Date"][n0 - 1], color='orange', linestyle='--', linewidth=2)

            # 画布基础设置
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.spines['left'].set_visible(False)
            ax3.spines['bottom'].set_visible(False)

            # 显示零轴
            ax3.axhline(0, color='gray', linewidth=1)

            # 修改坐标轴颜色
            ax3.spines['bottom'].set_edgecolor('gray')
            ax3.spines['left'].set_edgecolor('gray')
            plt.tick_params(axis='both', colors='#404040')

            # 设置图例 去掉边框
            ax3.legend(frameon=False, loc="upper right")

            # 设置坐标轴标签
            ax3.set_xlabel('Time Line')

            # 设置标题
            ax3.set_title(b1_table.columns[1] + " " + 'Monthly Spread', color=cofco_blue, loc="left", fontsize=10, pad=15)
            self.figCanvas.draw()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ShowImagePane3()
    window.show()

    sys.exit(app.exec_())