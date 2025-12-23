import sys
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtGui import QFont

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from shop.dish.dishmanagement import DishManagement

class AddDishDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加菜品")
        self.setFixedSize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # 菜品名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("菜品名称："))
        self.name_edit = QLineEdit()
        self.name_edit.setFont(QFont("Arial", 12))
        name_layout.addWidget(self.name_edit)
        main_layout.addLayout(name_layout)
        
        # 菜品价格
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("菜品价格："))
        self.price_edit = QLineEdit()
        self.price_edit.setFont(QFont("Arial", 12))
        price_layout.addWidget(self.price_edit)
        main_layout.addLayout(price_layout)
        
        # 菜品分类
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("菜品分类："))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["热菜", "冷菜", "汤品", "主食", "甜点", "饮品", "其他"])
        self.category_combo.setFont(QFont("Arial", 12))
        category_layout.addWidget(self.category_combo)
        main_layout.addLayout(category_layout)
        
        # 菜品描述
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("菜品描述："))
        self.desc_edit = QLineEdit()
        self.desc_edit.setFont(QFont("Arial", 12))
        desc_layout.addWidget(self.desc_edit)
        main_layout.addLayout(desc_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setFont(QFont("Arial", 12))
        cancel_button.setFixedHeight(35)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.setFont(QFont("Arial", 12))
        ok_button.setFixedHeight(35)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(button_layout)
    
    def get_dish_info(self):
        """获取菜品信息"""
        name = self.name_edit.text().strip()
        price = self.price_edit.text().strip()
        category = self.category_combo.currentText()
        description = self.desc_edit.text().strip()
        
        if not name or not price:
            QMessageBox.warning(self, "警告", "菜品名称和价格不能为空！")
            return None
        
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的价格！")
            return None
        
        return {
            "name": name,
            "price": price,
            "category": category,
            "description": description
        }

class EditDishDialog(QDialog):
    def __init__(self, dish_id, name, price, category, description, parent=None):
        super().__init__(parent)
        self.dish_id = dish_id
        self.original_name = name
        self.original_price = price
        self.original_category = category
        self.original_description = description
        self.setWindowTitle("编辑菜品")
        self.setFixedSize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # 菜品ID（只读）
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("菜品ID："))
        id_label = QLabel(self.dish_id)
        id_label.setFont(QFont("Arial", 12))
        id_label.setStyleSheet("background-color: #f0f0f0;")
        id_layout.addWidget(id_label)
        main_layout.addLayout(id_layout)
        
        # 菜品名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("菜品名称："))
        self.name_edit = QLineEdit(self.original_name)
        self.name_edit.setFont(QFont("Arial", 12))
        name_layout.addWidget(self.name_edit)
        main_layout.addLayout(name_layout)
        
        # 菜品价格
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("菜品价格："))
        self.price_edit = QLineEdit(str(self.original_price))
        self.price_edit.setFont(QFont("Arial", 12))
        price_layout.addWidget(self.price_edit)
        main_layout.addLayout(price_layout)
        
        # 菜品分类
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("菜品分类："))
        self.category_combo = QComboBox()
        categories = ["热菜", "冷菜", "汤品", "主食", "甜点", "饮品", "其他"]
        self.category_combo.addItems(categories)
        if self.original_category in categories:
            self.category_combo.setCurrentText(self.original_category)
        self.category_combo.setFont(QFont("Arial", 12))
        category_layout.addWidget(self.category_combo)
        main_layout.addLayout(category_layout)
        
        # 菜品描述
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("菜品描述："))
        self.desc_edit = QLineEdit(self.original_description)
        self.desc_edit.setFont(QFont("Arial", 12))
        desc_layout.addWidget(self.desc_edit)
        main_layout.addLayout(desc_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setFont(QFont("Arial", 12))
        cancel_button.setFixedHeight(35)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.setFont(QFont("Arial", 12))
        ok_button.setFixedHeight(35)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(button_layout)
    
    def get_update_params(self):
        """获取更新参数"""
        name = self.name_edit.text().strip()
        price = self.price_edit.text().strip()
        category = self.category_combo.currentText()
        description = self.desc_edit.text().strip()
        
        if not name or not price:
            QMessageBox.warning(self, "警告", "菜品名称和价格不能为空！")
            return None
        
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的价格！")
            return None
        
        # 只返回有变化的字段
        update_params = {}
        if name != self.original_name:
            update_params["name"] = name
        if price != self.original_price:
            update_params["price"] = price
        if category != self.original_category:
            update_params["category"] = category
        if description != self.original_description:
            update_params["description"] = description
        
        return update_params