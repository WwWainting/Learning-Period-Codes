"""
店家用户模块 - 定义店家CSV结构和相关常量
"""

import csv
from typing import List, Dict, Optional

# CSV文件路径
SHOP_CSV_FILE = 'shop/shop.csv'

# CSV字段定义
SHOP_FIELDS = ['id', 'name', 'pwd', 'telphone', 'address', 'email', 'business_license', 'type', 'business_hours', 'inserttime']

class Shop:
    """店家用户类"""
    
    def __init__(self, shop_id: str, name: str, pwd: str, telphone: str, 
                 address: str, email: str, business_license: str, shop_type: str = "其他", 
                 business_hours: str = "10:00-22:00", inserttime: str = None):
        self.id = shop_id
        self.name = name
        self.pwd = pwd
        self.telphone = telphone
        self.address = address
        self.email = email
        self.business_license = business_license
        self.type = shop_type
        self.business_hours = business_hours
        self.inserttime = inserttime
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'pwd': self.pwd,
            'telphone': self.telphone,
            'address': self.address,
            'email': self.email,
            'business_license': self.business_license,
            'type': self.type,
            'business_hours': self.business_hours,
            'inserttime': self.inserttime
        }
    
    def to_list(self) -> List[str]:
        """转换为列表格式（用于CSV写入）"""
        return [
            self.id,
            self.name,
            self.pwd,
            self.telphone,
            self.address,
            self.email,
            self.business_license,
            self.type,
            self.business_hours,
            self.inserttime
        ]
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Shop':
        """从字典创建店家对象"""
        return cls(
            shop_id=data['id'],
            name=data['name'],
            pwd=data['pwd'],
            telphone=data['telphone'],
            address=data['address'],
            email=data['email'],
            business_license=data['business_license'],
            shop_type=data.get('type', '其他'),
            business_hours=data.get('business_hours', '10:00-22:00'),
            inserttime=data['inserttime']
        )
    
    @classmethod
    def from_list(cls, data: List[str]) -> 'Shop':
        """从列表创建店家对象（用于CSV读取）"""
        if len(data) != len(SHOP_FIELDS):
            raise ValueError(f"数据字段数不匹配，期望{len(SHOP_FIELDS)}个字段，实际{len(data)}个字段")
        
        return cls(
            shop_id=data[0],
            name=data[1],
            pwd=data[2],
            telphone=data[3],
            address=data[4],
            email=data[5],
            business_license=data[6],
            shop_type=data[7],
            business_hours=data[8],
            inserttime=data[9]
        )
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Shop(id={self.id}, name={self.name}, telphone={self.telphone}, license={self.business_license})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()