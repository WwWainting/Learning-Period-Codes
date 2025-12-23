import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QTableWidgetItem, QStackedWidget, QGroupBox, QDialog, QLineEdit, 
    QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入业务逻辑模块
from user.usermanagement import UserManagement
from manager.managermanagement import ManagerManagement
from shop.shopmanagement import ShopManagement

class AdminMenuWindow(QWidget):
    """管理员菜单界面"""
    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle(f"餐饮订餐系统 - 管理员界面")
        self.resize(1000, 600)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建顶部信息栏
        top_layout = QHBoxLayout()
        welcome_label = QLabel(f"欢迎您，{self.manager.name} ({self.manager.role})！")
        welcome_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        top_layout.addWidget(welcome_label)
        top_layout.addStretch()
        
        logout_button = QPushButton("退出登录")
        logout_button.clicked.connect(self.logout)
        top_layout.addWidget(logout_button)
        main_layout.addLayout(top_layout)
        
        # 创建选项卡布局
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # 创建控制面板
        control_layout = QHBoxLayout()
        
        if self.manager.role == "超级管理员":
            # 超级管理员功能
            self.admin_button = QPushButton("管理员管理")
            self.admin_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
            control_layout.addWidget(self.admin_button)
            
            self.user_button = QPushButton("用户管理")
            self.user_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
            control_layout.addWidget(self.user_button)
            
            self.shop_button = QPushButton("店铺管理")
            self.shop_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
            control_layout.addWidget(self.shop_button)
            
            # 管理员管理界面
            self.create_admin_management_page()
        else:
            # 普通管理员功能
            self.user_button = QPushButton("用户管理")
            self.user_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
            control_layout.addWidget(self.user_button)
            
            self.shop_button = QPushButton("店铺管理")
            self.shop_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
            control_layout.addWidget(self.shop_button)
        
        main_layout.insertLayout(1, control_layout)
        
        # 用户管理界面
        self.create_user_management_page()
        
        # 店铺管理界面
        self.create_shop_management_page()
    
    def create_admin_management_page(self):
        """创建管理员管理界面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("管理员列表")
        group_layout = QVBoxLayout(group)
        
        self.admin_table = QTableWidget()
        self.admin_table.setColumnCount(5)
        self.admin_table.setHorizontalHeaderLabels(["ID", "用户名", "角色", "邮箱", "创建时间"])
        self.admin_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        group_layout.addWidget(self.admin_table)
        
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        
        # 加载管理员数据
        self.load_admins()
    
    def create_user_management_page(self):
        """创建用户管理界面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 只有超级管理员可以添加和删除用户
        if self.manager.role == "超级管理员":
            # 创建按钮布局
            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)
            
            # 添加用户按钮
            self.add_user_btn = QPushButton("添加用户")
            self.add_user_btn.setFont(QFont("Arial", 12))
            self.add_user_btn.clicked.connect(self.show_add_user_dialog)
            button_layout.addWidget(self.add_user_btn)
            
            # 删除用户按钮
            self.delete_user_btn = QPushButton("删除用户")
            self.delete_user_btn.setFont(QFont("Arial", 12))
            self.delete_user_btn.clicked.connect(self.show_delete_user_dialog)
            button_layout.addWidget(self.delete_user_btn)
            
            button_layout.addStretch()
            layout.addLayout(button_layout)
        
        group = QGroupBox("用户列表")
        group_layout = QVBoxLayout(group)
        
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["ID", "用户名", "电话", "地址", "邮箱", "注册时间"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        group_layout.addWidget(self.user_table)
        
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        
        # 加载用户数据
        self.load_users()
    
    def show_add_user_dialog(self):
        """显示添加用户对话框"""
        # 创建添加用户对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("添加用户")
        dialog.setFixedSize(400, 400)
        
        # 创建主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(15)
        
        # 用户名
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("用户名："))
        name_edit = QLineEdit()
        name_edit.setFont(QFont("Arial", 12))
        name_layout.addWidget(name_edit)
        main_layout.addLayout(name_layout)
        
        # 密码
        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(QLabel("密码："))
        pwd_edit = QLineEdit()
        pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        pwd_edit.setFont(QFont("Arial", 12))
        pwd_layout.addWidget(pwd_edit)
        main_layout.addLayout(pwd_layout)
        
        # 电话
        tel_layout = QHBoxLayout()
        tel_layout.addWidget(QLabel("电话："))
        tel_edit = QLineEdit()
        tel_edit.setFont(QFont("Arial", 12))
        tel_layout.addWidget(tel_edit)
        main_layout.addLayout(tel_layout)
        
        # 地址
        address_layout = QHBoxLayout()
        address_layout.addWidget(QLabel("地址："))
        address_edit = QLineEdit()
        address_edit.setFont(QFont("Arial", 12))
        address_layout.addWidget(address_edit)
        main_layout.addLayout(address_layout)
        
        # 邮箱
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("邮箱："))
        email_edit = QLineEdit()
        email_edit.setFont(QFont("Arial", 12))
        email_layout.addWidget(email_edit)
        main_layout.addLayout(email_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFont(QFont("Arial", 12))
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        # 确认按钮
        ok_btn = QPushButton("确认")
        ok_btn.setFont(QFont("Arial", 12))
        ok_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_btn)
        
        main_layout.addLayout(button_layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 获取输入数据
            name = name_edit.text().strip()
            pwd = pwd_edit.text().strip()
            telphone = tel_edit.text().strip()
            address = address_edit.text().strip()
            email = email_edit.text().strip()
            
            try:
                # 添加用户
                um = UserManagement()
                success = um.register(name, pwd, telphone, address, email)
                if success:
                    QMessageBox.information(self, "成功", f"用户'{name}'添加成功！")
                    self.load_users()
                else:
                    QMessageBox.warning(self, "失败", "用户添加失败！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"添加用户失败：{str(e)}")
    
    def show_delete_user_dialog(self):
        """显示删除用户对话框"""
        # 获取选中的行
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要删除的用户！")
            return
        
        # 获取当前用户信息
        user_id = self.user_table.item(current_row, 0).text()
        name = self.user_table.item(current_row, 1).text()
        
        # 确认删除
        reply = QMessageBox.question(self, "确认删除", f"确定要删除用户'{name}'吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 删除用户
                um = UserManagement()
                success = um.delete_user(user_id)
                if success:
                    QMessageBox.information(self, "成功", "用户删除成功！")
                    self.load_users()
                else:
                    QMessageBox.warning(self, "失败", "用户删除失败！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除用户失败：{str(e)}")
    
    def create_shop_management_page(self):
        """创建店铺管理界面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 只有超级管理员可以添加和删除店铺
        if self.manager.role == "超级管理员":
            # 创建按钮布局
            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)
            
            # 添加店铺按钮
            self.add_shop_btn = QPushButton("添加店铺")
            self.add_shop_btn.setFont(QFont("Arial", 12))
            self.add_shop_btn.clicked.connect(self.show_add_shop_dialog)
            button_layout.addWidget(self.add_shop_btn)
            
            # 删除店铺按钮
            self.delete_shop_btn = QPushButton("删除店铺")
            self.delete_shop_btn.setFont(QFont("Arial", 12))
            self.delete_shop_btn.clicked.connect(self.show_delete_shop_dialog)
            button_layout.addWidget(self.delete_shop_btn)
            
            button_layout.addStretch()
            layout.addLayout(button_layout)
        
        group = QGroupBox("店铺列表")
        group_layout = QVBoxLayout(group)
        
        self.shop_table = QTableWidget()
        self.shop_table.setColumnCount(9)
        self.shop_table.setHorizontalHeaderLabels(["ID", "店铺名称", "电话", "地址", "邮箱", "营业执照", "店铺类型", "营业时间", "注册时间"])
        self.shop_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        group_layout.addWidget(self.shop_table)
        
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        
        # 加载店铺数据
        self.load_shops()
    
    def load_admins(self):
        """加载管理员数据"""
        try:
            mm = ManagerManagement()
            managers = mm.list_all_managers()
            
            self.admin_table.setRowCount(len(managers))
            for row, manager in enumerate(managers):
                self.admin_table.setItem(row, 0, QTableWidgetItem(manager.id))
                self.admin_table.setItem(row, 1, QTableWidgetItem(manager.name))
                self.admin_table.setItem(row, 2, QTableWidgetItem(manager.role))
                self.admin_table.setItem(row, 3, QTableWidgetItem(manager.email))
                self.admin_table.setItem(row, 4, QTableWidgetItem(manager.inserttime))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载管理员数据失败：{str(e)}")
    
    def load_users(self):
        """加载用户数据"""
        try:
            um = UserManagement()
            users = um.list_all_users()
            
            self.user_table.setRowCount(len(users))
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(user.id))
                self.user_table.setItem(row, 1, QTableWidgetItem(user.name))
                self.user_table.setItem(row, 2, QTableWidgetItem(user.telphone))
                self.user_table.setItem(row, 3, QTableWidgetItem(user.address))
                self.user_table.setItem(row, 4, QTableWidgetItem(user.email))
                self.user_table.setItem(row, 5, QTableWidgetItem(user.inserttime))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载用户数据失败：{str(e)}")
    
    def load_shops(self):
        """加载店铺数据"""
        try:
            sm = ShopManagement()
            shops = sm.list_all_shops()
            
            self.shop_table.setRowCount(len(shops))
            for row, shop in enumerate(shops):
                self.shop_table.setItem(row, 0, QTableWidgetItem(shop.id))
                self.shop_table.setItem(row, 1, QTableWidgetItem(shop.name))
                self.shop_table.setItem(row, 2, QTableWidgetItem(shop.telphone))
                self.shop_table.setItem(row, 3, QTableWidgetItem(shop.address))
                self.shop_table.setItem(row, 4, QTableWidgetItem(shop.email))
                self.shop_table.setItem(row, 5, QTableWidgetItem(shop.business_license))
                self.shop_table.setItem(row, 6, QTableWidgetItem(shop.type))
                self.shop_table.setItem(row, 7, QTableWidgetItem(shop.business_hours))
                self.shop_table.setItem(row, 8, QTableWidgetItem(shop.inserttime))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载店铺数据失败：{str(e)}")
    
    def logout(self):
        """退出登录"""
        self.parent.show_login_window()
    
    def show_add_shop_dialog(self):
        """显示添加店铺对话框"""
        from PyQt6.QtWidgets import QComboBox
        
        # 创建添加店铺对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("添加店铺")
        dialog.setFixedSize(400, 500)
        
        # 创建主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(15)
        
        # 店铺名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("店铺名称："))
        name_edit = QLineEdit()
        name_edit.setFont(QFont("Arial", 12))
        name_layout.addWidget(name_edit)
        main_layout.addLayout(name_layout)
        
        # 密码
        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(QLabel("密码："))
        pwd_edit = QLineEdit()
        pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        pwd_edit.setFont(QFont("Arial", 12))
        pwd_layout.addWidget(pwd_edit)
        main_layout.addLayout(pwd_layout)
        
        # 电话
        tel_layout = QHBoxLayout()
        tel_layout.addWidget(QLabel("电话："))
        tel_edit = QLineEdit()
        tel_edit.setFont(QFont("Arial", 12))
        tel_layout.addWidget(tel_edit)
        main_layout.addLayout(tel_layout)
        
        # 地址
        address_layout = QHBoxLayout()
        address_layout.addWidget(QLabel("地址："))
        address_edit = QLineEdit()
        address_edit.setFont(QFont("Arial", 12))
        address_layout.addWidget(address_edit)
        main_layout.addLayout(address_layout)
        
        # 邮箱
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("邮箱："))
        email_edit = QLineEdit()
        email_edit.setFont(QFont("Arial", 12))
        email_layout.addWidget(email_edit)
        main_layout.addLayout(email_layout)
        
        # 营业执照号
        license_layout = QHBoxLayout()
        license_layout.addWidget(QLabel("营业执照号："))
        license_edit = QLineEdit()
        license_edit.setFont(QFont("Arial", 12))
        license_layout.addWidget(license_edit)
        main_layout.addLayout(license_layout)
        
        # 店铺类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("店铺类型："))
        type_combo = QComboBox()
        type_combo.addItems(["中餐", "西餐", "快餐", "火锅", "烧烤", "甜点", "饮品", "其他"])
        type_combo.setFont(QFont("Arial", 12))
        type_layout.addWidget(type_combo)
        main_layout.addLayout(type_layout)
        
        # 营业时间
        hours_layout = QHBoxLayout()
        hours_layout.addWidget(QLabel("营业时间："))
        hours_edit = QLineEdit()
        hours_edit.setPlaceholderText("例如：10:00-22:00")
        hours_edit.setFont(QFont("Arial", 12))
        hours_layout.addWidget(hours_edit)
        main_layout.addLayout(hours_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFont(QFont("Arial", 12))
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        # 确认按钮
        ok_btn = QPushButton("确认")
        ok_btn.setFont(QFont("Arial", 12))
        ok_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_btn)
        
        main_layout.addLayout(button_layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 获取输入数据
            name = name_edit.text().strip()
            pwd = pwd_edit.text().strip()
            telphone = tel_edit.text().strip()
            address = address_edit.text().strip()
            email = email_edit.text().strip()
            business_license = license_edit.text().strip()
            shop_type = type_combo.currentText()
            business_hours = hours_edit.text().strip() if hours_edit.text().strip() else "10:00-22:00"
            
            try:
                # 添加店铺
                sm = ShopManagement()
                success = sm.register(name, pwd, telphone, address, email, business_license, shop_type, business_hours)
                if success:
                    QMessageBox.information(self, "成功", f"店铺'{name}'添加成功！")
                    self.load_shops()
                else:
                    QMessageBox.warning(self, "失败", "店铺添加失败！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"添加店铺失败：{str(e)}")
    
    def show_delete_shop_dialog(self):
        """显示删除店铺对话框"""
        # 获取选中的行
        current_row = self.shop_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要删除的店铺！")
            return
        
        # 获取当前店铺信息
        shop_id = self.shop_table.item(current_row, 0).text()
        name = self.shop_table.item(current_row, 1).text()
        
        # 确认删除
        reply = QMessageBox.question(self, "确认删除", f"确定要删除店铺'{name}'吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 删除店铺
                sm = ShopManagement()
                success = sm.delete_shop(shop_id)
                if success:
                    QMessageBox.information(self, "成功", "店铺删除成功！")
                    self.load_shops()
                else:
                    QMessageBox.warning(self, "失败", "店铺删除失败！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除店铺失败：{str(e)}")