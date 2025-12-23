import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QGroupBox, QHeaderView, QDialog, QTabWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shop.dish.dishmanagement import DishManagement
from dialogs import AddDishDialog, EditDishDialog
from user.ordermanagement import OrderManagement
from user.usermanagement import UserManagement

class ShopMenuWindow(QWidget):
    """店家菜单界面"""
    def __init__(self, shop, parent=None):
        super().__init__(parent)
        self.shop = shop
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle(f"餐饮订餐系统 - 店家管理 ({self.shop.name})")
        self.resize(1000, 600)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建顶部信息栏
        top_layout = QHBoxLayout()
        welcome_label = QLabel(f"欢迎您，{self.shop.name}！")
        welcome_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        top_layout.addWidget(welcome_label)
        top_layout.addStretch()
        
        logout_button = QPushButton("退出登录")
        logout_button.clicked.connect(self.logout)
        top_layout.addWidget(logout_button)
        main_layout.addLayout(top_layout)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 创建菜品管理选项卡
        self.create_dish_management_tab()
        
        # 创建订单管理选项卡
        self.create_order_management_tab()
        
        # 加载菜品数据
        self.load_dishes()
    
    def load_dishes(self):
        """加载菜品数据"""
        try:
            dm = DishManagement(self.shop.id)
            dishes = dm.list_all_dishes()
            
            self.dish_table.setRowCount(len(dishes))
            for row, dish in enumerate(dishes):
                self.dish_table.setItem(row, 0, QTableWidgetItem(dish.id))
                self.dish_table.setItem(row, 1, QTableWidgetItem(dish.name))
                self.dish_table.setItem(row, 2, QTableWidgetItem(str(dish.price)))
                self.dish_table.setItem(row, 3, QTableWidgetItem(dish.category))
                self.dish_table.setItem(row, 4, QTableWidgetItem(dish.description))
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载菜品数据失败：{str(e)}")
    
    def logout(self):
        """退出登录"""
        self.parent.show_login_window()

    def show_add_dish_dialog(self):
        """显示添加菜品对话框"""
        dialog = AddDishDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.name_edit.text().strip()
            price = dialog.price_edit.text().strip()
            category = dialog.category_combo.currentText()
            description = dialog.desc_edit.text().strip()
            
            try:
                dm = DishManagement(self.shop.id)
                success = dm.add_dish(name, price, category, description)
                if success:
                    QMessageBox.information(self, "成功", f"菜品'{name}'添加成功！")
                    self.load_dishes()
                else:
                    QMessageBox.warning(self, "失败", "菜品添加失败！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"添加菜品失败：{str(e)}")

    def show_edit_dish_dialog(self):
        """显示编辑菜品对话框"""
        # 获取选中的行
        current_row = self.dish_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要编辑的菜品！")
            return
        
        # 获取当前菜品信息
        dish_id = self.dish_table.item(current_row, 0).text()
        name = self.dish_table.item(current_row, 1).text()
        price = self.dish_table.item(current_row, 2).text()
        category = self.dish_table.item(current_row, 3).text()
        description = self.dish_table.item(current_row, 4).text()
        
        dialog = EditDishDialog(dish_id, name, price, category, description, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            update_params = dialog.get_update_params()
            if update_params:
                try:
                    dm = DishManagement(self.shop.id)
                    success = dm.update_dish_info(dish_id, **update_params)
                    if success:
                        QMessageBox.information(self, "成功", "菜品信息更新成功！")
                        self.load_dishes()
                    else:
                        QMessageBox.warning(self, "失败", "菜品信息更新失败！")
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"更新菜品失败：{str(e)}")

    def show_delete_dish_dialog(self):
        """显示删除菜品对话框"""
        # 获取选中的行
        current_row = self.dish_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要删除的菜品！")
            return
        
        # 获取当前菜品信息
        dish_id = self.dish_table.item(current_row, 0).text()
        name = self.dish_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, "确认删除", f"确定要删除菜品'{name}'吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                dm = DishManagement(self.shop.id)
                success = dm.delete_dish(dish_id)
                if success:
                    QMessageBox.information(self, "成功", "菜品删除成功！")
                    self.load_dishes()
                else:
                    QMessageBox.warning(self, "失败", "菜品删除失败！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除菜品失败：{str(e)}")

    def show_dish_stats(self):
        """显示菜品统计信息"""
        try:
            dm = DishManagement(self.shop.id)
            dishes = dm.list_all_dishes()
            
            if not dishes:
                QMessageBox.information(self, "提示", "暂无菜品数据！")
                return
            
            # 统计各类别数量
            categories = {}
            total_value = 0.0
            
            for dish in dishes:
                # 类别统计
                if dish.category not in categories:
                    categories[dish.category] = 0
                categories[dish.category] += 1
                
                # 总价值统计
                try:
                    total_value += float(dish.price)
                except ValueError:
                    pass
            
            # 构建统计信息文本
            stats_text = f"\n--- 菜品统计信息 ---\n"
            stats_text += f"\n菜品总数: {len(dishes)}"
            stats_text += f"\n菜单总价值: {total_value:.2f} 元"
            stats_text += f"\n\n各类别分布:"
            
            for category, count in categories.items():
                percentage = (count / len(dishes)) * 100
                stats_text += f"\n  {category}: {count}道 ({percentage:.1f}%)"
            
            # 显示统计信息
            QMessageBox.information(self, "菜品统计", stats_text)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"获取菜品统计失败：{str(e)}")

    def create_dish_management_tab(self):
        """创建菜品管理选项卡"""
        dish_tab = QWidget()
        main_layout = QVBoxLayout(dish_tab)
        
        # 顶部按钮布局
        button_layout = QHBoxLayout()
        add_btn = QPushButton("添加菜品")
        add_btn.clicked.connect(self.show_add_dish_dialog)
        edit_btn = QPushButton("编辑菜品")
        edit_btn.clicked.connect(self.show_edit_dish_dialog)
        delete_btn = QPushButton("删除菜品")
        delete_btn.clicked.connect(self.show_delete_dish_dialog)
        stats_btn = QPushButton("菜品统计")
        stats_btn.clicked.connect(self.show_dish_stats)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(stats_btn)
        main_layout.addLayout(button_layout)
        
        # 菜品表格
        self.dish_table = QTableWidget()
        self.dish_table.setColumnCount(5)
        self.dish_table.setHorizontalHeaderLabels(["菜品ID", "菜品名称", "价格", "分类", "描述"])
        self.dish_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.dish_table)
        
        self.tab_widget.addTab(dish_tab, "菜品管理")

    def create_order_management_tab(self):
        """创建订单管理选项卡"""
        order_tab = QWidget()
        main_layout = QVBoxLayout(order_tab)
        
        # 订单表格
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(10)
        self.order_table.setHorizontalHeaderLabels(["订单ID", "用户ID", "用户姓名", "用户电话", "菜品名称", "价格", "数量", "状态", "下单时间", "操作"])
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.order_table)
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新订单")
        refresh_btn.clicked.connect(self.load_orders)
        main_layout.addWidget(refresh_btn)
        
        self.tab_widget.addTab(order_tab, "订单管理")
        
        # 初始加载订单
        self.load_orders()

    def load_orders(self):
        """加载订单数据"""
        try:
            om = OrderManagement()
            um = UserManagement()
            orders = om.get_shop_orders(self.shop.id)
            
            self.order_table.setRowCount(len(orders))
            for row, order in enumerate(orders):
                self.order_table.setItem(row, 0, QTableWidgetItem(order.order_id))
                self.order_table.setItem(row, 1, QTableWidgetItem(order.user_id))
                
                # 获取用户信息
                user = um.get_user_by_id(order.user_id)
                user_name = user.name if user else "未知"
                user_tel = user.telphone if user else "未知"
                
                self.order_table.setItem(row, 2, QTableWidgetItem(user_name))
                self.order_table.setItem(row, 3, QTableWidgetItem(user_tel))
                self.order_table.setItem(row, 4, QTableWidgetItem(order.dish_name))
                self.order_table.setItem(row, 5, QTableWidgetItem(order.price))
                self.order_table.setItem(row, 6, QTableWidgetItem(str(order.quantity)))
                self.order_table.setItem(row, 7, QTableWidgetItem(order.status))
                self.order_table.setItem(row, 8, QTableWidgetItem(order.order_time))
                
                # 操作按钮
                complete_btn = QPushButton("标记完成")
                complete_btn.setProperty("order_id", order.order_id)
                complete_btn.setProperty("user_id", order.user_id)
                complete_btn.clicked.connect(self.mark_order_complete)
                self.order_table.setCellWidget(row, 9, complete_btn)
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载订单数据失败：{str(e)}")

    def mark_order_complete(self):
        """标记订单为完成"""
        button = self.sender()
        order_id = button.property("order_id")
        user_id = button.property("user_id")
        
        try:
            om = OrderManagement()
            success = om.complete_order(user_id, order_id)
            if success:
                QMessageBox.information(self, "成功", "订单已标记为完成！")
                self.load_orders()
            else:
                QMessageBox.warning(self, "失败", "标记订单完成失败！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"标记订单完成失败：{str(e)}")