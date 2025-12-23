import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QGroupBox, QHeaderView, QSplitter, QStackedWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shop.shopmanagement import ShopManagement
from shop.dish.dishmanagement import DishManagement
from dialogs import AddDishDialog, EditDishDialog
from user.ordermanagement import OrderManagement

class UserMenuWindow(QWidget):
    """用户菜单界面"""
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle(f"餐饮订餐系统 - 欢迎 {self.user.name}")
        self.resize(1000, 600)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建顶部信息栏
        top_layout = QHBoxLayout()
        welcome_label = QLabel(f"欢迎您，{self.user.name}！")
        welcome_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        top_layout.addWidget(welcome_label)
        top_layout.addStretch()
        
        # 添加页面切换按钮
        self.browse_btn = QPushButton("浏览店铺")
        self.browse_btn.clicked.connect(self.show_browse_page)
        top_layout.addWidget(self.browse_btn)
        
        self.cart_btn = QPushButton("购物车")
        self.cart_btn.clicked.connect(self.show_cart_page)
        top_layout.addWidget(self.cart_btn)
        
        self.orders_btn = QPushButton("我的订单")
        self.orders_btn.clicked.connect(self.show_orders_page)
        top_layout.addWidget(self.orders_btn)
        
        logout_button = QPushButton("退出登录")
        logout_button.clicked.connect(self.logout)
        top_layout.addWidget(logout_button)
        main_layout.addLayout(top_layout)
        
        # 创建堆叠窗口用于页面切换
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # 创建浏览页面
        self.create_browse_page()
        
        # 创建购物车页面
        self.create_cart_page()
        
        # 创建订单页面
        self.create_orders_page()
        
        # 初始化显示浏览页面
        self.stacked_widget.setCurrentIndex(0)
        
        # 加载店铺数据
        self.load_shops()
    
    def create_browse_page(self):
        """创建浏览店铺和菜品的页面"""
        browse_page = QWidget()
        
        # 创建主布局
        main_layout = QVBoxLayout(browse_page)
        
        # 创建主要内容区域
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧店铺列表
        shop_group = QGroupBox("店铺列表")
        shop_layout = QVBoxLayout(shop_group)
        
        # 店铺表格
        self.shop_table = QTableWidget()
        self.shop_table.setColumnCount(4)
        self.shop_table.setHorizontalHeaderLabels(["店铺ID", "店铺名称", "电话", "地址"])
        self.shop_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.shop_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.shop_table.itemClicked.connect(self.show_shop_dishes)
        shop_layout.addWidget(self.shop_table)
        
        # 右侧菜品列表
        dish_group = QGroupBox("菜品列表")
        dish_layout = QVBoxLayout(dish_group)
        
        # 店铺信息
        self.shop_info_label = QLabel("请选择一个店铺查看菜品")
        self.shop_info_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.shop_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dish_layout.addWidget(self.shop_info_label)
        
        # 菜品表格
        self.dish_table = QTableWidget()
        self.dish_table.setColumnCount(6)
        self.dish_table.setHorizontalHeaderLabels(["菜品ID", "菜品名称", "价格", "分类", "描述", "操作"])
        self.dish_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        dish_layout.addWidget(self.dish_table)
        
        splitter.addWidget(shop_group)
        splitter.addWidget(dish_group)
        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)
        
        self.stacked_widget.addWidget(browse_page)
    
    def create_cart_page(self):
        """创建购物车页面"""
        cart_page = QWidget()
        
        # 创建主布局
        main_layout = QVBoxLayout(cart_page)
        
        # 购物车表格
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(7)
        self.cart_table.setHorizontalHeaderLabels(["订单ID", "店铺ID", "店铺名称", "菜品名称", "价格", "数量", "操作"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.cart_table)
        
        # 底部操作按钮
        bottom_layout = QHBoxLayout()
        
        self.refresh_cart_btn = QPushButton("刷新购物车")
        self.refresh_cart_btn.clicked.connect(self.load_cart)
        bottom_layout.addWidget(self.refresh_cart_btn)
        
        self.submit_order_btn = QPushButton("提交订单")
        self.submit_order_btn.clicked.connect(self.submit_order)
        bottom_layout.addWidget(self.submit_order_btn)
        
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)
        
        self.stacked_widget.addWidget(cart_page)
    
    def create_orders_page(self):
        """创建订单页面"""
        orders_page = QWidget()
        
        # 创建主布局
        main_layout = QVBoxLayout(orders_page)
        
        # 订单表格
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(8)
        self.orders_table.setHorizontalHeaderLabels(["订单ID", "店铺ID", "店铺名称", "菜品名称", "价格", "数量", "状态", "下单时间"])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.orders_table)
        
        # 底部操作按钮
        bottom_layout = QHBoxLayout()
        
        self.refresh_orders_btn = QPushButton("刷新订单")
        self.refresh_orders_btn.clicked.connect(self.load_orders)
        bottom_layout.addWidget(self.refresh_orders_btn)
        
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)
        
        self.stacked_widget.addWidget(orders_page)
    
    def show_browse_page(self):
        """显示浏览页面"""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_cart_page(self):
        """显示购物车页面"""
        self.stacked_widget.setCurrentIndex(1)
        self.load_cart()
    
    def show_orders_page(self):
        """显示订单页面"""
        self.stacked_widget.setCurrentIndex(2)
        self.load_orders()
    
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
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载店铺数据失败：{str(e)}")
    
    def show_shop_dishes(self, item):
        """显示选中店铺的菜品"""
        row = item.row()
        self.selected_shop_id = self.shop_table.item(row, 0).text()
        self.selected_shop_name = self.shop_table.item(row, 1).text()
        
        self.shop_info_label.setText(f"{self.selected_shop_name} 的菜品")
        
        try:
            dm = DishManagement(self.selected_shop_id)
            dishes = dm.list_all_dishes()
            
            self.dish_table.setRowCount(len(dishes))
            for row, dish in enumerate(dishes):
                self.dish_table.setItem(row, 0, QTableWidgetItem(dish.id))
                self.dish_table.setItem(row, 1, QTableWidgetItem(dish.name))
                self.dish_table.setItem(row, 2, QTableWidgetItem(str(dish.price)))
                self.dish_table.setItem(row, 3, QTableWidgetItem(dish.category))
                self.dish_table.setItem(row, 4, QTableWidgetItem(dish.description))
                
                # 添加加入购物车按钮
                add_to_cart_btn = QPushButton("加入购物车")
                add_to_cart_btn.clicked.connect(lambda checked, dish_id=dish.id, dish_name=dish.name, price=str(dish.price): 
                                                self.add_to_cart(dish_id, dish_name, price))
                self.dish_table.setCellWidget(row, 5, add_to_cart_btn)
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载菜品数据失败：{str(e)}")
    
    def add_to_cart(self, dish_id, dish_name, price):
        """将菜品加入购物车"""
        try:
            om = OrderManagement()
            success = om.add_to_cart(self.user.id, self.selected_shop_id, dish_id, dish_name, price)
            if success:
                QMessageBox.information(self, "成功", f"{dish_name} 已加入购物车！")
            else:
                QMessageBox.warning(self, "失败", "加入购物车失败！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加入购物车失败：{str(e)}")
    
    def load_cart(self):
        """加载购物车数据"""
        try:
            om = OrderManagement()
            cart_orders = om.get_cart_orders(self.user.id)
            
            # 获取店铺名称映射
            sm = ShopManagement()
            shops = sm.list_all_shops()
            shop_name_map = {shop.id: shop.name for shop in shops}
            
            self.cart_table.setRowCount(len(cart_orders))
            for row, order in enumerate(cart_orders):
                self.cart_table.setItem(row, 0, QTableWidgetItem(order.order_id))
                self.cart_table.setItem(row, 1, QTableWidgetItem(order.shop_id))
                self.cart_table.setItem(row, 2, QTableWidgetItem(shop_name_map.get(order.shop_id, "未知店铺")))
                self.cart_table.setItem(row, 3, QTableWidgetItem(order.dish_name))
                self.cart_table.setItem(row, 4, QTableWidgetItem(order.price))
                self.cart_table.setItem(row, 5, QTableWidgetItem(str(order.quantity)))
                
                # 添加删除按钮
                delete_btn = QPushButton("删除")
                delete_btn.clicked.connect(lambda checked, order_id=order.order_id: self.remove_from_cart(order_id))
                self.cart_table.setCellWidget(row, 6, delete_btn)
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载购物车失败：{str(e)}")
    
    def remove_from_cart(self, order_id):
        """从购物车中删除订单"""
        try:
            om = OrderManagement()
            success = om.remove_from_cart(self.user.id, order_id)
            if success:
                QMessageBox.information(self, "成功", "删除成功！")
                self.load_cart()
            else:
                QMessageBox.warning(self, "失败", "删除失败！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除失败：{str(e)}")
    
    def submit_order(self):
        """提交订单"""
        try:
            om = OrderManagement()
            # 获取当前购物车中的所有订单
            cart_orders = om.get_cart_orders(self.user.id)
            
            if not cart_orders:
                QMessageBox.warning(self, "提示", "购物车为空，无法提交订单！")
                return
            
            # 按店铺分组提交订单
            shop_ids = set([order.shop_id for order in cart_orders])
            
            for shop_id in shop_ids:
                success = om.submit_order(self.user.id, shop_id)
                if success:
                    QMessageBox.information(self, "成功", f"提交订单成功！")
                else:
                    QMessageBox.warning(self, "失败", f"提交订单失败！")
            
            # 刷新购物车和订单页面
            self.load_cart()
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"提交订单失败：{str(e)}")
    
    def load_orders(self):
        """加载用户的所有订单"""
        try:
            om = OrderManagement()
            orders = om.get_submitted_orders(self.user.id)
            
            # 获取店铺名称映射
            sm = ShopManagement()
            shops = sm.list_all_shops()
            shop_name_map = {shop.id: shop.name for shop in shops}
            
            self.orders_table.setRowCount(len(orders))
            for row, order in enumerate(orders):
                self.orders_table.setItem(row, 0, QTableWidgetItem(order.order_id))
                self.orders_table.setItem(row, 1, QTableWidgetItem(order.shop_id))
                self.orders_table.setItem(row, 2, QTableWidgetItem(shop_name_map.get(order.shop_id, "未知店铺")))
                self.orders_table.setItem(row, 3, QTableWidgetItem(order.dish_name))
                self.orders_table.setItem(row, 4, QTableWidgetItem(order.price))
                self.orders_table.setItem(row, 5, QTableWidgetItem(str(order.quantity)))
                self.orders_table.setItem(row, 6, QTableWidgetItem(order.status))
                self.orders_table.setItem(row, 7, QTableWidgetItem(order.order_time))
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载订单失败：{str(e)}")
    
    def logout(self):
        """退出登录"""
        self.parent.show_login_window()