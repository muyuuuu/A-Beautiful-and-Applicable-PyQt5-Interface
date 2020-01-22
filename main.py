#!/bin/bash
import sys, hashlib, sqlite3, re, PyQt5.QtGui
import qdarkstyle, datetime, webbrowser
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton, 
                            QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,
                            QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QRadioButton,
                            QTreeWidgetItem, QDesktopWidget, QTabWidget, QSpinBox, QComboBox,
                            QCalendarWidget, QDateTimeEdit, QMessageBox, QAbstractItemView,
                            QHeaderView, QTableWidget, QTableWidgetItem, QStyledItemDelegate,
                            QSizePolicy, QTextEdit, QScrollArea, QGroupBox)
from PyQt5.QtCore import Qt, QUrl, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import matplotlib.pyplot as plt

# 绘图的空白界面
class MymplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=500, height=400):
        plt.style.use('fivethirtyeight')
        self.fig = Figure(figsize=(width, height))
        self.axes = self.fig.add_subplot(111) # 多界面绘图
        self.axes.yaxis.tick_right()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    # 绘图类的绘图方法
    def plot_time(self, *args):
        # 修改字体
        n_bins = 10
        x = np.arange(n_bins)
        y1, y2, y3, y4 = np.random.randint(1, 25, size=(4, n_bins))

        self.axes.clear()
        self.fig.suptitle("Tabulation: NCST MMA contest information statistics")
        width = 0.2
        self.axes.bar(x, y1, width = 0.2)
        self.axes.bar(x + width, y2, width = 0.2)
        self.axes.bar(x + width * 2, y3, width = 0.2)
        self.axes.bar(x + width * 3, y4, width = 0.2)
        self.axes.set_ylabel("Statistics of participants")
        self.axes.grid(True)
        self.draw()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # 设置窗口名称
        self.setWindowTitle("华北理工数学建模协会比赛查询")

        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("华北理工大学数学建模协会制~")

        # 设置初始化的窗口大小
        self.setFixedSize(600, 400)

        # 设置初始化的窗口位置
        self.center()

        # 设置Qcomobox为显示正常，否则某项会过大
        self.delegate = QStyledItemDelegate()

        # 设置窗口透明度
        # self.setWindowOpacity(0.9) # 设置窗口透明度

        # 设置图标
        self.setWindowIcon(QIcon("1.jpg"))

        # 设置窗口样式
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 设置整体布局 左右显示
        pagelayout = QGridLayout()

        # 链接sql与查询
        try:
            self.db = sqlite3.connect('mathmodel.db')
            self.query = self.db.cursor()
        except:
            QMessageBox.critical(None, ("无法打开数据库"), ("SQlite支持"), QMessageBox.Cancel)
            return False

        """
        此处完成布局页面的基本功能
        布局分为左侧和右侧，左侧为按钮，右侧为堆栈布局，完成鼠标点击的页面切换功能
        最后两个布局部署在splitter中，完成页面内部拖拉界面可变大小
        """

        """ 左侧开始布局 """
        # 创建左侧主窗口
        top_left_frame = QFrame(self)  
        # 绘制矩形面板
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        #　左边按钮为垂直布局
        button_layout = QVBoxLayout(top_left_frame)
        # 登录按钮 用于验证身份
        verifyid_btn = QPushButton("确认身份")
        verifyid_btn.setFixedSize(100, 30)
        button_layout.addWidget(verifyid_btn)
        # 输入用户名　密码按钮
        # 因为在radiobutton中需要选择是否为管理员
        # 因此需要 确定某些按钮是否可用，所以，设置为self方便子函数的调用
        self.user_btn = QPushButton("登录")
        self.user_btn.setFixedSize(100, 30)
        button_layout.addWidget(self.user_btn)
        # 信息管理　按钮 （超级管理员可用）
        self.registor_btn = QPushButton("信息管理")
        self.registor_btn.setFixedSize(100, 30)
        button_layout.addWidget(self.registor_btn)
        # 录入信息 按钮 （普通管理员可用）
        self.input_btn = QPushButton("录入信息")
        self.input_btn.setFixedSize(100, 30)
        button_layout.addWidget(self.input_btn) 
        # 信息查询 按钮 （所有人可看）
        query_btn = QPushButton("查询信息")
        query_btn.setFixedSize(100, 30)
        button_layout.addWidget(query_btn) 
        # 建模之家　按钮 （建模学子的博客 不支持无技术门槛的博客）
        friend_btn = QPushButton("建模园地")
        friend_btn.setFixedSize(100, 30)
        button_layout.addWidget(friend_btn) 
        # 个人控件　按钮 （预留接口 完成建模的动态，组队等功能）
        space_btn = QPushButton("个人空间")
        space_btn.setFixedSize(100, 30)
        button_layout.addWidget(space_btn)      
        # 退出按钮
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(100, 30), quit_btn.setText("退出")
        button_layout.addWidget(quit_btn)
        # 增加间距，美化界面
        button_layout.addStretch(1)


        """
        右侧开始布局 单击左侧的按钮 对应到右侧不同的界面
        每个界面的布局详细介绍
        """

        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # 右边显示为stack布局 即点击按钮，右侧会加载不同的页面
        self.right_layout = QStackedLayout(right_frame)
        # 右侧的布局已经传入了 right_frame 参数 所以后续的控件不用加此参数 布局 addwidget 即可

        # 确认身份 界面
        # 管理员身份
        self.radio_btn_admin = QRadioButton()
        self.radio_btn_admin.setText("我是管理员，来输入数据的")
        # 游客身份 二者只能选一个
        self.radio_btn_user = QRadioButton()
        self.radio_btn_user.setText("我是游客，就来看看")
        # 以垂直布局管理器管理 并设置为第一个界面
        radio_btn_layout = QVBoxLayout()  
        radio_btn_widget = QWidget()
        radio_btn_layout.addWidget(self.radio_btn_admin)
        radio_btn_layout.addWidget(self.radio_btn_user)
        radio_btn_widget.setLayout(radio_btn_layout)
        self.right_layout.addWidget(radio_btn_widget)

        # 管理员的登录界面 
        # 分超级管理和普通管理 游客无帐号，且账号密码错误无法登录
        self.user_line = QLineEdit()
        self.user_line.setPlaceholderText("请输入账号：")
        self.user_line.setFixedWidth(400)
        self.password_line = QLineEdit()
        self.password_line.setPlaceholderText("请输入密码：")
        self.password_line.setEchoMode(QLineEdit.Password)
        self.password_line.setFixedWidth(400)
        # 帐号密码的布局
        login_layout = QVBoxLayout()
        login_btn_layout = QHBoxLayout()
        login_btn_cancel = QPushButton("取消")
        login_btn_cancel.setFixedWidth(80)
        login_btn_confirm = QPushButton("确认")
        login_btn_confirm.setFixedWidth(80)
        # 按钮的布局
        login_btn_layout.addWidget(login_btn_cancel)
        login_btn_layout.addWidget(login_btn_confirm)
        login_widget = QWidget()
        login_widget.setLayout(login_layout)
        # 添加全部元素的布局
        login_layout.addWidget(self.user_line)
        login_layout.addWidget(self.password_line)
        login_layout.addLayout(login_btn_layout)
        # 添加至右侧的layout布局 也是第二个界面
        self.right_layout.addWidget(login_widget)

        # 信息管理页面 
        # 只有超级管理员才能看
        # 此界面为 Qtabwidget 多窗口切换的界面 单击不同的标签 完成界面内不同界面的切换
        info_mana = QTabWidget()
        self.right_layout.addWidget(info_mana)
        # 分为 注册普通管理 教师管理 学院专业管理 竞赛管理四个标签页面
        admin_info = QWidget()
        teach_info = QWidget()
        colleage_major_info = QWidget()
        contest_info = QWidget()
        # 添加上述的四个标签
        info_mana.addTab(admin_info, "帐号管理")
        info_mana.addTab(teach_info, "教师管理")
        info_mana.addTab(colleage_major_info, "学院专业管理")
        info_mana.addTab(contest_info, "竞赛管理")
        register_label = QLabel("这里申请账号")

        # 注册帐号的页面 输入 确认密码 可以删除 表格显示
        self.registor_id = QLineEdit()
        self.registor_id.setPlaceholderText("请输入新帐号：")
        self.registor_id.setFixedWidth(400)
        self.registor_psd = QLineEdit()
        # 注册的密码
        self.registor_psd.setPlaceholderText("请输入密码：")
        self.registor_psd.setFixedWidth(400)
        # 设置为密码显示 即不显示原文
        self.registor_psd.setEchoMode(QLineEdit.Password)
        # 再次输入密码 两次密码不一致 无法注册
        self.registor_confirm = QLineEdit()
        self.registor_confirm.setPlaceholderText("请确认密码：")
        self.registor_confirm.setFixedWidth(400)
        self.registor_confirm.setEchoMode(QLineEdit.Password)
        self.registor_confirm_btn = QPushButton("确认提交")
        self.registor_confirm_btn.setFixedSize(100, 30)
        # 刷新后看到全部注册申请的普通管理员帐号
        register_btn_del = QPushButton("确认删除")
        register_btn_del.setFixedSize(100, 30)
        # 设置用于显示普通管理员帐号的表格 易于展示
        self.registor_table = QTableWidget()
        # 视图仅进行观察，不可修改 tableview父类可用的，tablewidget子类也可以用 因此选择了子类
        # 将所有的表格放入一个字典中 方便后期同一的初始化 代码维护方便 
        # 使用字典 在初始化时可以判断哪个对象调用了方法 因为每个对象的具体操作有些不同 
        # 后来发现多此一举 完全可以增加一个参数解决这个问题
        self.table = {}
        # 只有在超级管理员 页面才显示 普通状态只创建 但不加载
        self.table['registor_table'] = self.registor_table
        # 设置注册帐号的布局 并添加控件 
        registor_btn_layout = QHBoxLayout()
        registor_layout = QVBoxLayout()
        register_widget = QWidget()
        register_widget.setLayout(registor_layout)
        registor_layout.addWidget(register_label)
        registor_layout.addWidget(self.registor_id)
        registor_layout.addWidget(self.registor_psd)
        registor_layout.addWidget(self.registor_confirm)
        registor_btn_layout.addWidget(self.registor_confirm_btn)
        registor_btn_layout.addWidget(register_btn_del)
        registor_layout.addLayout(registor_btn_layout)
        registor_layout.addWidget(self.table['registor_table'])
        # 最后将添加完控件的布局 部署到第一个标签栏中
        admin_info.setLayout(registor_layout)

        # 开始设置教师信息管理的标签栏 输入注册 有删除按钮 表格显示
        teacher_layout = QVBoxLayout()
        teacher_table_layout = QHBoxLayout()
        teacher_input_layout = QVBoxLayout()
        teacher_layout.addLayout(teacher_input_layout)
        teacher_layout.addLayout(teacher_table_layout)
        # 显示教师信息的表格 
        self.teacher_table = QTableWidget()
        # 只有在超级管理员 页面才显示 普通状态只创建 但不加载
        self.table['teacher_table'] = QTableWidget()
        teacher_table_layout.addWidget(self.table['teacher_table'])
        self.teacher_input_name_line = QLineEdit()
        self.teacher_input_name_line.setPlaceholderText("请输入教师姓名")
        teacher_input_como_layout = QHBoxLayout()
        teacher_input_college_label = QLabel("请输入教师学院")
        teacher_input_college_label.setFixedWidth(200)
        # 学院在 comobox内 连接数据库加载选项 不能随意输入 且 只有在超级管理员状态下加载
        self.teacher_input_college_como = QComboBox()
        teacher_input_como_layout.addWidget(teacher_input_college_label)
        teacher_input_como_layout.addWidget(self.teacher_input_college_como)
        self.teacher_input_id_line = QLineEdit()
        self.teacher_input_id_line.setPlaceholderText("请输入教师工号")
        teacher_input_btn_layout = QHBoxLayout()
        teacher_input_btn_confirm = QPushButton("确认申请")
        teacher_input_btn_layout.addWidget(teacher_input_btn_confirm)
        teacher_input_btn_del = QPushButton("确认删除")
        teacher_input_btn_layout.addWidget(teacher_input_btn_del)
        #　添加上述控件
        teacher_input_layout.addWidget(self.teacher_input_name_line)
        teacher_input_layout.addLayout(teacher_input_como_layout)
        teacher_input_layout.addWidget(self.teacher_input_id_line)
        teacher_input_layout.addLayout(teacher_input_btn_layout)
        # 设置教师页面的布局
        teach_info.setLayout(teacher_layout)
        
        # 学院专业管理标签界面 输入 有删除按钮 表格显示
        colleage_major_info_layout = QVBoxLayout()
        colleage_major_info_button_layout = QHBoxLayout()
        colleage_major_info_layout.addLayout(colleage_major_info_button_layout)
        self.colleage_major_info_college = QLineEdit()
        self.colleage_major_info_college.setPlaceholderText("请输入插入的学院")
        self.colleage_major_info_major = QLineEdit()
        self.colleage_major_info_major.setPlaceholderText("请输入插入的专业")
        self.colleage_major_input_btn = QPushButton("确定插入")
        colleage_major_del_btn = QPushButton("确定删除")
        colleage_major_info_button_layout.addWidget(self.colleage_major_info_college)
        colleage_major_info_button_layout.addWidget(self.colleage_major_info_major)
        colleage_major_info_button_layout.addWidget(self.colleage_major_input_btn)
        colleage_major_info_button_layout.addWidget(colleage_major_del_btn)
        self.colleage_major_twoside = QTableWidget()
        self.table['colleage_major_twoside'] = self.colleage_major_twoside
        colleage_major_info_layout.addWidget(self.table['colleage_major_twoside'])
        colleage_major_info.setLayout(colleage_major_info_layout)

        #  竞赛管理的标签页面 输入竞赛 删除按钮完成删除 表格显示
        contest_layout = QVBoxLayout()
        contest_info.setLayout(contest_layout)
        self.contest_info_table = QTableWidget()
        self.table['contest_info_table'] = self.contest_info_table
        contest_input_layout = QVBoxLayout()
        self.contest_input_sponsor_line = QLineEdit()
        self.contest_input_sponsor_line.setPlaceholderText("输入主办方")
        self.contest_input_class_line = QLineEdit()
        self.contest_input_class_line.setPlaceholderText("比赛级别")
        self.contest_input_id_line = QLineEdit()
        self.contest_input_id_line.setPlaceholderText("比赛名称")
        contest_input_layout.addWidget(self.contest_input_sponsor_line)
        contest_input_layout.addWidget(self.contest_input_class_line)
        contest_input_layout.addWidget(self.contest_input_id_line)
        contest_layout.addLayout(contest_input_layout)
        contest_layout.addWidget(self.table['contest_info_table'])
        manage_contest_layout = QHBoxLayout()
        manage_contest_button_input = QPushButton()
        manage_contest_button_input.setText("输入比赛")
        manage_contest_button_del = QPushButton()
        manage_contest_button_del.setText("删除比赛")
        manage_contest_layout.addWidget(manage_contest_button_input)
        manage_contest_layout.addWidget(manage_contest_button_del)
        contest_layout.addLayout(manage_contest_layout)
        
        """
        这个是普通管理员输入比赛信息的页面
        建模园地输入 建模学子的博客信息 treeview控件加载控制选项关闭或者展开
        不适用内置的webengine库，缓存不够容易卡死，选择调用系统浏览器完成加载
        比赛录入 录入三个人的比赛信息（数据库无主键）：学号 姓名 学院 专业 性别 教师 比赛 奖项 比赛的开始时间 结束时间 获奖时间
        """

        # 建模园地 使用 TreeView　水平布局， 可以设置选项显示或者关闭 选择
        # 读取数据库(姓名 专业 年级 域名)加载建模学子的博客 （且即使不是管理员身份 也要加载）
        self.friend_tree = QTreeWidget()
        self.friend_tree.setColumnCount(2)  # 三列 
        # 设置标题
        self.friend_tree.setHeaderLabels(['年级', '人员, 网址, 个签, 曾获最高奖，点击打开网页（请用Chrome或Firefox打开）']) 
        self.friend_tree.setColumnWidth(1, 400) # 设置第一列的宽度
        friend_widget = QWidget()
        friend_layout = QVBoxLayout()
        friend_widget.setLayout(friend_layout)
        friend_label = QLabel("如想加入自己的博客，请联系建模协会官方人员。")
        friend_label1 = QLabel("注意：不支持加入在CSDN，博客园，知乎等借助第三方平台编写的无技术门槛的博客，鼓励与推荐hexo或jekyll。")
        friend_layout.addWidget(friend_label)
        friend_layout.addWidget(friend_label1)
        friend_layout.addWidget(self.friend_tree)
        self.right_layout.addWidget(friend_widget)
        input_tab = QTabWidget()
        self.right_layout.addWidget(input_tab)
        # 录入信息中的建模园地
        input_friend_widget = QWidget()
        input_friend_layout = QVBoxLayout()
        self.input_friend_name = QLineEdit()
        self.input_friend_name.setPlaceholderText("请输入姓名")
        self.input_friend_url = QLineEdit()
        self.input_friend_url.setPlaceholderText("请输入网址(不可为空，不可和已有的网址的重复)")
        input_friend_label = QLabel("请选择年级")
        input_friend_label.setMaximumHeight(20)
        # 上下两个方向键输入 防止乱输入
        self.input_friend_class = QSpinBox()
        self.input_friend_class.setMinimum(2013)
        self.input_friend_class.setMaximum(3000)
        # 设置为当前年份
        current_year = datetime.datetime.now().year
        self.input_friend_class.setValue(current_year)
        self.input_friend_sign = QLineEdit()
        self.input_friend_sign.setPlaceholderText("请输入个性签名")
        self.input_friend_price = QLineEdit()
        self.input_friend_price.setPlaceholderText("请输入最高奖项, 没有写无")         
        input_friend_button = QPushButton("确认输入") 
        del_friend_button = QPushButton("确认删除")
        # 创立博客的视图 便于维护   
        self.input_friend_table = QTableWidget(right_frame)
        self.table['input_friend_table'] = self.input_friend_table
        #　添加控件
        input_friend_layout.addWidget(self.input_friend_name)
        input_friend_layout.addWidget(self.input_friend_url)
        input_friend_layout.addWidget(input_friend_label)
        input_friend_layout.addWidget(self.input_friend_class)
        input_friend_layout.addWidget(self.input_friend_sign)
        input_friend_layout.addWidget(self.input_friend_price)
        input_friend_layout.addWidget(input_friend_button)
        input_friend_layout.addWidget(self.table['input_friend_table'])
        input_friend_layout.addWidget(del_friend_button)
        input_friend_widget.setLayout(input_friend_layout)
        input_tab.addTab(input_friend_widget, "建模园地")

        # 录入信息中的录入比赛标签
        input_contest_widget = QWidget(right_frame)
        # 第一个水平布局，选择比赛
        input_contest_layout = QVBoxLayout()
        input_contest_widget.setLayout(input_contest_layout)
        input_contest_name_layout = QHBoxLayout()
        input_contest_label = QLabel("请选择比赛")
        input_contest_label.setFixedWidth(100)
        # 应该在确认身份后加载数据 而不是加载数据但不给普通用户显示 可能会泄漏到内存
        self.input_contest_class = QComboBox()
        input_contest_teacher_label = QLabel("指导教师")
        self.input_contest_teacher_name = QComboBox()
        input_contest_teacher_label.setFixedWidth(100)
        input_contest_name_layout.addWidget(input_contest_label)
        input_contest_name_layout.addWidget(self.input_contest_class)
        input_contest_name_layout.addWidget(input_contest_teacher_label)
        input_contest_name_layout.addWidget(self.input_contest_teacher_name)
        input_contest_layout.addLayout(input_contest_name_layout)
        # 第二个水平布局，选择比赛的起止时间
        input_contest_time_layout = QHBoxLayout()
        input_contest_time_begin = QLabel("开始时间")
        input_contest_time_begin.setFixedWidth(100)
        self.input_contest_time_begincomo = QDateTimeEdit()
        # 三年前 即录入比赛的最大年限为三年 三年内不录入则无法录入
        self.input_contest_time_begincomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        self.input_contest_time_begincomo.setCalendarPopup(True)
        input_contest_time_end = QLabel("结束时间")
        input_contest_time_end.setFixedWidth(100)
        self.input_contest_time_endcomo = QDateTimeEdit()
        self.input_contest_time_endcomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        self.input_contest_time_endcomo.setCalendarPopup(True)
        input_contest_time_in = QLabel("获奖时间")
        input_contest_time_in.setFixedWidth(100)
        self.input_contest_time_incomo = QDateTimeEdit()
        self.input_contest_time_incomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        self.input_contest_time_incomo.setCalendarPopup(True)
        input_contest_time_layout.addWidget(input_contest_time_begin)
        input_contest_time_layout.addWidget(self.input_contest_time_begincomo)
        input_contest_time_layout.addWidget(input_contest_time_end)
        input_contest_time_layout.addWidget(self.input_contest_time_endcomo)
        input_contest_time_layout.addWidget(input_contest_time_in)
        input_contest_time_layout.addWidget(self.input_contest_time_incomo)
        input_contest_layout.addLayout(input_contest_time_layout)
        # 添加此标签栏
        input_tab.addTab(input_contest_widget, "录入比赛")

        # 录入比赛信息 队员的信息控件使用字典创建 
        # 因为要录入三个人的比赛信息 所以选择了for循环 而不是写三次
        self.team = {}
        for i in range(1, 4):
            self.team['team_layout' + str(i)] = QHBoxLayout()
            self.team['team_id' + str(i)] = QLineEdit()
            self.team['team_id' + str(i)].setFixedWidth(230)
            self.team['team_id' + str(i)].setPlaceholderText("请输入学号")
            self.team['team_name' + str(i)] = QLineEdit()
            self.team['team_name' + str(i)].setFixedWidth(220)
            self.team['team_name' + str(i)].setPlaceholderText("请输入姓名")
            self.team['team_price' + str(i)] = QComboBox()
            self.team['team_price' + str(i)].setFixedWidth(220)
            self.team['team_college' + str(i)] = QComboBox()
            self.team['team_major' + str(i)] = QComboBox()
            self.team['team_gender' + str(i)] = QComboBox()
            self.team['team_layout' + str(i)].addWidget(self.team['team_id' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_name' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_price' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_college' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_major' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_gender' + str(i)])
            input_contest_layout.addLayout(self.team['team_layout' + str(i)])

        # 防止输入错误的情况发生 增加的删除 修改按钮 （方便修改 此处的视图可编辑）
        # 修改后重新提交数据库即可 且修改内容仅为本次输入的数据 并非修改历史数据
        input_contest_button_layout = QHBoxLayout() 
        input_contest_button_input = QPushButton("确认输入人员信息")
        input_contest_button_del = QPushButton("确认删除人员信息")
        input_contest_button_update = QPushButton("确认提交更改")
        input_contest_button_layout.addWidget(input_contest_button_input)
        input_contest_button_layout.addWidget(input_contest_button_del)
        input_contest_button_layout.addWidget(input_contest_button_update)
        input_contest_layout.addLayout(input_contest_button_layout)
        self.input_contest_info_table = QTableWidget()  
        self.table['input_contest_info_table'] = self.input_contest_info_table
        input_contest_layout.addWidget(self.table['input_contest_info_table'])
        # 应该在增加一个删除某个人历史数据的界面 待增加

        """
        查询信息的界面 游客身份而可查询 即只有管理员可录入数据 其它外来人员只能查看
        因此 这部份的数据库要一开始就加载
        """
        
        # 查询信息
        output_tab = QTabWidget(right_frame)
        self.right_layout.addWidget(output_tab)
        output_year = QWidget()
        output_teacher = QWidget()
        output_sduent = QWidget()
        # 同样分为四个标签
        output_tab.addTab(output_year, "按时间查询")
        output_tab.addTab(output_teacher, "按教师查询")
        output_tab.addTab(output_sduent, "按学生查询")

        # 按年份查询 查询内容为
        # 一年内几个比赛的人数对比 一个比赛的历年总人数对比
        # 普通用户只能看到统计图片 管理员点击按钮时可以保存数据
        output_year_layout = QVBoxLayout()
        output_year.setLayout(output_year_layout)
        output_year_button_layout = QHBoxLayout()
        self.output_year_comobo = QComboBox()
        self.output_year_comobo.addItem("选择要查询的比赛")
        self.output_year_comobo.setItemDelegate(self.delegate)
        output_year_oneyear = QPushButton("这一年参赛人数统计")
        output_year_allyear = QPushButton("此比赛历年情况对比")
        output_year_button_layout.addWidget(self.output_year_comobo)
        output_year_button_layout.addWidget(output_year_oneyear)
        output_year_button_layout.addWidget(output_year_allyear)
        output_year_layout.addLayout(output_year_button_layout)
        # 增加matplotlib 绘图的面板和工具栏
        mpl_layout = QVBoxLayout()
        self.mpl = MymplCanvas(self)
        self.mpl_tool = NavigationToolbar(self.mpl, self)
        mpl_layout.addWidget(self.mpl)
        mpl_layout.addWidget(self.mpl_tool)
        mpl_scroll = QScrollArea()
        mpl_groupBox = QGroupBox()
        mpl_groupBox.setLayout(mpl_layout)
        mpl_scroll.setWidget(mpl_groupBox)
        mpl_scroll.setWidgetResizable(True)
        # 根据实际情况修改

        self.mpl.setFixedWidth(5000)
        output_year_layout.addWidget(mpl_scroll)

        # 按教师查询
        output_teacher_layout = QVBoxLayout()
        output_teacher.setLayout(output_teacher_layout)
        self.output_teacher_comobo = QComboBox()
        self.output_teacher_result = QTextEdit()
        # 输出的查询结果为只读 不可写
        self.output_teacher_result.setReadOnly(True)
        output_teacher_layout.addWidget(self.output_teacher_comobo)
        output_teacher_layout.addWidget(self.output_teacher_result)
        self.insert_teacher_comobo(self.output_teacher_comobo)
        
        # 按照学生查询
        output_sduent_layout = QVBoxLayout()
        output_sduent.setLayout(output_sduent_layout)
        self.output_sduent_line = QLineEdit()
        self.output_sduent_line.setPlaceholderText("输入学号，回车即可查询")
        self.output_sduent_result = QTextEdit()
        # 同样为只读查询
        self.output_sduent_result.setReadOnly(True)
        output_sduent_layout.addWidget(self.output_sduent_line)
        output_sduent_layout.addWidget(self.output_sduent_result)

        # 三分界面，可拖动
        self.splitter1 = QSplitter(Qt.Vertical)
        # top_left_frame.setFixedHeight(280)
        self.splitter1.addWidget(top_left_frame)
        self.splitter1.setMinimumWidth(150)
        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setMinimumWidth(250)
        #　添加右侧的布局
        self.splitter2.addWidget(right_frame)

        # 窗口部件添加布局
        widget = QWidget()
        pagelayout.addWidget(self.splitter2)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        """
        此处为函数功能区域 完成和用户交互的逻辑部分 响应用户的操作事件
        """

        """展示一致的页面"""
        # 最开始 登录 信息管理 信息录入的界面均不可选
        self.user_btn.setEnabled(False)
        self.registor_btn.setEnabled(False)
        self.input_btn.setEnabled(False)
        # 认证按钮 对应页面：选择是游客还是管理员
        verifyid_btn.clicked.connect(self.show_verifyid_page)
        # 对应页面 登录。如果登录按钮 可以展示给游客
        self.user_btn.clicked.connect(self.show_login_page)
        # 此页面只能被加载一次
        self.show_register_page_count = 0
        # 对应 信息管理的页面 
        self.registor_btn.clicked.connect(self.show_register_page)
        # 用于设置次数 防止多次点击 多次加载建模园地的数据 加载一次即可
        self.page_count = 1
        # 对应建模园地的也页面
        friend_btn.clicked.connect(self.show_friend_page)
        # 对应 录入信息的页面
        self.input_btn.clicked.connect(self.show_input)
        # Treeview的点击事件 点击后调用系统浏览器加载页面
        self.friend_tree.clicked.connect(self.show_firend_web)
        # 对应查询信息的页面
        query_btn.clicked.connect(self.show_output)
        # 对应退出页面
        quit_btn.clicked.connect(self.quit_act)

        """ 按钮对应的逻辑函数"""

        # 最开始的确认身份 radio button只能选择一个 判断状态 
        self.radio_btn_user.toggled.connect(self.change_status)
        self.radio_btn_admin.toggled.connect(self.change_status)

        # 点击按钮 超级管理员会删除普通管理员
        register_btn_del.clicked.connect(self.del_admin)

        # 点击登录按钮后 要链接数据库确认密码是否正确
        login_btn_confirm.clicked.connect(self.confirm_password)

        # 申请普通管理员时，把信息插入到数据库
        self.registor_confirm_btn.clicked.connect(self.insert_admin)

        # 信息管理页面下 教师管理标签。确认申请老师的帐号后 数据表格显示 默认状态不显示
        teacher_input_btn_confirm.clicked.connect(self.input_teacher_info)
        # 点击按钮后 删除教师帐号
        teacher_input_btn_del.clicked.connect(self.delete_teacher_info)
        # 确定删除学院和专业信息
        colleage_major_del_btn.clicked.connect(self.del_college_major)

        # 信息管理页面 竞赛管理标签下 点击插入比赛 删除比赛时显示比赛信息的数据表 默认不显示
        manage_contest_button_input.clicked.connect(self.process_contest)
        manage_contest_button_del.clicked.connect(self.process_contest)

        # 信息管理页面下 以双列表格的形式展示学院和专业 点击学院，则查询学院对应的专业
        self.table['colleage_major_twoside'].clicked.connect(self.show_major)

        #　信息管理页面下的学院专业管理标签 设置标记数　统计上次专业的数量　下次显示时先清空在显示，所以需要计数
        self.major_count = 0
        # 信息管理页面下的学院专业管理标签 插入、学院和专业的信息
        self.colleage_major_input_btn.clicked.connect(self.insert_college_major)
        # 插入的学院和专业的内容更改后 才允许插入 否则会重复
        self.colleage_major_info_college.textChanged.connect(self.enable_colleage_major_input_btn)
        self.colleage_major_info_major.textChanged.connect(self.enable_colleage_major_input_btn)

        # 信息录入页面下 输入与删除建模学子博客
        input_friend_button.clicked.connect(self.insert_stublog)
        del_friend_button.clicked.connect(self.del_friend_table)

        # 录入信息页面 从comobox里面选择超级管理员指定的比赛 
        self.input_contest_class.setItemDelegate(self.delegate)
        
        # 录入信息页面 从（comobox）中选择教师信息
        self.insert_teacher_comobo(self.input_contest_teacher_name)

        # 信息查询页面 点击按钮后展示 matplotlib 绘图 
        output_year_oneyear.clicked.connect(self.draw_one_year)
        output_year_allyear.clicked.connect(self.draw_all_year)

        # 普通管理员插入时 统计表格的行号 再次输入新的数据时 在原来数据的后面追加
        self.input_contest_row_count = 0
        # 普通管理员的插入信息 一次性插入三个人
        input_contest_button_input.clicked.connect(self.input_contest_one)
        # 只删除一条
        input_contest_button_del.clicked.connect(self.del_contest_one)
        # 为了便于管理员的输入 表格设置为可编辑 编辑完点击更新 即可完成数据库端的更新
        input_contest_button_update.clicked.connect(self.update_contest_info)

        # 此处为在信息录入页面的比赛、性别选择框录入输入好的数据
        # 此部分数据无机密 所以可以直接在软件运行时加载 泄漏到内存中
        # 三个队员的学院
        for i in range(1, 4):
            self.query.execute("select * from college")
            colleges = self.query.fetchall()
            self.team["team_college" + str(i)].setItemDelegate(self.delegate)
            self.team["team_major" + str(i)].setItemDelegate(self.delegate)
            self.team["team_college" + str(i)].addItem("")
            for college_name in colleges:
                college_ = str(college_name[0])
                self.team["team_college" + str(i)].addItem(college_)
        
        # 三个队员的性别 
        for i in range(1, 4):
            self.team["team_gender" + str(i)].setFixedWidth(50)
            self.team["team_gender" + str(i)].setItemDelegate(self.delegate)
            for gender in ['男', '女']:
                self.team["team_gender" + str(i)].addItem(gender)            

        # 学院改变时专业跟随改变 即只能看到该学院对应的几个专业 减少专业的查找量 
        self.team["team_college1"].currentIndexChanged.connect(self.change_major1)
        self.team["team_college2"].currentIndexChanged.connect(self.change_major2)
        self.team["team_college3"].currentIndexChanged.connect(self.change_major3)

        # 比赛改变时 奖项跟随改变
        self.input_contest_class.currentIndexChanged.connect(self.select_contest_class)

        # 表格双击触发编辑事件，判断是否为空。
        # 空：表示在空白单元格输入信息 此是不允许
        # 非空：表示单元格内有内容 此时可以编辑
        self.table['input_contest_info_table'].cellDoubleClicked.connect(self.confirm_update)

        # 查询页面 输入学生的学号 回车即可查询
        self.output_sduent_line.returnPressed.connect(self.query_sdu)

        # 按教师查询 教师下拉框改变后触发
        self.output_teacher_comobo.currentTextChanged.connect(self.query_teacher)

    # 信息录入界面
    def select_contest_class(self):
        """
        根据 input_contest_class 选择的比赛名称 对应改比赛的奖项
        """
        if self.input_contest_class.currentText() == '全国大学生数学建模竞赛':
            for i in range (1, 4):
                self.team['team_price' + str(i)].setItemDelegate(self.delegate)
                self.team['team_price' + str(i)].addItem('国家一等奖')
                self.team['team_price' + str(i)].addItem('国家二等奖')
                self.team['team_price' + str(i)].addItem('省级一等奖')
                self.team['team_price' + str(i)].addItem('省级二等奖')
                self.team['team_price' + str(i)].addItem('成功参赛奖')
        if self.input_contest_class.currentText() == '美国大学生数学建模竞赛':
            for i in range (1, 4):
                self.team['team_price' + str(i)].setItemDelegate(self.delegate)
                self.team['team_price' + str(i)].addItem('Outstanding Winner')
                self.team['team_price' + str(i)].addItem('Finalist')
                self.team['team_price' + str(i)].addItem('Meritorious Winner')
                self.team['team_price' + str(i)].addItem('Honorable Mention')
                self.team['team_price' + str(i)].addItem('Successful Participant')
                self.team['team_price' + str(i)].addItem('Unsuccessful Participant')
                self.team['team_price' + str(i)].addItem('Disqualified')

    # 信息管理 信息录入界面
    def init_table(self, string = ''):
        """
        因多个界面涉及到了表格的初始化 所以封装到一个函数中
        所有表格放到一个字典中 根据字典的 ID 调用对象 增加一个string参数判断调用对象
        只是调用初始化表格的位置不同 表格在何时可以显示也需要严密的逻辑
        """
        
        # 均不显示垂直表头
        self.table[string].verticalHeader().setVisible(False)

        # 不可编辑的 建模园地 竞赛管理 教师管理 普通管理员管理
        # 视图仅进行观察，不可修改 tableview可用的，tablewidget也可以用
        if string in ['input_friend_table', 'contest_info_table', 'teacher_table', 'registor_table']:
            self.table[string].setEditTriggers(QAbstractItemView.NoEditTriggers)                

        # 视图整行选中的
        if string in ['input_friend_table', 'input_contest_info_table', 'contest_info_table', 'teacher_table']:
            self.table[string].setSelectionBehavior(QAbstractItemView.SelectRows)

        # 自适应伸缩的 不能用elif
        if string in ['input_friend_table', 'contest_info_table', 'colleage_major_twoside', 'teacher_table', 'registor_table']:
            self.table[string].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if string == 'input_friend_table':
            # 博客的表格
            self.table[string].setColumnCount(2)
            self.table[string].setRowCount(1000)
            self.table[string].setHorizontalHeaderLabels(['人员','其他信息'])

        elif string == 'input_contest_info_table':
            # 录入比赛的表格
            self.table[string].setColumnCount(11)
            self.table[string].setRowCount(1000)
            self.table[string].setHorizontalHeaderLabels(['学号','姓名',' 学院',' 专业', '性别', '开始时间', '结束时间', '获奖时间'
                , '指导教师', '比赛', '奖项级别'])
            self.table[string].setColumnWidth(0, 150)
            self.table[string].setColumnWidth(1, 150)
            self.table[string].setColumnWidth(2, 200)
            self.table[string].setColumnWidth(3, 200)
            self.table[string].setColumnWidth(4, 80)
            self.table[string].setColumnWidth(5, 150)
            self.table[string].setColumnWidth(6, 150)
            self.table[string].setColumnWidth(7, 150)
            self.table[string].setColumnWidth(8, 150)
            self.table[string].setColumnWidth(9, 300)
            self.table[string].setColumnWidth(10, 100)

        elif string == 'contest_info_table':
            # 竞赛管理的表格
            self.table[string].setFixedHeight(400)
            # self.contest_info_table.setFixedHeight
            self.table[string].setRowCount(100)
            self.table[string].setColumnCount(3)
            self.table[string].setHorizontalHeaderLabels(['主办方','比赛级别','比赛名称'])

        elif string == 'colleage_major_twoside':
            # 信息管理页面 学院专业的表格
            self.table[string].setColumnCount(2)
            self.table[string].setRowCount(50)
            self.table[string].setHorizontalHeaderLabels(['学院','专业'])

        elif string == 'teacher_table':
            # 信息管理页面 教师的表格
            self.table[string].setFixedHeight(400)
            self.table[string].setRowCount(100)
            self.table[string].setColumnCount(3)
            self.table[string].setHorizontalHeaderLabels(['教师名称','教师学院','教师工号'])

        elif string == 'registor_table':
            # 如果是 信息管理页面的 观看普通管理员的表格
            # 共 100 行 1 列
            self.table[string].setRowCount(100)
            self.table[string].setColumnCount(1)
            self.table[string].setHorizontalHeaderLabels(['帐号名称'])

    # 查询界面的 查询教师指导情况
    def query_teacher(self):
        """
        输入： combobox内选择的教师的工号
        输出： 查询这个老师指导比赛的情况
        """
        flag = 0
        info_ = self.output_teacher_comobo.currentText()
        self.query.execute("select * from sducontest where teacher = \"{}\"".format(info_))
        results = self.query.fetchall()
        if len(results) == 0:
            self.output_teacher_result.setText("暂无信息")
        else:
            string = ""
            for result in results:
                # 学号不输出
                for i in result:
                    string += i
                    string += "  "
                string += "\n"
            self.output_teacher_result.setText(string)            

    # 查询界面的 查询学生参赛情况标签
    def query_sdu(self):
        """
        输入： 学号或姓名 输入违法提示：输入无效
        输出： 输出学生的姓名、性别、学号(含有年级)、专业、获奖情况(包含指导教师)、QQ号(是否要输出，仅管理员可见)
        """
        #　检查是否有效输入
        flag = 0 
        info_ = self.output_sduent_line.text()
        if (str.isdigit(info_)):
            self.query.execute("select * from sducontest where id = \"{}\"".format(info_))
            results = self.query.fetchall()
        elif (str.isalpha(info_)):
            self.query.execute("select * from sducontest where name = \"{}\"".format(info_))
            results = self.query.fetchall()
        else:
            QMessageBox.information(None, ("友情提示"), ("输入无效"), QMessageBox.Cancel)
            flag = 1
        if flag == 0:
            string = ""
            # 有查询结果
            if len(results) != 0:
                for result in results:
                    # 学号不输出
                    for i in result:
                        string += i
                        string += "  "
                    string += "\n"
                self.output_sduent_result.setText(string)
            else:
                self.output_sduent_result.setText("查无此人")

    def insert_contest_combo(self, a):
        """
        a 是调用的对象
        因为 信息管理 录入比赛 查询比赛 的combox都需要加入比赛框 避免代码重复 此部份程序封装为函数
        contest 是竞赛的数据表
        """
        a.clear()
        self.query.execute("select * from contest")
        rows = self.query.fetchall()
        for row in rows:
            item = str(row[2])
            a.addItem(item)

    # 录入信息界面的录入比赛标签 
    def confirm_update(self):
        """
        判断当前编辑的表格项是否为空
        若为空 提示不可修改且将表格设置为不可编辑 
        若不为空 允许双击事件，取消表格的不可编辑状态 不可用alledittriggers
        """
        item = self.table['input_contest_info_table'].currentItem()
        try:
            text = item.text()
            # 允许表格编辑 取消可能在上次设置的不可编辑事件
            self.table['input_contest_info_table'].setEditTriggers(QAbstractItemView.DoubleClicked)
        except :
            QMessageBox.information(None, ("友情提示"), ("空内容无法修改，只能修改已有内容"), QMessageBox.Cancel)
            self.table['input_contest_info_table'].setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 录入信息界面的录入比赛标签 
    def update_contest_info(self):
        """
        获取修改部分 对修改后的表格提交到数据库 完成修改
        """
        # self.input_contest_info_table
        pass

    # 录入信息界面的录入比赛标签 
    def del_contest_one(self):
        """
        删除选中的一条比赛 没必要因一个人的输入错误 而删除三个人的信息
        """
        # self.input_contest_info_table
        pass

    #　录入信息页面的录入比赛标签
    def input_contest_one(self):
        """ 
        创建空列表 添加三个队员的信息 （1，4）是因为最初的字典是设立的这个索引
        添加完毕后 插入到数据库 并显示在表格中
        """
        # 学号 姓名 学院 专业 性别 开始时间 结束时间 获奖时间 教师 比赛名称 获奖级别
        id_, name_, college_, major_, gender_, begin_time, end_time, in_time, teacher_, contest_, class_ \
            = [], [], [], [], [], [], [], [], [], [], [] 
        for i in range(1, 4):
            id_.append(self.team['team_id' + str(i)].text())
            name_.append(self.team['team_name' + str(i)].text())
            college_.append(self.team['team_college' + str(i)].currentText())
            major_.append(self.team['team_major' + str(i)].currentText())
            gender_.append(self.team['team_gender' + str(i)].currentText())
            begin_time.append(self.input_contest_time_begincomo.date().toString(Qt.ISODate))
            end_time.append(self.input_contest_time_endcomo.date().toString(Qt.ISODate))
            in_time.append(self.input_contest_time_incomo.date().toString(Qt.ISODate))
            teacher_.append(self.input_contest_teacher_name.currentText())
            contest_.append(self.input_contest_class.currentText())
            class_.append(self.team['team_price' + str(i)].currentText())
        for i in range (3):
            self.query.execute("insert into sducontest(id, name, college, major, gender, begin_time, end_time, in_time, teacher, \
                contest, price) values(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")" \
                .format(id_[i], name_[i], college_[i], major_[i], gender_[i], begin_time[i], \
                end_time[i], in_time[i], teacher_[i], contest_[i], class_[i]))
            self.db.commit()
            # 显示时行数自增 保证每次添加都追加都上次添加的后面
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 0, QTableWidgetItem(id_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 1, QTableWidgetItem(name_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 2, QTableWidgetItem(college_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 3, QTableWidgetItem(major_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 4, QTableWidgetItem(gender_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 5, QTableWidgetItem(begin_time[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 6, QTableWidgetItem(end_time[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 7, QTableWidgetItem(in_time[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 8, QTableWidgetItem(teacher_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 9, QTableWidgetItem(contest_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 10, QTableWidgetItem(class_[i]))
            self.input_contest_row_count += 1

    # 录入信息标签页的录入比赛标签
    def change_major(self):
        """
        必须先选择学院 才能选择专业。修改学院后，调用此函数查询对应的专业 并添加到combox中 使专业与学院对应
        返回 majors 是学院对应的所有专业
        """
        sender = self.sender()
        college_ = sender.currentText()
        self.query.execute("select major_name from major where college_name = \"{}\"".format(college_))
        majors = self.query.fetchall()
        return majors

    def change_major3(self):
        """
        第三个队员的学院改变时查询对应的专业
        clear 是清除上次的查询结果 只捕获当前的查询内容即可
        """
        self.team["team_major3"].clear()
        majors = self.change_major()
        for major_name in majors:
            major_ = str(major_name[0])
            self.team["team_major3"].addItem(major_)

    # 同上 查询第二个队员的专业
    def change_major2(self):       
        self.team["team_major2"].clear() 
        majors = self.change_major()
        for major_name in majors:
            major_ = str(major_name[0])
            self.team["team_major2"].addItem(major_)

    # 同上 查询第一个队员的专业
    def change_major1(self):
        majors = self.change_major()
        self.team["team_major1"].clear()
        for major_name in majors:
            major_ = str(major_name[0])
            self.team["team_major1"].addItem(major_)
        
    # 信息管理页面的删除学院专业信息
    def del_college_major(self):
        """
        todo: （应该设置为可编辑，然后更新，而不是删除后再次输入）
        输入： item获取当前项的内容 pos根据位置判断当前项是学院还是专业。选择空行提示无效。
        响应： 学院删除后展示学院 专业删除后展示专业。
        """
        item = self.table['colleage_major_twoside'].currentItem()
        pos = self.table['colleage_major_twoside'].currentColumn()
        try:
            info = item.text()
            if pos == 0:
                self.query.execute("delete from college where name = \"{}\"".format(info))
                self.db.commit()
                self.show_college(self.table['colleage_major_twoside'])
            if pos == 1:
                self.query.execute("delete from major where major_name = \"{}\"".format(info))
                self.db.commit()
                self.show_major()
        # 清空
        except:
            QMessageBox.information(None, ("友情提示"), ("请不要选择空行"), QMessageBox.Cancel)

    # 信息管理页面的管理学院和专业标签
    def enable_colleage_major_input_btn(self):
        """
        只有当学院或专业发生改变时才能输入 否则不能输入
        """
        self.colleage_major_input_btn.setEnabled(True)

    # 信息管理页面的管理学院和专业标签
    def insert_college_major(self):
        """
        输入：学院名和专业名
        响应：如果学院不为空 插入对应的学院名和专业名。否则提示：不选择学院无法输入 
        """
        college_name = self.colleage_major_info_college.text()
        major_name = self.colleage_major_info_major.text()
        if major_name != "":
            self.query.execute("insert into major values(\"{}\", \"{}\")".format(major_name, college_name))
        elif major_name == "":
            QMessageBox.information(None, ("友情提示"), ("输入专业前请选择学院"), QMessageBox.Cancel)
        self.db.commit()
        self.show_college(self.table['colleage_major_twoside'])
        self.show_major()
        self.colleage_major_input_btn.setEnabled(False)

    # 信息管理学院专业管理标签下 显示专业
    def show_major(self):
        """
        pos 根据位置判断当前输入的为学院还是专业
        若是学院 在显示学院对应的专业前将专业栏清空 然后才显示 否则不响应
        """
        pos = self.table['colleage_major_twoside'].currentColumn()
        if pos == 0:
            for i in range(self.major_count + 1):
                item = QTableWidgetItem("")
                self.table['colleage_major_twoside'].setItem(i, 1, item)
        item = self.table['colleage_major_twoside'].currentItem()
        try:
            college_info = item.text()
            self.query.execute("select major_name from major where college_name = \"{}\"".format(college_info))
            rows = self.query.fetchall()
            for row in rows:
                inx = rows.index(row)
                # 记录当前的专业数 用于下次的清空
                self.major_count = inx
                major_name = QTableWidgetItem(row[0])
                self.table['colleage_major_twoside'].setItem(inx, 1, major_name)            
        # 空行对应的学院无法显示专业
        except:
            QMessageBox.information(None, ("友情提示"), ("请不要选择空行，无法显示专业"), QMessageBox.Cancel)

    # 信息管理页面下学院专业管理标签
    # 录入信息中的录入比赛标签
    def show_college(self, a):
        """
        如果是信息管理页面 则是 Qtablewidget对象 此时设置为在表格中显示
        如果是录入信息界面 则是 Qcombobox对象 此时设置为将学院添加至下拉框中
        """
        self.query.execute("select * from college")
        rows = self.query.fetchall()
        self.pattern = re.compile("'(.*)'")
        # 录入信息界面调用
        if isinstance(a, QComboBox):
            a.setItemDelegate(self.delegate)
            for row in rows:
                i = self.pattern.findall(str(row))
                a.addItem(i[0])
        # 信息管理界面调用
        if isinstance(a, QTableWidget):
            for row in rows:
                inx = rows.index(row)
                college_name = QTableWidgetItem(row[0])
                self.table['colleage_major_twoside'].setItem(inx, 0, college_name)

    # 录入比赛中的教师信息
    def insert_teacher_comobo(self, a):
        """
        通过下拉列表选择教师（有工号，保证教师唯一） 
        """
        self.query.execute("select * from teacher")
        rows = self.query.fetchall()
        a.setItemDelegate(self.delegate)
        for row in rows:
            item = str(row[0]) + "--" + str(row[2])
            a.addItem(item)

    #　信息查询页面的按比赛查询
    def draw_one_year(self):
        """
        输入：选择内容为某一年 没选择比赛
        输出：选择年份下 今年全部参赛的人数走势图
        """
        # pass
        self.mpl.plot_time()

    # 信息查询页面的按比赛查询
    def draw_all_year(self):
        """
        输入：选择一个比赛 不选择年份
        输出：这个比赛的历史参赛人数走势图
        """
        # pass
        self.mpl.plot_time()

    # 信息录入界面下的建模园地标签
    def del_friend_table(self):
        """
        选中要删除的内容 点击删除 会按照 url（主键） 在数据库中删除
        不用加入判断是否有没有 如果没有则不会显示。因为都是查询数据库后才能显示出来
        """
        row_num = -1
        for i in self.table['input_friend_table'].selectionModel().selection().indexes():
            row_num = i.row()
        if self.table['input_friend_table'].item(row_num, 0):
            del_id = self.table['input_friend_table'].item(row_num, 1).text()
            # 只在视图中删除
            self.table['input_friend_table'].removeRow(row_num)
            # 在数据库中删除
            self.query.execute("delete from sdublog where url = '%s'" % del_id)
            self.db.commit()
            QMessageBox.information(None, ("友情提示"), ("删除完毕"), QMessageBox.Ok)
        self.show_firend_table()

    # 信息录入界面下的建模园地标签
    def show_firend_table(self):
        """
        配合 del_friend_table 函数和 insert_stublog 函数，必须在两个函数执行之前执行
        只有先显示出来，才能选择并删除
        """
        self.query.execute("select * from sdublog")
        rows = self.query.fetchall()
        for row in rows:
            inx = rows.index(row)
            name = QTableWidgetItem(row[0])
            self.table['input_friend_table'].setItem(inx, 0, name)
            info_ = QTableWidgetItem(row[1])
            self.table['input_friend_table'].setItem(inx, 1, info_)

    # 信息录入界面下的建模园地标签
    def insert_stublog(self):
        """
        输入：姓名 网址(主键 不可重复) 年级 专业(自由输入) 个性签名 最高奖
        且域名为空不可插入。插入到数据库后并在表格中显示。
        """
        name = self.input_friend_name.text()
        url = self.input_friend_url.text()
        # 可以避免设置按钮可用不可用 麻烦 
        if url == "":
            QMessageBox.information(None, ("友情提示"), ("网址不可为空"), QMessageBox.Ok)
        else:
            grade = str(self.input_friend_class.value())
            sign = self.input_friend_sign.text()
            price = self.input_friend_price.text()
            self.query.execute("INSERT INTO sdublog VALUES(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".
                format(name, url, grade, sign, price))
            self.db.commit()
            # 在表格中显示 可视化
            self.show_firend_table()
            # 因为设置的为先显示表格，所以可以已有数据，是否和已有的网址重复
            self.input_friend_url.setPlaceholderText("重新插入时域名不可空，不可和已有的重复")

    # 信息管理页面的竞赛管理标签
    def show_contest(self):
        """
        在当前标签页下的表格中展示所有的竞赛
        todo: 所有涉及竞赛的地方均加入
        """
        self.query.execute("select * from contest")
        rows = self.query.fetchall()
        for row in rows:
            # print(row)
            inx = rows.index(row)
            column = 0
            for i in row:
                item = QTableWidgetItem(i)
                self.table['contest_info_table'].setItem(inx, column, item)
                column = column + 1

    # 信息管理页面的竞赛管理标签
    def process_contest(self):
        """
        如果点击的按钮是输入比赛 则输入 并展示结果
        如果点击的按钮是删除比赛 则删除 并展示结果
        """
        sender = self.sender()
        text = sender.text()
        if text == '输入比赛':
            sponsor = self.contest_input_sponsor_line.text()
            class_ = self.contest_input_class_line.text()
            id_ = self.contest_input_id_line.text()
            self.query.execute("INSERT INTO contest VALUES(\"{}\", \"{}\", \"{}\")".format(sponsor, class_, id_))
            self.db.commit()
            self.show_contest()
        if text == '删除比赛':
            row_num = -1
            for i in self.table['contest_info_table'].selectionModel().selection().indexes():
                row_num = i.row()
            if self.table['contest_info_table'].item(row_num, 0):
                del_id = self.table['contest_info_table'].item(row_num, 2).text()
                # 在数据库中删除
                self.query.execute("delete from contest where id = '%s'" % del_id)
                self.db.commit()
                QMessageBox.information(None, ("友情提示"), ("删除完毕"), QMessageBox.Ok)
                self.show_contest()
        
    # 信息管理页面的教师信息管理
    def delete_teacher_info(self):
        """
        表格中选中教师的信息 按照工号进行删除
        """
        row_num = -1
        for i in self.table['teacher_table'].selectionModel().selection().indexes():
            row_num = i.row()
        if self.table['teacher_table'].item(row_num, 0):
            del_id = self.table['teacher_table'].item(row_num, 2).text()
            # 视图中移除
            self.table['teacher_table'].removeRow(row_num)
            # 在数据库中删除
            self.query.execute("delete from teacher where id = '%s'" % del_id)
            self.db.commit()
            QMessageBox.information(None, ("友情提示"), ("删除完毕"), QMessageBox.Ok)
        self.show_teacher()

    # 信息管理页面的教师信息管理
    def show_teacher(self):
        """
        在当前页面的表格内展示教师信息
        todo：所有涉及教师的地方都载入此函数
        """
        self.query.execute("select * from teacher")
        rows = self.query.fetchall()
        for row in rows:
            # print(row)
            inx = rows.index(row)
            column = 0
            for i in row:
                item = QTableWidgetItem(i)
                self.table['teacher_table'].setItem(inx, column, item)
                column = column + 1

    # 信息管理页面的教师信息管理
    def input_teacher_info(self):
        """
        插入教师信息 插入完毕后调用 show_teacher 函数完成显示
        此外还要关联到 查询界面 和 信息录入界面
        """
        name = self.teacher_input_name_line.text()
        college = self.teacher_input_college_como.currentText()
        id = self.teacher_input_id_line.text()
        self.query.execute("INSERT INTO teacher VALUES(\"{}\", \"{}\", \"{}\")".format(name, college, id))
        self.db.commit()
        self.show_teacher()
        # 关联查询界面的教师信息
        self.insert_contest_combo(self.output_year_comobo)
        # 关联录入界面的教师信息
        self.insert_contest_combo(self.input_contest_class)

    # 信息管理界面下的账号管理标签
    def del_admin(self):
        """
        用于删除用不到的管理员的帐号
        wuyuhang的超级管理员帐号不能被删除
        """
        row_num = -1
        for i in self.table['registor_table'].selectionModel().selection().indexes():
            row_num = i.row()
        if self.table['registor_table'].item(row_num, 0):
            del_id = self.table['registor_table'].item(row_num, 0).text()
            if del_id != "wuyuhang@admin":
                # 只在视图中删除
                self.table['registor_table'].removeRow(row_num)
                # 在数据库中删除
                self.query.execute("delete from admin where id = '%s'" % del_id)
                self.db.commit()
                QMessageBox.information(None, ("友情提示"), ("删除完毕"), QMessageBox.Ok)
            else:
                QMessageBox.information(None, ("友情提示"), ("此帐号不能删除"), QMessageBox.Ok)

    # 信息管理界面下的账号管理标签
    def insert_admin(self):
        """
        给竞赛部或信息部注册普通管理员帐号
        验证密码：两次输入的密码一直才能注册 注册即插入到数据库中
        且密码以md5加密的形式存放到数据库中 防止密码泄漏
        """
        in_id = self.registor_id.text()
        psd = self.registor_psd.text()
        confirm_psd = self.registor_confirm.text()
        ls = []
        for row in self.query.execute("select id from admin where id = '%s'" % in_id):
            ls.append(row)
        if len(ls) != 0:
            QMessageBox.information(None, ("友情提示"), ("此账号已经注册过，请重新注册"), QMessageBox.Cancel)
        elif psd != confirm_psd:
            QMessageBox.information(None, ("友情提示"), ("两次输入的密码不一致"), QMessageBox.Cancel)
        else:
            # 加入密码不为空的逻辑判断
            if psd == confirm_psd and in_id != "" and psd != "":
                # 密码加密插入到数据库中
                if self.query.execute("INSERT INTO admin VALUES(\"{}\", \"{}\")".format(in_id, 
                        hashlib.md5(psd.encode('utf-8')).hexdigest())):
                    QMessageBox.information(None, ("友情提示"), ("注册成功"), QMessageBox.Ok)
                    self.db.commit()
                else:
                    QMessageBox.information(None, ("友情提示"), ("注册失败"), QMessageBox.Cancel)
        self.show_admin()

    # 登录界面
    def confirm_password(self):
        """
        连接数据库验证密码是否正确 密码不正确无法登录
        验证密码时 密码也需要md5加密后才能验证和数据库内存储的是否相同
        如验证为超级管理员 则开放信息管理界面 和 录入信息界面
        若验证为普通管理员 不开放信息管理界面 只开放录入信息界面
        """
        self.registor_btn.setEnabled(False)
        in_userid = self.user_line.text()
        in_psd = hashlib.md5(self.password_line.text().encode('utf-8')).hexdigest()
        # 超级管理员
        # self.query.execute("SELECT * FROM admin ")
        self.query.execute("SELECT * FROM admin WHERE id = '%s'" % in_userid)
        info = self.query.fetchall()
        if info:
            # 超级管理员
            if self.user_line.text() == 'wuyuhang@admin':
                if in_psd == info[0][1]:
                    self.registor_btn.setEnabled(True)
                    self.input_btn.setEnabled(True)
                else:
                    QMessageBox.information(None, ("友情提示"), ("密码输入错误"), QMessageBox.Cancel)
            # 普通管理员
            else:
                if in_psd == info[0][1]:
                    self.input_btn.setEnabled(True)
                else:
                    QMessageBox.information(None, ("友情提示"), ("密码输入错误"), QMessageBox.Cancel)

    # 确认身份界面
    def change_status(self):
        """
        游客身份：登录 信息管理 录入信息界面全部关闭
        管理身份：只开放登录界面
        """
        if self.radio_btn_user.isChecked():
            self.user_btn.setEnabled(False)
            self.registor_btn.setEnabled(False)
            self.input_btn.setEnabled(False)
        else:
            self.user_btn.setEnabled(True)

    # 查询信息页面的大小设置
    def show_output(self):
        self.setFixedSize(1800, 1000)
        self.center()
        self.right_layout.setCurrentIndex(5)
        self.insert_contest_combo(self.output_year_comobo)

    # 输入信息页面
    def show_input(self):
        """
        占用面积大 所以全屏 并 加载表格 
        """
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width(), screen.height())
        self.center()
        self.right_layout.setCurrentIndex(4)
        # 初始化录入博客的表格
        self.init_table('input_friend_table')
        # 初始化 录入比赛的表格
        self.init_table('input_contest_info_table')
        self.show_firend_table()
        self.insert_contest_combo(self.input_contest_class)

    # 按钮点击 切换页面时的调用 
    def init(self):
        """
        重新初始化当前页面的大小
        注意先后顺序，resize　在前面会使代码无效
        """
        # 得提前设置这两个
        self.splitter1.setMinimumWidth(150)
        self.splitter2.setMinimumWidth(250)
        self.setFixedSize(600, 400)

    # 建模园地界面
    def show_firend_web(self):
        """
        TreeView 的点击事件 webengine 容易崩溃 需要调系统浏览器
        浏览器打开选中的网址
        """
        item = self.friend_tree.currentItem()
        # 因当前项是姓名和网址的结合 需要以空格分割取出网址
        url = item.text(1).split("  ")[1]
        # 加逻辑判断
        if url[:4] == "http":
            webbrowser.open(url)

    # 建模园地界面
    def show_friend_page(self):
        """
        连接数据库(只连接一次) 查询学生的年级 并按照年级构造树的结构 即16级放在一起 17级放在一起
        查询数据库时：查询所有的年级分布 创建根节点
        查询所有的学生 按年级划分到对应的根节点并加入
        """
        self.right_layout.setCurrentIndex(3)
        self.init()
        self.setFixedSize(960, 650)
        self.center()
        self.page_count += 1
        if self.page_count == 2:
            # 加载博客的数据库
            self.query.execute("SELECT DISTINCT grade FROM sdublog")
            rows = self.query.fetchall()
            ls = []
            for j in rows:
                ls.append(str(j[0]))
                locals() ['child_' + str(j[0])] = QTreeWidgetItem(self.friend_tree)
                locals() ['child_' + str(j[0])].setText(0, str(j[0]) + '级')
            self.query.execute("select * from sdublog")
            rows = self.query.fetchall()
            key = 0
            string = ""
            for row in rows:
                locals() ['child_' + str(row[2]) + '_' + str(key)] = QTreeWidgetItem(locals() ['child_' + str(row[2])])
                for j in row:
                    # 不同项之间加入空格 美化显示
                    if str(j) not in ls:
                        string += (str(j) + '  ')
                locals() ['child_' + str(row[2]) + '_' + str(key)].setText(1, string)
                key += 1
                string = ""

    # 信息管理的页面 
    def show_register_page(self):
        """
        多次点击只被加载一次 否则会有段错误
        此页面被加载时显示 普通管理员管理 学院专业管理 教师信息管理 和 竞赛管理
        """
        self.init()
        self.setFixedSize(1000, 700)
        self.center()
        self.right_layout.setCurrentIndex(2)
        if self.show_register_page_count == 0:
            self.show_register_page_count += 1
            # 初始化普通管理员表格
            self.init_table('registor_table')
            # 初始化教师管理表格 并显示
            self.init_table('teacher_table')
            self.show_teacher()
            # 初始化学院专业管理表格
            self.init_table('colleage_major_twoside')
            # 初始化竞赛管理的表格
            self.init_table('contest_info_table') 
            # 信息管理页面的学院查询
            self.show_college(self.table['colleage_major_twoside'])
            # 信息管理页面中插入老师时的 选择教师学院
            self.show_college(self.teacher_input_college_como)
            # 展示比赛的信息
            self.show_contest()
            # 展示管理员信息
            self.show_admin()

    # 展示普通管理员
    def show_admin(self):
        self.query.execute("SELECT id FROM admin")
        rows = self.query.fetchall()
        for row in rows:
            # print(row)
            inx = rows.index(row)
            str_re1 = self.pattern.findall(str(row))
            item = QTableWidgetItem(str_re1[0])
            self.table['registor_table'].setItem(inx, 0, item)

    # 显示登录的页面
    def show_login_page(self):
        """
        登录界面下 注册按钮 录入信息 按钮不显示 
        登录密码正确后才能显示
        """
        self.init()
        self.registor_btn.setEnabled(False)
        self.input_btn.setEnabled(False)
        self.right_layout.setCurrentIndex(1)

    # 显示验证身份的页面 
    def show_verifyid_page(self):
        """
        radio button 只能选择一种身份 游客还是管理员
        """
        self.init()
        self.right_layout.setCurrentIndex(0)

    # 退出界面 
    def quit_act(self):
        """
        有信息框的提示　询问是否确认退出
        """
        # sender 是发送信号的对象
        # sender = self.sender()
        # print(sender.text() + '键被按下')
        message = QMessageBox.question(self, ' ', '确认退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            self.db.close()
            qApp = QApplication.instance()
            qApp.quit()

    # 窗口居中函数
    def center(self):
        """
        获取桌面长宽  获取窗口长宽 计算位置 移动
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())