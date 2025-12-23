"""
菜品模块 - 支持多店家独立菜单的菜品类定义
"""

import csv
import os
from typing import List, Dict, Optional

# CSV字段定义
DISH_FIELDS = ['id', 'name', 'price', 'category', 'description']

class Dish:
    """菜品类"""
    
    def __init__(self, dish_id: str, name: str, price: str, category: str, description: str):
        self.id = dish_id
        self.name = name
        self.price = price
        self.category = category
        self.description = description
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description
        }
    
    def to_list(self) -> List[str]:
        """转换为列表格式（用于CSV写入）"""
        return [
            self.id,
            self.name,
            self.price,
            self.category,
            self.description
        ]
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Dish':
        """从字典创建菜品对象"""
        return cls(
            dish_id=data['id'],
            name=data['name'],
            price=data['price'],
            category=data['category'],
            description=data['description']
        )
    
    @classmethod
    def from_list(cls, data: List[str]) -> 'Dish':
        """从列表创建菜品对象（用于CSV读取）"""
        if len(data) != len(DISH_FIELDS):
            raise ValueError(f"数据字段数不匹配，期望{len(DISH_FIELDS)}个字段，实际{len(data)}个字段")
        
        return cls(
            dish_id=data[0],
            name=data[1],
            price=data[2],
            category=data[3],
            description=data[4]
        )
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Dish(id={self.id}, name={self.name}, price={self.price}, category={self.category})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()


class DishManagement:
    """菜品管理类 - 支持多店家独立菜单"""
    
    def __init__(self, shop_id: str):
        self.shop_id = shop_id
        self.csv_file = f"shop/dish/shop_{shop_id}_dishes.csv"
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """确保CSV文件存在，如果不存在则创建并写入表头"""
        if not os.path.exists(self.csv_file):
            # 确保目录存在
            os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(DISH_FIELDS)
            print(f"已创建店家 {self.shop_id} 的菜品CSV文件: {self.csv_file}")
    
    def _read_all_dishes(self) -> List[Dish]:
        """读取所有菜品"""
        dishes = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dish = Dish.from_dict(row)
                    dishes.append(dish)
        except FileNotFoundError:
            print(f"菜品文件不存在: {self.csv_file}")
        except Exception as e:
            print(f"读取菜品文件时出错: {e}")
        return dishes
    
    def _write_dish(self, dish: Dish):
        """写入单个菜品到CSV文件"""
        try:
            # 读取现有菜品
            dishes = self._read_all_dishes()
            
            # 检查菜品ID是否已存在
            for existing_dish in dishes:
                if existing_dish.id == dish.id:
                    print(f"菜品ID已存在: {dish.id}")
                    return False
            
            # 添加新菜品
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(dish.to_list())
            
            print(f"菜品添加成功: {dish.name}")
            return True
            
        except Exception as e:
            print(f"写入菜品数据时出错: {e}")
            return False
    
    def _get_next_id(self) -> str:
        """获取下一个菜品ID"""
        dishes = self._read_all_dishes()
        if not dishes:
            return "1"
        
        # 提取现有ID的数字部分
        max_id = 0
        for dish in dishes:
            try:
                num = int(dish.id)
                max_id = max(max_id, num)
            except ValueError:
                continue
        
        return str(max_id + 1)
    
    def add_dish(self, name: str, price: str, category: str, description: str) -> bool:
        """
        添加新菜品
        
        Args:
            name: 菜品名称
            price: 价格
            category: 类别
            description: 描述
            
        Returns:
            bool: 添加是否成功
        """
        # 验证输入
        if not all([name, price, category, description]):
            print("所有字段都必须填写")
            return False
        
        # 检查菜品名称是否已存在
        dishes = self._read_all_dishes()
        for dish in dishes:
            if dish.name == name:
                print(f"菜品名称已存在: {name}")
                return False
        
        # 生成菜品ID
        dish_id = self._get_next_id()
        
        # 创建菜品对象
        new_dish = Dish(
            dish_id=dish_id,
            name=name,
            price=price,
            category=category,
            description=description
        )
        
        # 写入菜品数据
        return self._write_dish(new_dish)
    
    def get_dish_by_name(self, name: str) -> Optional[Dish]:
        """根据菜品名称获取菜品信息"""
        dishes = self._read_all_dishes()
        for dish in dishes:
            if dish.name == name:
                return dish
        return None
    
    def get_dish_by_id(self, dish_id: str) -> Optional[Dish]:
        """根据菜品ID获取菜品信息"""
        dishes = self._read_all_dishes()
        for dish in dishes:
            if dish.id == dish_id:
                return dish
        return None
    
    def list_all_dishes(self) -> List[Dish]:
        """列出所有菜品"""
        return self._read_all_dishes()
    
    def update_dish_info(self, dish_id: str, **kwargs) -> bool:
        """更新菜品信息"""
        dishes = self._read_all_dishes()
        updated = False
        
        for i, dish in enumerate(dishes):
            if dish.id == dish_id:
                # 更新菜品信息
                for key, value in kwargs.items():
                    if hasattr(dish, key) and key != 'id':  # 不允许修改ID
                        setattr(dish, key, value)
                        updated = True
                break
        
        if updated:
            # 重写整个文件
            try:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(DISH_FIELDS)
                    for dish in dishes:
                        writer.writerow(dish.to_list())
                print(f"菜品信息更新成功: {dish_id}")
                return True
            except Exception as e:
                print(f"更新菜品信息时出错: {e}")
                return False
        
        print(f"未找到菜品: {dish_id}")
        return False
    
    def delete_dish(self, dish_id: str) -> bool:
        """删除菜品"""
        dishes = self._read_all_dishes()
        original_count = len(dishes)
        
        # 过滤掉要删除的菜品
        dishes = [dish for dish in dishes if dish.id != dish_id]
        
        if len(dishes) == original_count:
            print(f"未找到要删除的菜品: {dish_id}")
            return False
        
        # 重写文件
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(DISH_FIELDS)
                for dish in dishes:
                    writer.writerow(dish.to_list())
            print(f"菜品删除成功: {dish_id}")
            return True
        except Exception as e:
            print(f"删除菜品时出错: {e}")
            return False
    
    def get_shop_id(self) -> str:
        """获取关联的店家ID"""
        return self.shop_id
    
    def get_csv_file_path(self) -> str:
        """获取CSV文件路径"""
        return self.csv_file