"""
店家用户管理模块 - 实现登录、注册等功能
"""

import csv
import os
from datetime import datetime
from typing import List, Optional
from shop.shop import Shop, SHOP_CSV_FILE, SHOP_FIELDS

class ShopManagement:
    """店家用户管理类"""
    
    def __init__(self):
        self.csv_file = SHOP_CSV_FILE
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """确保CSV文件存在，如果不存在则创建并写入表头"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(SHOP_FIELDS)
            print(f"已创建店家CSV文件: {self.csv_file}")
    
    def _read_all_shops(self) -> List[Shop]:
        """读取所有店家"""
        shops = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    shop = Shop.from_dict(row)
                    shops.append(shop)
        except FileNotFoundError:
            print(f"店家文件不存在: {self.csv_file}")
        except Exception as e:
            print(f"读取店家文件时出错: {e}")
        return shops
    
    def _write_shop(self, shop: Shop):
        """写入单个店家到CSV文件"""
        try:
            # 读取现有店家
            shops = self._read_all_shops()
            
            # 检查店家ID是否已存在
            for existing_shop in shops:
                if existing_shop.id == shop.id:
                    print(f"店家ID已存在: {shop.id}")
                    return False
            
            # 添加新店家 - 重新写入整个文件以确保格式正确
            shops.append(shop)
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(SHOP_FIELDS)
                for s in shops:
                    writer.writerow(s.to_list())
            
            print(f"店家注册成功: {shop.name}")
            return True
            
        except Exception as e:
            print(f"写入店家数据时出错: {e}")
            return False
    
    def _get_next_id(self) -> str:
        """获取下一个店家ID"""
        shops = self._read_all_shops()
        if not shops:
            return "S001"
        
        # 提取现有ID的数字部分
        max_id = 0
        for shop in shops:
            if shop.id.startswith('S'):
                try:
                    num = int(shop.id[1:])
                    max_id = max(max_id, num)
                except ValueError:
                    continue
        
        return f"S{max_id + 1:03d}"
    
    def register(self, name: str, pwd: str, telphone: str, address: str, email: str, business_license: str, shop_type: str = "其他", business_hours: str = "10:00-22:00") -> bool:
        """
        注册新店家
        
        Args:
            name: 店家名称
            pwd: 密码
            telphone: 电话号码
            address: 地址
            email: 邮箱
            business_license: 营业执照号
            shop_type: 店铺类型
            business_hours: 营业时间
            
        Returns:
            bool: 注册是否成功
        """
        # 验证输入
        if not all([name, pwd, telphone, address, email, business_license]):
            print("所有字段都必须填写")
            return False
        
        # 检查店家名称是否已存在
        shops = self._read_all_shops()
        for shop in shops:
            if shop.name == name:
                print(f"店家名称已存在: {name}")
                return False
        
        # 检查营业执照号是否已存在
        for shop in shops:
            if shop.business_license == business_license:
                print(f"营业执照号已存在: {business_license}")
                return False
        
        # 生成店家ID和注册时间
        shop_id = self._get_next_id()
        inserttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 创建店家对象
        new_shop = Shop(
            shop_id=shop_id,
            name=name,
            pwd=pwd,
            telphone=telphone,
            address=address,
            email=email,
            business_license=business_license,
            shop_type=shop_type,
            business_hours=business_hours,
            inserttime=inserttime
        )
        
        # 写入店家数据
        return self._write_shop(new_shop)
    
    def login(self, name: str, pwd: str) -> Optional[Shop]:
        """
        店家登录验证
        
        Args:
            name: 店家名称
            pwd: 密码
            
        Returns:
            Shop: 登录成功返回店家对象，失败返回None
        """
        if not name or not pwd:
            print("店家名称和密码不能为空")
            return None
        
        shops = self._read_all_shops()
        for shop in shops:
            if shop.name == name and shop.pwd == pwd:
                print(f"登录成功: {shop.name}")
                return shop
        
        print("店家名称或密码错误")
        return None
    
    def get_shop_by_name(self, name: str) -> Optional[Shop]:
        """根据店家名称获取店家信息"""
        shops = self._read_all_shops()
        for shop in shops:
            if shop.name == name:
                return shop
        return None
    
    def get_shop_by_id(self, shop_id: str) -> Optional[Shop]:
        """根据店家ID获取店家信息"""
        shops = self._read_all_shops()
        for shop in shops:
            if shop.id == shop_id:
                return shop
        return None
    
    def list_all_shops(self) -> List[Shop]:
        """列出所有店家"""
        return self._read_all_shops()
    
    def update_shop_info(self, shop_id: str, **kwargs) -> bool:
        """更新店家信息"""
        shops = self._read_all_shops()
        updated = False
        
        for i, shop in enumerate(shops):
            if shop.id == shop_id:
                # 更新店家信息
                for key, value in kwargs.items():
                    if hasattr(shop, key) and key != 'id':  # 不允许修改ID
                        setattr(shop, key, value)
                        updated = True
                break
        
        if updated:
            # 重写整个文件
            try:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(SHOP_FIELDS)
                    for shop in shops:
                        writer.writerow(shop.to_list())
                print(f"店家信息更新成功: {shop_id}")
                return True
            except Exception as e:
                print(f"更新店家信息时出错: {e}")
                return False
        
        print(f"未找到店家: {shop_id}")
        return False
    
    def delete_shop(self, shop_id: str) -> bool:
        """删除店家"""
        shops = self._read_all_shops()
        original_count = len(shops)
        
        # 过滤掉要删除的店家
        shops = [shop for shop in shops if shop.id != shop_id]
        
        if len(shops) == original_count:
            print(f"未找到要删除的店家: {shop_id}")
            return False
        
        # 重写文件
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(SHOP_FIELDS)
                for shop in shops:
                    writer.writerow(shop.to_list())
            print(f"店家删除成功: {shop_id}")
            return True
        except Exception as e:
            print(f"删除店家时出错: {e}")
            return False


# 测试代码
if __name__ == "__main__":
    # 创建店家管理对象
    sm = ShopManagement()
    
    # 测试注册
    print("=== 测试注册 ===")
    success = sm.register("川味轩", "shop123", "13600136000", "北京市西城区新街口外大街2号", "chuanweixuan@example.com", "1101011234567890")
    print(f"注册结果: {success}")
    
    success = sm.register("粤香阁", "shop456", "13500135000", "北京市海淀区中关村大街1号", "yuexiangge@example.com", "1101089876543210")
    print(f"注册结果: {success}")
    
    # 测试登录
    print("\n=== 测试登录 ===")
    shop = sm.login("川味轩", "shop123")
    if shop:
        print(f"登录店家: {shop}")
    
    shop = sm.login("川味轩", "wrongpwd")
    if shop:
        print(f"登录店家: {shop}")
    else:
        print("登录失败")
    
    # 测试查询
    print("\n=== 测试查询 ===")
    all_shops = sm.list_all_shops()
    print(f"总店家数: {len(all_shops)}")
    for s in all_shops:
        print(s)