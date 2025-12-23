"""
消费者用户管理模块 - 实现登录、注册等功能
"""

import csv
import os
from datetime import datetime
from typing import List, Optional
from user.user import User, USER_CSV_FILE, USER_FIELDS

class UserManagement:
    """消费者用户管理类"""
    
    def __init__(self):
        self.csv_file = USER_CSV_FILE
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """确保CSV文件存在，如果不存在则创建并写入表头"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(USER_FIELDS)
            print(f"已创建用户CSV文件: {self.csv_file}")
    
    def _read_all_users(self) -> List[User]:
        """读取所有用户"""
        users = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User.from_dict(row)
                    users.append(user)
        except FileNotFoundError:
            print(f"用户文件不存在: {self.csv_file}")
        except Exception as e:
            print(f"读取用户文件时出错: {e}")
        return users
    
    def _write_user(self, user: User):
        """写入单个用户到CSV文件"""
        try:
            # 读取现有用户
            users = self._read_all_users()
            
            # 检查用户ID是否已存在
            for existing_user in users:
                if existing_user.id == user.id:
                    print(f"用户ID已存在: {user.id}")
                    return False
            
            # 添加新用户 - 重写整个文件以确保格式正确
            users.append(user)
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(USER_FIELDS)
                for u in users:
                    writer.writerow(u.to_list())
            
            print(f"用户注册成功: {user.name}")
            return True
            
        except Exception as e:
            print(f"写入用户数据时出错: {e}")
            return False
    
    def _get_next_id(self) -> str:
        """获取下一个用户ID"""
        users = self._read_all_users()
        if not users:
            return "U001"
        
        # 提取现有ID的数字部分
        max_id = 0
        for user in users:
            if user.id.startswith('U'):
                try:
                    num = int(user.id[1:])
                    max_id = max(max_id, num)
                except ValueError:
                    continue
        
        return f"U{max_id + 1:03d}"
    
    def register(self, name: str, pwd: str, telphone: str, address: str, email: str) -> bool:
        """
        注册新用户
        
        Args:
            name: 用户名
            pwd: 密码
            telphone: 电话号码
            address: 地址
            email: 邮箱
            
        Returns:
            bool: 注册是否成功
        """
        # 验证输入
        if not all([name, pwd, telphone, address, email]):
            print("所有字段都必须填写")
            return False
        
        # 检查用户名是否已存在
        users = self._read_all_users()
        for user in users:
            if user.name == name:
                print(f"用户名已存在: {name}")
                return False
        
        # 生成用户ID和注册时间
        user_id = self._get_next_id()
        inserttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 创建用户对象
        new_user = User(
            user_id=user_id,
            name=name,
            pwd=pwd,
            telphone=telphone,
            address=address,
            email=email,
            inserttime=inserttime
        )
        
        # 写入用户数据
        return self._write_user(new_user)
    
    def login(self, name: str, pwd: str) -> Optional[User]:
        """
        用户登录验证
        
        Args:
            name: 用户名
            pwd: 密码
            
        Returns:
            User: 登录成功返回用户对象，失败返回None
        """
        if not name or not pwd:
            print("用户名和密码不能为空")
            return None
        
        users = self._read_all_users()
        for user in users:
            if user.name == name and user.pwd == pwd:
                print(f"登录成功: {user.name}")
                return user
        
        print("用户名或密码错误")
        return None
    
    def get_user_by_name(self, name: str) -> Optional[User]:
        """根据用户名获取用户信息"""
        users = self._read_all_users()
        for user in users:
            if user.name == name:
                return user
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """根据用户ID获取用户信息"""
        users = self._read_all_users()
        for user in users:
            if user.id == user_id:
                return user
        return None
    
    def list_all_users(self) -> List[User]:
        """列出所有用户"""
        return self._read_all_users()
    
    def update_user_info(self, user_id: str, **kwargs) -> bool:
        """更新用户信息"""
        users = self._read_all_users()
        updated = False
        
        for i, user in enumerate(users):
            if user.id == user_id:
                # 更新用户信息
                for key, value in kwargs.items():
                    if hasattr(user, key) and key != 'id':  # 不允许修改ID
                        setattr(user, key, value)
                        updated = True
                break
        
        if updated:
            # 重写整个文件
            try:
                with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(USER_FIELDS)
                    for user in users:
                        writer.writerow(user.to_list())
                print(f"用户信息更新成功: {user_id}")
                return True
            except Exception as e:
                print(f"更新用户信息时出错: {e}")
                return False
        
        print(f"未找到用户: {user_id}")
        return False
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        users = self._read_all_users()
        original_count = len(users)
        
        # 过滤掉要删除的用户
        users = [user for user in users if user.id != user_id]
        
        if len(users) == original_count:
            print(f"未找到要删除的用户: {user_id}")
            return False
        
        # 重写文件
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(USER_FIELDS)
                for user in users:
                    writer.writerow(user.to_list())
            print(f"用户删除成功: {user_id}")
            return True
        except Exception as e:
            print(f"删除用户时出错: {e}")
            return False


# 测试代码
if __name__ == "__main__":
    # 创建用户管理对象
    um = UserManagement()
    
    # 测试注册
    print("=== 测试注册 ===")
    success = um.register("张三", "123456", "13800138000", "北京市朝阳区", "zhangsan@example.com")
    print(f"注册结果: {success}")
    
    success = um.register("李四", "654321", "13900139000", "上海市浦东新区", "lisi@example.com")
    print(f"注册结果: {success}")
    
    # 测试登录
    print("\n=== 测试登录 ===")
    user = um.login("张三", "123456")
    if user:
        print(f"登录用户: {user}")
    
    user = um.login("张三", "wrongpwd")
    if user:
        print(f"登录用户: {user}")
    else:
        print("登录失败")
    
    # 测试查询
    print("\n=== 测试查询 ===")
    all_users = um.list_all_users()
    print(f"总用户数: {len(all_users)}")
    for u in all_users:
        print(u)