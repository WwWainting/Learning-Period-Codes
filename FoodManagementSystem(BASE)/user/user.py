"""
消费者用户模块 - 定义用户CSV结构和相关常量
"""

import csv
from typing import List, Dict, Optional

# CSV文件路径
USER_CSV_FILE = 'user/user.csv'

# CSV字段定义
USER_FIELDS = ['id', 'name', 'pwd', 'telphone', 'address', 'email', 'inserttime']

class User:
    """消费者用户类"""
    
    def __init__(self, user_id: str, name: str, pwd: str, telphone: str, 
                 address: str, email: str, inserttime: str = None):
        self.id = user_id
        self.name = name
        self.pwd = pwd
        self.telphone = telphone
        self.address = address
        self.email = email
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
            self.inserttime
        ]
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'User':
        """从字典创建用户对象"""
        return cls(
            user_id=data['id'],
            name=data['name'],
            pwd=data['pwd'],
            telphone=data['telphone'],
            address=data['address'],
            email=data['email'],
            inserttime=data['inserttime']
        )
    
    @classmethod
    def from_list(cls, data: List[str]) -> 'User':
        """从列表创建用户对象（用于CSV读取）"""
        if len(data) != len(USER_FIELDS):
            raise ValueError(f"数据字段数不匹配，期望{len(USER_FIELDS)}个字段，实际{len(data)}个字段")
        
        return cls(
            user_id=data[0],
            name=data[1],
            pwd=data[2],
            telphone=data[3],
            address=data[4],
            email=data[5],
            inserttime=data[6]
        )
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"User(id={self.id}, name={self.name}, telphone={self.telphone}, email={self.email})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()