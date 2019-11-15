import sys
import qdarkstyle
import numpy as np
from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton, 
                            QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,
                            QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QRadioButton,
                            QTreeWidgetItem, QDesktopWidget, QTabWidget, QSpinBox, QComboBox,
                            QCalendarWidget, QDateTimeEdit, QMessageBox)
from PyQt5.QtCore import Qt, QUrl, QDate
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # 设置窗口的名称
        self.setWindowTitle("某个学校数学建模协会比赛查询")

        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("我在主页面～")

        # 设置初始化的窗口大小
        self.setFixedSize(600, 400)

        # 设置初始化的窗口位置
        self.center()

        # 设置窗口透明度
        self.setWindowOpacity(0.9) # 设置窗口透明度

        # 设置窗口样式
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 设置整体布局 左右显示
        pagelayout = QGridLayout()

        # 左侧开始布局
        # 创建左侧部件
        top_left_frame = QFrame(self)  
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        #　左边按钮为垂直布局
        button_layout = QVBoxLayout(top_left_frame)

        # 登录按钮
        verifyid_btn = QPushButton(top_left_frame)
        verifyid_btn.setFixedSize(100, 30), verifyid_btn.setText("确认身份")
        button_layout.addWidget(verifyid_btn)
        # 输入用户名　密码按钮
        # 因为在radiobutton中需要选择来确定某些按钮是否可用，所以，设置为self方便子函数的调用
        self.user_btn = QPushButton(top_left_frame)
        self.user_btn.setFixedSize(100, 30), self.user_btn.setText("登录")
        button_layout.addWidget(self.user_btn)
        # 申请账号　按钮
        self.registor_btn = QPushButton(top_left_frame)
        self.registor_btn.setFixedSize(100, 30), self.registor_btn.setText("申请帐号")
        button_layout.addWidget(self.registor_btn)
        # 录入信息按钮
        self.input_btn = QPushButton(top_left_frame)
        self.input_btn.setFixedSize(100, 30), self.input_btn.setText("录入信息")
        button_layout.addWidget(self.input_btn) 
        # 查询按钮
        query_btn = QPushButton(top_left_frame)
        query_btn.setFixedSize(100, 30), query_btn.setText("查询信息")
        button_layout.addWidget(query_btn) 
        # 建模之家　按钮
        friend_btn = QPushButton(top_left_frame)
        friend_btn.setFixedSize(100, 30), friend_btn.setText("建模园地")
        button_layout.addWidget(friend_btn) 
        # 个人控件　按钮
        space_btn = QPushButton(top_left_frame)
        space_btn.setFixedSize(100, 30), space_btn.setText("个人空间")
        button_layout.addWidget(space_btn)      
        # 退出按钮
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(100, 30), quit_btn.setText("退出")
        button_layout.addWidget(quit_btn)
        
        # 左下角为博客 必须要有布局，才可以显示至内容中
        bottom_left_frame = QFrame(self)
        blank_label = QLabel(bottom_left_frame)
        blank_layout = QVBoxLayout(bottom_left_frame)
        blank_label.setText("建模学子的博客")
        blank_label.setFixedHeight(20)
        blank_layout.addWidget(blank_label)
        self.webEngineView = QWebEngineView(bottom_left_frame)
        self.webEngineView.close()
        blank_layout.addWidget(self.webEngineView)
        
        # 右侧开始布局 对应按钮布局
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # 右边显示为stack布局
        self.right_layout = QStackedLayout(right_frame)

        # 确认身份
        # 管理员身份
        self.radio_btn_admin = QRadioButton(right_frame)
        self.radio_btn_admin.setText("我是管理员，来输入数据的")
        # 游客身份
        self.radio_btn_user = QRadioButton(right_frame)
        self.radio_btn_user.setText("我是游客，就来看看")
        # 以垂直布局管理器管理
        # 这里没必要在传入frame，已经有布局了
        radio_btn_layout = QVBoxLayout()  
        radio_btn_widget = QWidget(right_frame)
        radio_btn_layout.addWidget(self.radio_btn_admin)
        radio_btn_layout.addWidget(self.radio_btn_user)
        radio_btn_widget.setLayout(radio_btn_layout)
        self.right_layout.addWidget(radio_btn_widget)

        # 登录界面
        self.user_line = QLineEdit(right_frame)
        self.user_line.setPlaceholderText("输入账号：")
        self.user_line.setFixedWidth(400)
        self.password_line = QLineEdit(right_frame)
        self.password_line.setPlaceholderText("请输入密码：")
        self.password_line.setFixedWidth(400)
        login_layout = QVBoxLayout()
        login_btn_layout = QHBoxLayout()
        login_btn_cancel = QPushButton("取消")
        login_btn_cancel.setFixedWidth(80)
        login_btn_confirm = QPushButton("确认")
        login_btn_confirm.setFixedWidth(80)
        login_btn_layout.addWidget(login_btn_cancel)
        login_btn_layout.addWidget(login_btn_confirm)
        login_widget = QWidget(right_frame)
        login_widget.setLayout(login_layout)
        login_layout.addWidget(self.user_line)
        login_layout.addWidget(self.password_line)
        login_layout.addLayout(login_btn_layout)
        # 添加至右侧的layout布局
        self.right_layout.addWidget(login_widget)

        # 申请帐号
        registor_id = QLineEdit(right_frame)
        registor_id.setPlaceholderText("请输入新帐号：")
        registor_id.setFixedWidth(400)
        registor_psd = QLineEdit(right_frame)
        registor_psd.setPlaceholderText("请输入密码：")
        registor_psd.setFixedWidth(400)
        registor_confirm = QLineEdit(right_frame)
        registor_confirm.setPlaceholderText("请确认密码：")
        registor_confirm.setFixedWidth(400)
        registor_confirm_btn = QPushButton("确认提交")
        registor_confirm_btn.setFixedSize(100, 30)
        registor_layout = QVBoxLayout()
        register_widget = QWidget(right_frame)
        register_widget.setLayout(registor_layout)
        registor_layout.addWidget(registor_id)
        registor_layout.addWidget(registor_psd)
        registor_layout.addWidget(registor_confirm)
        registor_layout.addWidget(registor_confirm_btn)
        self.right_layout.addWidget(register_widget)

        # 建模园地 使用 TreeView　水平布局，不能和webengine设置在一起　
        # 应该读取数据库
        self.friend_tree = QTreeWidget(right_frame)
        self.friend_tree.setColumnCount(3)  # 三列 
        # 设置标题
        self.friend_tree.setHeaderLabels(['年级', '人员', '友情链接']) 
        root = QTreeWidgetItem(self.friend_tree) # 设置根节点
        self.friend_tree.setColumnWidth(2, 400) # 设置宽度
        # 设置子节点
        root.setText(0, "年级") # 0 表示位置
        root.setText(1, "姓名")
        root.setText(2, "网址")
        child_16 = QTreeWidgetItem(root)
        child_16.setText(0, "16级")

        child_ljw = QTreeWidgetItem(child_16)
        child_ljw.setText(1, "Name1")
        child_ljw.setText(2, "https://muyuuuu.github.io")

        child_17 = QTreeWidgetItem(root)
        child_17.setText(0, "17级")

        child_lqr = QTreeWidgetItem(child_17)
        child_lqr.setText(1, "Name2")
        child_lqr.setText(2, "https://dgimoyeran.github.io")

        friend_widget = QWidget(right_frame)
        friend_layout = QVBoxLayout()
        friend_widget.setLayout(friend_layout)
        friend_layout.addWidget(self.friend_tree)
        self.right_layout.addWidget(friend_widget)

        self.url = ''  #　后期会获取要访问的url

        # 录入信息
        # 录入信息为多个水平布局，最后垂直布局
        input_tab = QTabWidget(right_frame)
        self.right_layout.addWidget(input_tab)
        # 录入信息中的建模园地
        input_friend_widget = QWidget(right_frame)
        input_friend_layout = QVBoxLayout()
        input_friend_name = QLineEdit()
        input_friend_name.setPlaceholderText("请输入姓名")
        input_friend_url = QLineEdit()
        input_friend_url.setPlaceholderText("请输入网址")
        input_friend_label = QLabel("请选择年级")
        input_friend_label.setMaximumHeight(20)
        input_friend_class = QSpinBox()
        input_friend_class.setMinimum(2013)
        input_friend_class.setMaximum(3000)
        input_friend_class.setValue(2020)
        input_friend_layout.addWidget(input_friend_name)
        input_friend_layout.addWidget(input_friend_url)
        input_friend_layout.addWidget(input_friend_label)
        input_friend_layout.addWidget(input_friend_class)
        input_friend_widget.setLayout(input_friend_layout)
        input_tab.addTab(input_friend_widget, "建模园地")

        # 录入信息中的录入比赛
        input_contest_widget = QWidget(right_frame)
        # 第一个水平布局，选择比赛
        input_contest_layout = QVBoxLayout()
        input_contest_widget.setLayout(input_contest_layout)
        input_contest_label = QLabel("请选择比赛")
        input_contest_label.setFixedHeight(30)
        input_contest_class = QComboBox()
        input_contest_layout.addWidget(input_contest_label)
        input_contest_layout.addWidget(input_contest_class)
        # 第二个水平布局，选择比赛的起止时间
        input_contest_time_layout = QHBoxLayout()
        input_contest_time_begin = QLabel("开始时间")
        input_contest_time_begincomo = QDateTimeEdit()
        input_contest_time_begincomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        input_contest_time_begincomo.setCalendarPopup(True)
        # input_contest_time_begincomo.setFixedWidth(250)
        input_contest_time_end = QLabel("结束时间")
        input_contest_time_endcomo = QDateTimeEdit()
        input_contest_time_endcomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        input_contest_time_endcomo.setCalendarPopup(True)
        input_contest_time_layout.addWidget(input_contest_time_begin)
        input_contest_time_layout.addWidget(input_contest_time_begincomo)
        input_contest_time_layout.addWidget(input_contest_time_end)
        input_contest_time_layout.addWidget(input_contest_time_endcomo)
        input_contest_layout.addLayout(input_contest_time_layout)
        input_tab.addTab(input_contest_widget, "录入比赛")
        # 第三个水平布局，输入指导教师
        input_contest_teacher_layout = QHBoxLayout()
        input_contest_teacher_label = QLabel("指导教师")
        input_contest_teacher_college = QComboBox()
        input_contest_teacher_name = QLineEdit()
        input_contest_teacher_name.setPlaceholderText("请输入教师姓名")
        input_contest_teacher_layout.addWidget(input_contest_teacher_label)
        input_contest_teacher_layout.addWidget(input_contest_teacher_college)
        input_contest_teacher_layout.addWidget(input_contest_teacher_name)
        input_contest_layout.addLayout(input_contest_teacher_layout)

        for team in range(3):
            input_contest_team_layout = QHBoxLayout()
            input_contest_team_label = QLabel()
            string = "队员" + str(team + 1)
            input_contest_team_label.setText(string)
            input_contest_team_como = QComboBox()
            input_contest_team_name = QLineEdit()
            input_contest_team_name.setPlaceholderText("请输入队员姓名")
            input_contest_team_class_label = QLabel("请选择年级")
            input_contest_team_class = QSpinBox()
            input_contest_team_class.setMinimum(2013)
            input_contest_team_class.setMaximum(3000)
            input_contest_team_class.setValue(2020)
            input_contest_team_layout.addWidget(input_contest_team_label)
            input_contest_team_layout.addWidget(input_contest_team_name)
            input_contest_team_layout.addWidget(input_contest_team_class_label)
            input_contest_team_layout.addWidget(input_contest_team_class)
            input_contest_layout.addLayout(input_contest_team_layout)

        # 查询信息
        output_tab = QTabWidget(right_frame)
        self.right_layout.addWidget(output_tab)
        output_year = QWidget()
        output_teacher = QWidget()
        output_name = QWidget()
        output_college = QWidget()

        output_tab.addTab(output_year, "按时间查询")
        output_tab.addTab(output_teacher, "按教师查询")
        output_tab.addTab(output_name, "按学生查询")
        output_tab.addTab(output_college, "按学院查询")

        # 三分界面，可拖动
        self.splitter1 = QSplitter(Qt.Vertical)
        top_left_frame.setFixedHeight(280)
        self.splitter1.addWidget(top_left_frame)
        self.splitter1.addWidget(bottom_left_frame)
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

        # 函数功能区
        # show corresponing page
        verifyid_btn.clicked.connect(self.show_verifyid_page)
        self.user_btn.clicked.connect(self.show_login_page)
        self.registor_btn.clicked.connect(self.show_register_page)
        friend_btn.clicked.connect(self.show_friend_page)
        self.friend_tree.clicked.connect(self.show_firend_web)
        self.input_btn.clicked.connect(self.show_input)
        quit_btn.clicked.connect(self.quit_act)
        query_btn.clicked.connect(self.show_output)

        # confirm user status to set some button unenable
        self.user_btn.setEnabled(False)
        self.registor_btn.setEnabled(False)
        self.input_btn.setEnabled(False)
        # two radio button connected to change_status function to get user status
        self.radio_btn_user.toggled.connect(self.change_status)
        self.radio_btn_admin.toggled.connect(self.change_status)

    # 设置为只有管理员才能进行登录、申请、输入行为
    def change_status(self):
        if self.radio_btn_user.isChecked():
            self.user_btn.setEnabled(False)
            self.registor_btn.setEnabled(False)
            self.input_btn.setEnabled(False)
        else:
            self.user_btn.setEnabled(True)
            # only super admin can registor new ID
            # self.registor_btn.setEnabled(True)
            # self.input_btn.setEnabled(True)

    # 查询信息的页面
    def show_output(self):
        self.init()
        self.right_layout.setCurrentIndex(5)

    # 输入信息的页面
    def show_input(self):
        self.setFixedSize(750, 600)
        self.right_layout.setCurrentIndex(4)

    def init(self):
        # 刚开始要管理浏览器，否则很丑
        self.webEngineView.close()
        # 注意先后顺序，resize　在前面会使代码无效
        # 得提前设置这两个
        self.splitter1.setMinimumWidth(150)
        self.splitter2.setMinimumWidth(250)
        self.setFixedSize(600, 400)
        self.center()
        # screen = QDesktopWidget().screenGeometry()
        # size = self.geometry()
        # print(size.width())
        # self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # TreeView 的点击事件
    def show_firend_web(self):
        item = self.friend_tree.currentItem()
        if item.text(2)[:4] == "http":
            self.url = item.text(2)
            self.splitter1.setMinimumWidth(1200)
            self.setFixedSize(1800, 1080)
            self.center()
            self.webEngineView.show()
            self.webEngineView.load(QUrl(self.url))

    # 展示树形结构
    def show_friend_page(self):
        self.init()
        self.right_layout.setCurrentIndex(3)

    # 显示注册帐号的页面
    def show_register_page(self):
        self.init()
        self.right_layout.setCurrentIndex(2)

    # 显示登录的页面
    def show_login_page(self):
        self.init()
        self.right_layout.setCurrentIndex(1)

    # stacklayout 布局，显示验证身份的页面
    def show_verifyid_page(self):
        self.init()
        self.right_layout.setCurrentIndex(0)

    # 退出按钮 有信息框的提示　询问是否确认退出
    def quit_act(self):
        # sender 是发送信号的对象
        # sender = self.sender()
        # print(sender.text() + '键被按下')
        message = QMessageBox.question(self, ' ', '确认退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            qApp = QApplication.instance()
            qApp.quit()

    def center(self):
        '''
        获取桌面长宽
        获取窗口长宽
        移动
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())