import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入业务逻辑模块
from user.usermanagement import UserManagement
from shop.shopmanagement import ShopManagement


class LoginWindow(QWidget):
    """登录界面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口标题
        self.setWindowTitle("餐饮订餐系统 - 登录")
        
        # 设置固定大小
        self.setFixedSize(400, 350)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)
        
        # 添加标题
        title_label = QLabel("餐饮订餐系统")
        title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建角色选择
        role_layout = QHBoxLayout()
        role_label = QLabel("用户类型：")
        role_label.setFont(QFont("Arial", 12))
        role_label.setFixedWidth(80)
        role_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        role_layout.addWidget(role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["消费者", "店家", "管理员"])
        self.role_combo.setFont(QFont("Arial", 12))
        self.role_combo.setFixedHeight(35)
        self.role_combo.setMinimumWidth(200)
        role_layout.addWidget(self.role_combo)
        main_layout.addLayout(role_layout)
        
        # 创建用户名输入
        username_layout = QHBoxLayout()
        username_label = QLabel("用户名：")
        username_label.setFont(QFont("Arial", 12))
        username_label.setFixedWidth(80)
        username_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        username_layout.addWidget(username_label)
        self.username_edit = QLineEdit()
        self.username_edit.setFont(QFont("Arial", 12))
        self.username_edit.setFixedHeight(35)
        self.username_edit.setMinimumWidth(200)
        username_layout.addWidget(self.username_edit)
        main_layout.addLayout(username_layout)
        
        # 创建密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel("密码：")
        password_label.setFont(QFont("Arial", 12))
        password_label.setFixedWidth(80)
        password_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        password_layout.addWidget(password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFont(QFont("Arial", 12))
        self.password_edit.setFixedHeight(35)
        self.password_edit.setMinimumWidth(200)
        password_layout.addWidget(self.password_edit)
        main_layout.addLayout(password_layout)
        
        # 创建按钮布局
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)
        
        # 注册按钮
        self.register_button = QPushButton("注册")
        self.register_button.setFont(QFont("Arial", 12))
        self.register_button.setFixedHeight(40)
        self.register_button.clicked.connect(self.show_register_window)
        button_layout.addWidget(self.register_button)
        
        main_layout.addLayout(button_layout)
        
        # 设置用户名输入框为焦点
        self.username_edit.setFocus()
    
    def login(self):
        """处理登录逻辑"""
        role = self.role_combo.currentText()
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空！")
            return
        
        try:
            if role == "消费者":
                um = UserManagement()
                user = um.login(username, password)
                if user:
                    QMessageBox.information(self, "成功", f"登录成功！欢迎 {user.name}")
                    self.parent.show_user_menu(user)
                else:
                    QMessageBox.critical(self, "失败", "用户名或密码错误！")
            
            elif role == "店家":
                sm = ShopManagement()
                shop = sm.login(username, password)
                if shop:
                    QMessageBox.information(self, "成功", f"登录成功！欢迎 {shop.name}")
                    self.parent.show_shop_menu(shop)
                else:
                    QMessageBox.critical(self, "失败", "用户名或密码错误！")
            
            elif role == "管理员":
                from manager.managermanagement import ManagerManagement
                mm = ManagerManagement()
                manager = mm.login(username, password)
                if manager:
                    QMessageBox.information(self, "成功", f"登录成功！欢迎 {manager.name} ({manager.role})")
                    self.parent.show_admin_menu(manager)
                else:
                    QMessageBox.critical(self, "失败", "用户名或密码错误！")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"登录过程中发生错误：{str(e)}")
    
    def show_register_window(self):
        """显示注册窗口"""
        role = self.role_combo.currentText()
        if role == "管理员":
            QMessageBox.warning(self, "警告", "管理员不支持注册！")
            return
        
        self.parent.show_register_window(role)


class RegisterWindow(QWidget):
    """注册界面"""
    def __init__(self, role, parent=None):
        super().__init__(parent)
        self.role = role
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle(f"餐饮订餐系统 - {self.role}注册")
        self.setFixedSize(400, 550 if self.role == "消费者" else 650)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)
        
        # 添加标题
        self.title_label = QLabel(f"{self.role}注册")
        self.title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        # 创建表单布局
        form_layout = QVBoxLayout()
        
        # 根据不同角色设置不同的字段标签
        if self.role == "消费者":
            # 消费者注册字段
            name_label = "用户名："
            address_label = "地址："
        else:  # 店家
            # 店家注册字段
            name_label = "店铺名称："
            address_label = "店铺地址："
        
        # 名称/用户名
        name_layout = QHBoxLayout()
        name_label_obj = QLabel(name_label)
        name_label_obj.setFont(QFont("Arial", 12))
        name_label_obj.setFixedWidth(80)
        name_label_obj.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        name_layout.addWidget(name_label_obj)
        self.username_edit = QLineEdit()
        self.username_edit.setFont(QFont("Arial", 12))
        self.username_edit.setFixedHeight(35)
        self.username_edit.setMinimumWidth(200)
        name_layout.addWidget(self.username_edit)
        form_layout.addLayout(name_layout)
        
        # 密码
        password_layout = QHBoxLayout()
        password_label = QLabel("密码：")
        password_label.setFont(QFont("Arial", 12))
        password_label.setFixedWidth(80)
        password_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        password_layout.addWidget(password_label)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFont(QFont("Arial", 12))
        self.password_edit.setFixedHeight(35)
        self.password_edit.setMinimumWidth(200)
        password_layout.addWidget(self.password_edit)
        form_layout.addLayout(password_layout)
        
        # 电话号码
        tel_layout = QHBoxLayout()
        tel_label = QLabel("电话号码：")
        tel_label.setFont(QFont("Arial", 12))
        tel_label.setFixedWidth(80)
        tel_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        tel_layout.addWidget(tel_label)
        self.tel_edit = QLineEdit()
        self.tel_edit.setFont(QFont("Arial", 12))
        self.tel_edit.setFixedHeight(35)
        self.tel_edit.setMinimumWidth(200)
        tel_layout.addWidget(self.tel_edit)
        form_layout.addLayout(tel_layout)
        
        # 地址/店铺地址
        address_layout = QHBoxLayout()
        address_label_obj = QLabel(address_label)
        address_label_obj.setFont(QFont("Arial", 12))
        address_label_obj.setFixedWidth(80)
        address_label_obj.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        address_layout.addWidget(address_label_obj)
        self.address_edit = QLineEdit()
        self.address_edit.setFont(QFont("Arial", 12))
        self.address_edit.setFixedHeight(35)
        self.address_edit.setMinimumWidth(200)
        address_layout.addWidget(self.address_edit)
        form_layout.addLayout(address_layout)
        
        # 邮箱
        email_layout = QHBoxLayout()
        email_label = QLabel("邮箱：")
        email_label.setFont(QFont("Arial", 12))
        email_label.setFixedWidth(80)
        email_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        email_layout.addWidget(email_label)
        self.email_edit = QLineEdit()
        self.email_edit.setFont(QFont("Arial", 12))
        self.email_edit.setFixedHeight(35)
        self.email_edit.setMinimumWidth(200)
        email_layout.addWidget(self.email_edit)
        form_layout.addLayout(email_layout)
        
        # 店家特有字段
        if self.role == "店家":
            # 营业执照号
            license_layout = QHBoxLayout()
            license_label = QLabel("营业执照号：")
            license_label.setFont(QFont("Arial", 12))
            license_label.setFixedWidth(80)
            license_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            license_layout.addWidget(license_label)
            self.license_edit = QLineEdit()
            self.license_edit.setFont(QFont("Arial", 12))
            self.license_edit.setFixedHeight(35)
            self.license_edit.setMinimumWidth(200)
            license_layout.addWidget(self.license_edit)
            form_layout.addLayout(license_layout)
            
            # 店铺类型
            type_layout = QHBoxLayout()
            type_label = QLabel("店铺类型：")
            type_label.setFont(QFont("Arial", 12))
            type_label.setFixedWidth(80)
            type_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            type_layout.addWidget(type_label)
            self.type_combo = QComboBox()
            self.type_combo.addItems(["中餐", "西餐", "快餐", "火锅", "烧烤", "甜点", "饮品", "其他"])
            self.type_combo.setFont(QFont("Arial", 12))
            self.type_combo.setFixedHeight(35)
            self.type_combo.setMinimumWidth(200)
            type_layout.addWidget(self.type_combo)
            form_layout.addLayout(type_layout)
            
            # 营业时间
            hours_layout = QHBoxLayout()
            hours_label = QLabel("营业时间：")
            hours_label.setFont(QFont("Arial", 12))
            hours_label.setFixedWidth(80)
            hours_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            hours_layout.addWidget(hours_label)
            self.hours_edit = QLineEdit()
            self.hours_edit.setFont(QFont("Arial", 12))
            self.hours_edit.setFixedHeight(35)
            self.hours_edit.setMinimumWidth(200)
            self.hours_edit.setPlaceholderText("例如：10:00-22:00")
            hours_layout.addWidget(self.hours_edit)
            form_layout.addLayout(hours_layout)
        
        main_layout.addLayout(form_layout)
        
        # 创建按钮布局
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        # 创建注册按钮
        self.register_button = QPushButton("注册")
        self.register_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.register_button.setFixedHeight(40)
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)
        
        # 创建返回按钮
        self.back_button = QPushButton("返回")
        self.back_button.setFont(QFont("Arial", 12))
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.back_to_login)
        button_layout.addWidget(self.back_button)
        
        main_layout.addLayout(button_layout)
    
    def back_to_login(self):
        """返回登录界面"""
        self.parent.show_login_window()
    
    def register(self):
        """处理注册逻辑"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        telphone = self.tel_edit.text().strip()
        address = self.address_edit.text().strip()
        email = self.email_edit.text().strip()
        
        if not username or not password or not telphone or not address or not email:
            QMessageBox.warning(self, "警告", "所有字段都不能为空！")
            return
        
        try:
            if self.role == "消费者":
                um = UserManagement()
                success = um.register(username, password, telphone, address, email)
                if success:
                    QMessageBox.information(self, "成功", "注册成功！")
                    self.parent.show_login_window()
                else:
                    QMessageBox.critical(self, "失败", "注册失败！用户名可能已存在")
            
            elif self.role == "店家":
                business_license = self.license_edit.text().strip()
                shop_type = self.type_combo.currentText()
                business_hours = self.hours_edit.text().strip()
                
                if not business_license:
                    QMessageBox.warning(self, "警告", "营业执照号不能为空！")
                    return
                
                if not business_hours:
                    QMessageBox.warning(self, "警告", "营业时间不能为空！")
                    return
                
                sm = ShopManagement()
                success = sm.register(username, password, telphone, address, email, business_license, shop_type, business_hours)
                if success:
                    QMessageBox.information(self, "成功", "注册成功！")
                    self.parent.show_login_window()
                else:
                    QMessageBox.critical(self, "失败", "注册失败！店铺名称或营业执照号可能已存在")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"注册过程中发生错误：{str(e)}")
