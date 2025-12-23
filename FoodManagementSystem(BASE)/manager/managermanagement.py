"""
管理员用户管理模块 - （管理员不支持注册）
"""

import csv
import os
from datetime import datetime
from typing import List, Optional
from manager.manager import Manager, MANAGER_CSV_FILE, MANAGER_FIELDS

class ManagerManagement:
    """管理员用户管理类"""
    
    def __init__(self):
        self.csv_file = MANAGER_CSV_FILE
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """确保CSV文件存在，如果不存在则创建并写入表头和默认管理员"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(MANAGER_FIELDS)
                # 添加默认超级管理员
                default_admin = Manager(
                    manager_id="M001",
                    name="admin",
                    pwd="admin123",
                    email="admin@restaurant.com",
                    role="超级管理员",
                    inserttime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                writer.writerow(default_admin.to_list())
            print(f"已创建管理员CSV文件: {self.csv_file}")
            print("已创建默认超级管理员: 用户名=admin, 密码=admin123")
    
    def _read_all_managers(self) -> List[Manager]:
        """读取所有管理员"""
        managers = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    manager = Manager.from_dict(row)
                    managers.append(manager)
        except FileNotFoundError:
            print(f"管理员文件不存在: {self.csv_file}")
        except Exception as e:
            print(f"读取管理员文件时出错: {e}")
        return managers
    
    def _write_manager(self, manager: Manager):
        """写入单个管理员到CSV文件（内部使用，用于初始化）"""
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(manager.to_list())
            return True
        except Exception as e:
            print(f"写入管理员数据时出错: {e}")
            return False
    
    def _get_next_id(self) -> str:
        """获取下一个管理员ID"""
        managers = self._read_all_managers()
        if not managers:
            return "M001"
        
        # 提取现有ID的数字部分
        max_id = 0
        for manager in managers:
            if manager.id.startswith('M'):
                try:
                    num = int(manager.id[1:])
                    max_id = max(max_id, num)
                except ValueError:
                    continue
        
        return f"M{max_id + 1:03d}"
    
    def login(self, name: str, pwd: str) -> Optional[Manager]:
        """
        管理员登录验证
        
        Args:
            name: 管理员用户名
            pwd: 密码
            
        Returns:
            Manager: 登录成功返回管理员对象，失败返回None
        """
        if not name or not pwd:
            print("管理员用户名和密码不能为空")
            return None
        
        managers = self._read_all_managers()
        for manager in managers:
            if manager.name == name and manager.pwd == pwd:
                print(f"登录成功: {manager.name} ({manager.role})")
                return manager
        
        print("管理员用户名或密码错误")
        return None
    
    def get_manager_by_name(self, name: str) -> Optional[Manager]:
        """根据管理员用户名获取管理员信息"""
        managers = self._read_all_managers()
        for manager in managers:
            if manager.name == name:
                return manager
        return None
    
    def get_manager_by_id(self, manager_id: str) -> Optional[Manager]:
        """根据管理员ID获取管理员信息"""
        managers = self._read_all_managers()
        for manager in managers:
            if manager.id == manager_id:
                return manager
        return None
    
    def list_all_managers(self) -> List[Manager]:
        """列出所有管理员"""
        return self._read_all_managers()
    
    def add_manager(self, name: str, pwd: str, email: str, role: str = "普通管理员") -> bool:
        """
        添加管理员（仅限超级管理员操作）
        
        Args:
            name: 管理员用户名
            pwd: 密码
            email: 邮箱
            role: 角色，默认为"普通管理员"
            
        Returns:
            bool: 添加是否成功
        """
        # 验证输入
        if not all([name, pwd, email, role]):
            print("所有字段都必须填写")
            return False
        
        # 检查用户名是否已存在
        managers = self._read_all_managers()
        for manager in managers:
            if manager.name == name:
                print(f"管理员用户名已存在: {name}")
                return False
        
        # 生成管理员ID和创建时间
        manager_id = self._get_next_id()
        inserttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 创建管理员对象
        new_manager = Manager(
            manager_id=manager_id,
            name=name,
            pwd=pwd,
            email=email,
            role=role,
            inserttime=inserttime
        )
        
        # 写入管理员数据
        return self._write_manager(new_manager)
    
    def update_manager_info(self, manager_id: str, **kwargs) -> bool:
        """更新管理员信息"""
        managers = self._read_all_managers()
        updated = False
        
        for i, manager in enumerate(managers):
            if manager.id == manager_id:
                # 更新管理员信息
                for key, value in kwargs.items():
                    if hasattr(manager, key) and key != 'id':  # 不允许修改ID
                        setattr(manager, key, value)
                        updated = True
                break
        
        if updated:
            # 重写整个文件
            try:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(MANAGER_FIELDS)
                    for manager in managers:
                        writer.writerow(manager.to_list())
                print(f"管理员信息更新成功: {manager_id}")
                return True
            except Exception as e:
                print(f"更新管理员信息时出错: {e}")
                return False
        
        print(f"未找到管理员: {manager_id}")
        return False
    
    def delete_manager(self, manager_id: str) -> bool:
        """删除管理员（不能删除超级管理员）"""
        managers = self._read_all_managers()
        
        # 检查是否为超级管理员
        target_manager = None
        for manager in managers:
            if manager.id == manager_id:
                target_manager = manager
                break
        
        if not target_manager:
            print(f"未找到要删除的管理员: {manager_id}")
            return False
        
        if target_manager.role == "超级管理员":
            print("不能删除超级管理员")
            return False
        
        # 过滤掉要删除的管理员
        original_count = len(managers)
        managers = [manager for manager in managers if manager.id != manager_id]
        
        if len(managers) == original_count:
            print(f"未找到要删除的管理员: {manager_id}")
            return False
        
        # 重写文件
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(MANAGER_FIELDS)
                for manager in managers:
                    writer.writerow(manager.to_list())
            print(f"管理员删除成功: {manager_id}")
            return True
        except Exception as e:
            print(f"删除管理员时出错: {e}")
            return False


# 测试代码
if __name__ == "__main__":
    # 创建管理员管理对象
    mm = ManagerManagement()
    
    # 测试登录
    print("=== 测试登录 ===")
    manager = mm.login("admin", "admin123")
    if manager:
        print(f"登录管理员: {manager}")
    
    manager = mm.login("admin", "wrongpwd")
    if manager:
        print(f"登录管理员: {manager}")
    else:
        print("登录失败")
    
    # 测试查询
    print("\n=== 测试查询 ===")
    all_managers = mm.list_all_managers()
    print(f"总管理员数: {len(all_managers)}")
    for m in all_managers:
        print(m)