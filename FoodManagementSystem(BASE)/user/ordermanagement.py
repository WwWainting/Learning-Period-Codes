import csv
import os
from datetime import datetime
from typing import List, Optional
from user.order import Order, ORDER_FIELDS, ORDER_FILE_TEMPLATE

class OrderManagement:
    """订单管理类"""
    
    def __init__(self, user_id: str = None):
        self.user_id = user_id
        if user_id:
            self.order_file = ORDER_FILE_TEMPLATE.format(user_id=user_id)
        else:
            self.order_file = None
        self._ensure_order_file_exists()
    
    def _ensure_order_file_exists(self):
        """确保订单文件存在"""
        if self.order_file and not os.path.exists(self.order_file):
            with open(self.order_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(ORDER_FIELDS)
            print(f"已创建订单文件: {self.order_file}")
    
    def _read_all_orders(self, user_id: str = None) -> List[Order]:
        """读取所有订单"""
        orders = []
        try:
            if user_id:
                order_file = ORDER_FILE_TEMPLATE.format(user_id=user_id)
            else:
                order_file = self.order_file
            
            if not order_file or not os.path.exists(order_file):
                return orders
                
            with open(order_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    order = Order.from_dict(row)
                    orders.append(order)
        except Exception as e:
            print(f"读取订单文件时出错: {e}")
        return orders
    
    def _write_orders(self, orders: List[Order], user_id: str = None):
        """写入订单到CSV文件"""
        try:
            if user_id:
                order_file = ORDER_FILE_TEMPLATE.format(user_id=user_id)
            else:
                order_file = self.order_file
            
            if not order_file:
                return False
                
            with open(order_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(ORDER_FIELDS)
                for order in orders:
                    writer.writerow(order.to_list())
            return True
        except Exception as e:
            print(f"写入订单文件时出错: {e}")
            return False
    
    def _get_next_order_id(self, user_id: str = None) -> str:
        """获取下一个订单ID"""
        orders = self._read_all_orders(user_id)
        if not orders:
            return "O001"
        
        max_id = 0
        for order in orders:
            if order.order_id.startswith('O'):
                try:
                    num = int(order.order_id[1:])
                    max_id = max(max_id, num)
                except ValueError:
                    continue
        
        return f"O{max_id + 1:03d}"
    
    def add_to_cart(self, user_id: str, shop_id: str, dish_id: str, dish_name: str, price: str, quantity: int = 1) -> bool:
        """添加菜品到购物车"""
        try:
            orders = self._read_all_orders(user_id)
            
            # 检查是否已经在购物车中
            for order in orders:
                if (order.shop_id == shop_id and order.dish_id == dish_id and 
                    order.user_id == user_id and order.status == "购物车"):
                    # 更新数量
                    order.quantity += quantity
                    order.order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return self._write_orders(orders, user_id)
            
            # 不在购物车中，添加新订单
            order_id = self._get_next_order_id(user_id)
            order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            new_order = Order(
                order_id=order_id,
                user_id=user_id,
                shop_id=shop_id,
                dish_id=dish_id,
                dish_name=dish_name,
                price=price,
                quantity=quantity,
                status="购物车",
                order_time=order_time
            )
            
            orders.append(new_order)
            return self._write_orders(orders, user_id)
        except Exception as e:
            print(f"添加到购物车失败: {e}")
            return False
    
    def submit_order(self, user_id: str, shop_id: str) -> bool:
        """提交订单"""
        try:
            orders = self._read_all_orders(user_id)
            
            # 更新指定店铺的购物车订单状态
            updated = False
            for order in orders:
                if (order.user_id == user_id and order.shop_id == shop_id and 
                    order.status == "购物车"):
                    order.status = "已提交"
                    order.order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    updated = True
            
            if not updated:
                return False
            
            return self._write_orders(orders, user_id)
        except Exception as e:
            print(f"提交订单失败: {e}")
            return False
    
    def get_cart_orders(self, user_id: str, shop_id: str = None) -> List[Order]:
        """获取购物车中的订单"""
        orders = self._read_all_orders(user_id)
        cart_orders = []
        
        for order in orders:
            if order.user_id == user_id and order.status == "购物车":
                if shop_id is None or order.shop_id == shop_id:
                    cart_orders.append(order)
        
        return cart_orders
    
    def get_submitted_orders(self, user_id: str) -> List[Order]:
        """获取用户已提交的订单"""
        orders = self._read_all_orders(user_id)
        return [order for order in orders if order.user_id == user_id and order.status != "购物车"]
    
    def get_shop_orders(self, shop_id: str) -> List[Order]:
        """获取商家的所有订单"""
        # 遍历所有用户订单文件
        shop_orders = []
        user_dir = "d:/project/user"
        
        for file_name in os.listdir(user_dir):
            if file_name.startswith("orders_") and file_name.endswith(".csv"):
                file_path = os.path.join(user_dir, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            order = Order.from_dict(row)
                            # 检查shop_id是否匹配，不管状态如何，先添加所有匹配的订单
                            if order.shop_id == shop_id:
                                shop_orders.append(order)
                except Exception as e:
                    print(f"读取订单文件 {file_name} 时出错: {e}")
        
        return shop_orders
    
    def remove_from_cart(self, user_id: str, order_id: str) -> bool:
        """从购物车移除订单"""
        try:
            orders = self._read_all_orders(user_id)
            orders = [order for order in orders if not (order.user_id == user_id and order.order_id == order_id and order.status == "购物车")]
            return self._write_orders(orders, user_id)
        except Exception as e:
            print(f"从购物车移除失败: {e}")
            return False
    
    def update_cart_quantity(self, user_id: str, order_id: str, quantity: int) -> bool:
        """更新购物车中订单的数量"""
        try:
            orders = self._read_all_orders(user_id)
            
            for order in orders:
                if (order.user_id == user_id and order.order_id == order_id and 
                    order.status == "购物车"):
                    order.quantity = quantity
                    order.order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return self._write_orders(orders, user_id)
            
            return False
        except Exception as e:
            print(f"更新购物车数量失败: {e}")
            return False
    
    def complete_order(self, user_id: str, order_id: str) -> bool:
        """完成订单"""
        try:
            orders = self._read_all_orders(user_id)
            
            for order in orders:
                if order.user_id == user_id and order.order_id == order_id:
                    order.status = "已完成"
                    order.order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return self._write_orders(orders, user_id)
            
            return False
        except Exception as e:
            print(f"完成订单失败: {e}")
            return False
