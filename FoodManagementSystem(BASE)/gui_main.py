import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入拆分后的界面模块
from login_register import LoginWindow, RegisterWindow
from user_menu import UserMenuWindow
from shop_menu import ShopMenuWindow
from admin_menu import AdminMenuWindow

class MainApplication(QMainWindow):
    """主应用程序"""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("餐饮订餐系统")
        
        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建堆叠部件
        self.stacked_widget = QStackedWidget()
        self.central_widget.setLayout(QVBoxLayout())
        self.central_widget.layout().addWidget(self.stacked_widget)
        
        # 创建并显示登录界面
        self.show_login_window()
    
    def show_login_window(self):
        """显示登录界面"""
        # 检查是否已存在登录界面
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, LoginWindow):
                self.stacked_widget.setCurrentWidget(widget)
                self.resize(400, 300)
                widget.username_edit.setFocus()  # 设置焦点到用户名输入框
                return
        
        # 创建新的登录界面
        self.login_window = LoginWindow(self)
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.setCurrentWidget(self.login_window)
        self.resize(400, 300)
        self.login_window.username_edit.setFocus()  # 设置焦点到用户名输入框
    
    def show_user_menu(self, user):
        """显示用户菜单界面"""
        # 检查是否已存在用户菜单界面
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, UserMenuWindow):
                self.stacked_widget.setCurrentWidget(widget)
                widget.load_shops()  # 刷新店铺数据
                self.resize(1000, 600)
                return
        
        # 创建新的用户菜单界面
        self.user_menu_window = UserMenuWindow(user, self)
        self.stacked_widget.addWidget(self.user_menu_window)
        self.stacked_widget.setCurrentWidget(self.user_menu_window)
        self.resize(1000, 600)
    
    def show_shop_menu(self, shop):
        """显示店家菜单界面"""
        # 移除现有的ShopMenuWindow实例
        for i in reversed(range(self.stacked_widget.count())):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, ShopMenuWindow):
                self.stacked_widget.removeWidget(widget)
                widget.deleteLater()  # 确保 widget 被正确销毁
        
        # 创建新的店家菜单界面
        self.shop_menu_window = ShopMenuWindow(shop, self)
        self.stacked_widget.addWidget(self.shop_menu_window)
        self.stacked_widget.setCurrentWidget(self.shop_menu_window)
        self.resize(900, 600)
    
    def show_admin_menu(self, manager):
        """显示管理员菜单界面"""
        # 检查是否已存在管理员菜单界面
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, AdminMenuWindow):
                self.stacked_widget.setCurrentWidget(widget)
                widget.load_users()  # 刷新用户数据
                widget.load_shops()  # 刷新店铺数据
                if manager.role == "超级管理员":
                    widget.load_admins()  # 刷新管理员数据
                self.resize(1000, 600)
                return
        
        # 创建新的管理员菜单界面
        self.admin_menu_window = AdminMenuWindow(manager, self)
        self.stacked_widget.addWidget(self.admin_menu_window)
        self.stacked_widget.setCurrentWidget(self.admin_menu_window)
        self.resize(1000, 600)
    
    def show_register_window(self, role):
        """显示注册界面"""
        # 检查是否已存在注册界面
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            if isinstance(widget, RegisterWindow):
                # 更新角色并刷新界面
                widget.role = role
                widget.setWindowTitle(f"餐饮订餐系统 - {role}注册")
                widget.title_label.setText(f"{role}注册")
                self.stacked_widget.setCurrentWidget(widget)
                self.resize(450, 400)
                widget.username_edit.setFocus()  # 设置焦点到用户名输入框
                return
        
        # 创建新的注册界面
        self.register_window = RegisterWindow(role, self)
        self.stacked_widget.addWidget(self.register_window)
        self.stacked_widget.setCurrentWidget(self.register_window)
        self.resize(450, 400)
        self.register_window.username_edit.setFocus()  # 设置焦点到用户名输入框

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec())