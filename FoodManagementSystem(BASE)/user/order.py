import csv
import os
from datetime import datetime
from typing import List, Optional

class Order:
    """订单类"""
    def __init__(self, order_id: str, user_id: str, shop_id: str, dish_id: str, dish_name: str, price: str, quantity: int, status: str, order_time: str):
        self.order_id = order_id
        self.user_id = user_id
        self.shop_id = shop_id
        self.dish_id = dish_id
        self.dish_name = dish_name
        self.price = price
        self.quantity = quantity
        self.status = status  # 状态："购物车"、"已提交"、"已完成"
        self.order_time = order_time
    
    def to_dict(self) -> dict:
        """将订单对象转换为字典"""
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'shop_id': self.shop_id,
            'dish_id': self.dish_id,
            'dish_name': self.dish_name,
            'price': self.price,
            'quantity': str(self.quantity),
            'status': self.status,
            'order_time': self.order_time
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """从字典创建订单对象"""
        return cls(
            order_id=data['order_id'],
            user_id=data['user_id'],
            shop_id=data['shop_id'],
            dish_id=data['dish_id'],
            dish_name=data['dish_name'],
            price=data['price'],
            quantity=int(data['quantity']),
            status=data['status'],
            order_time=data['order_time']
        )
    
    def to_list(self) -> list:
        """将订单对象转换为列表"""
        return [
            self.order_id,
            self.user_id,
            self.shop_id,
            self.dish_id,
            self.dish_name,
            self.price,
            str(self.quantity),
            self.status,
            self.order_time
        ]

# 订单字段
ORDER_FIELDS = ['order_id', 'user_id', 'shop_id', 'dish_id', 'dish_name', 'price', 'quantity', 'status', 'order_time']

# 订单文件路径模板
ORDER_FILE_TEMPLATE = 'user/orders_{user_id}.csv'
