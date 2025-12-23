"""
管理员用户模块
"""

import csv
from typing import List, Dict, Optional

# CSV文件路径
MANAGER_CSV_FILE = 'manager/manager.csv'

# CSV字段定义
MANAGER_FIELDS = ['id', 'name', 'pwd', 'email', 'role', 'inserttime']

class Manager:
    """管理员用户类"""
    
    def __init__(self, manager_id: str, name: str, pwd: str, email: str, role: str, inserttime: str = None):
        self.id = manager_id
        self.name = name
        self.pwd = pwd
        self.email = email
        self.role = role  # 角色：超级管理员、普通管理员等
        self.inserttime = inserttime
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'pwd': self.pwd,
            'email': self.email,
            'role': self.role,
            'inserttime': self.inserttime
        }
    
    def to_list(self) -> List[str]:
        """转换为列表格式（用于CSV写入）"""
        return [
            self.id,
            self.name,
            self.pwd,
            self.email,
            self.role,
            self.inserttime
        ]
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Manager':
        """从字典创建管理员对象"""
        return cls(
            manager_id=data['id'],
            name=data['name'],
            pwd=data['pwd'],
            email=data['email'],
            role=data['role'],
            inserttime=data['inserttime']
        )
    
    @classmethod
    def from_list(cls, data: List[str]) -> 'Manager':
        """从列表创建管理员对象（用于CSV读取）"""
        if len(data) != len(MANAGER_FIELDS):
            raise ValueError(f"数据字段数不匹配，期望{len(MANAGER_FIELDS)}个字段，实际{len(data)}个字段")
        
        return cls(
            manager_id=data[0],
            name=data[1],
            pwd=data[2],
            email=data[3],
            role=data[4],
            inserttime=data[5]
        )
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Manager(id={self.id}, name={self.name}, role={self.role}, email={self.email})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()