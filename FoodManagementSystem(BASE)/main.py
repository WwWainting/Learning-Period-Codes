import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user.usermanagement import UserManagement
from shop.shopmanagement import ShopManagement
from manager.managermanagement import ManagerManagement
from user.ordermanagement import OrderManagement
from shop.dish.dishmanagement import DishManagement

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    """主菜单"""
    print("=" * 50)
    print("餐饮订餐系统")
    print("=" * 50)
    print("1. 我是消费者")
    print("2. 我是店家")
    print("3. 我是管理员")
    print("0. 退出系统")
    print("=" * 50)

def user_menu():
    """消费者菜单"""
    print("\n--- 消费者管理 ---")
    print("1. 注册")
    print("2. 登录")
    ##print("3. 查看所有消费者")
    print("0. 返回主菜单")

def shop_menu():
    """店家菜单"""
    print("\n--- 店家管理 ---")
    print("1. 注册")
    print("2. 登录")
    ##print("3. 查看所有店家")
    print("0. 返回主菜单")

def consumer_management():
    """消费者管理"""
    um = UserManagement()
    
    while True:
        user_menu()
        choice = input("请选择操作: ").strip()
        
        if choice == '1':
            # 消费者注册
            print("\n--- 消费者注册 ---")
            name = input("用户名: ").strip()
            pwd = input("密码: ").strip()
            telphone = input("电话号码: ").strip()
            address = input("地址: ").strip()
            email = input("邮箱: ").strip()
            
            success = um.register(name, pwd, telphone, address, email)
            if success:
                print("注册成功！")
            else:
                print("注册失败！")
        
        elif choice == '2':
            # 消费者登录
            print("\n--- 消费者登录 ---")
            name = input("用户名: ").strip()
            pwd = input("密码: ").strip()
            
            user = um.login(name, pwd)
            if user:
                print(f"登录成功！欢迎 {user.name}")
                print(f"用户信息: {user}")
                # 显示消费者操作菜单
                user_operations(user)
            else:
                print("登录失败！")
        
        elif choice == '3':
            # 查看所有消费者
            print("\n--- 所有消费者列表 ---")
            users = um.list_all_users()
            if users:
                for user in users:
                    print(f"ID: {user.id}, 姓名: {user.name}, 电话: {user.telphone}, 邮箱: {user.email}, 注册时间: {user.inserttime}")
            else:
                print("暂无消费者数据")
        
        elif choice == '0':
            break
        
        else:
            print("无效选择，请重新输入！")
        
        input("\n按回车键继续...")

def shop_management():
    """店家管理"""
    sm = ShopManagement()
    
    while True:
        shop_menu()
        choice = input("请选择操作: ").strip()
        
        if choice == '1':
            # 店家注册
            print("\n--- 店家注册 ---")
            name = input("店家名称: ").strip()
            pwd = input("密码: ").strip()
            telphone = input("电话号码: ").strip()
            address = input("地址: ").strip()
            email = input("邮箱: ").strip()
            business_license = input("营业执照号: ").strip()
            
            success = sm.register(name, pwd, telphone, address, email, business_license)
            if success:
                print("注册成功！")
            else:
                print("注册失败！")
        
        elif choice == '2':
            # 店家登录
            print("\n--- 店家登录 ---")
            name = input("店家名称: ").strip()
            pwd = input("密码: ").strip()
            
            shop = sm.login(name, pwd)
            if shop:
                print(f"登录成功！欢迎 {shop.name}")
                print(f"店家信息: {shop}")
                input("按回车键进入菜品管理...")
               # 进入菜品管理，传入店家名称和ID
                from shop.dish.dishmanagement import dish_menu
                dish_menu(shop.name, shop.id)
            else:
                print("登录失败！")
        
        elif choice == '3':
            # 查看所有店家
            print("\n--- 所有店家列表 ---")
            shops = sm.list_all_shops()
            if shops:
                for shop in shops:
                    print(f"ID: {shop.id}, 名称: {shop.name}, 电话: {shop.telphone}, 营业执照: {shop.business_license}, 注册时间: {shop.inserttime}")
            else:
                print("暂无店家数据")
        
        elif choice == '0':
            break
        
        else:
            print("无效选择，请重新输入！")
        
        input("\n按回车键继续...")

def admin_login():
    """管理员登录"""
    print("\n--- 管理员登录 ---")
    name = input("管理员用户名: ").strip()
    pwd = input("密码: ").strip()
    
    mm = ManagerManagement()
    manager = mm.login(name, pwd)
    
    if manager:
        print(f"登录成功！欢迎 {manager.name} ({manager.role})")
        
        # 如果是超级管理员，显示管理功能
        if manager.role == "超级管理员":
            while True:
                print("\n--- 管理员功能 ---")
                print("1. 查看所有管理员")
                print("2. 添加管理员")
                print("3. 查看所有消费者")
                print("4. 查看所有店家")
                print("0. 退出登录")
                
                choice = input("请选择操作: ").strip()
                
                if choice == '1':
                    # 查看所有管理员
                    print("\n--- 所有管理员列表 ---")
                    managers = mm.list_all_managers()
                    for m in managers:
                        print(f"ID: {m.id}, 用户名: {m.name}, 角色: {m.role}, 邮箱: {m.email}, 创建时间: {m.inserttime}")
                
                elif choice == '2':
                    # 添加管理员
                    print("\n--- 添加管理员 ---")
                    new_name = input("新管理员用户名: ").strip()
                    new_pwd = input("密码: ").strip()
                    new_email = input("邮箱: ").strip()
                    new_role = input("角色 (普通管理员/超级管理员): ").strip() or "普通管理员"
                    
                    success = mm.add_manager(new_name, new_pwd, new_email, new_role)
                    if success:
                        print("管理员添加成功！")
                    else:
                        print("管理员添加失败！")
                
                elif choice == '3':
                    # 查看所有消费者
                    print("\n--- 所有消费者列表 ---")
                    um = UserManagement()
                    users = um.list_all_users()
                    if users:
                        for user in users:
                            print(f"ID: {user.id}, 姓名: {user.name}, 电话: {user.telphone}, 注册时间: {user.inserttime}")
                    else:
                        print("暂无消费者数据")
                
                elif choice == '4':
                    # 查看所有店家
                    print("\n--- 所有店家列表 ---")
                    sm = ShopManagement()
                    shops = sm.list_all_shops()
                    if shops:
                        for shop in shops:
                            print(f"ID: {shop.id}, 名称: {shop.name}, 电话: {shop.telphone}, 营业执照: {shop.business_license}, 注册时间: {shop.inserttime}")
                    else:
                        print("暂无店家数据")
                
                elif choice == '0':
                    break
                
                else:
                    print("无效选择，请重新输入！")
                
                input("\n按回车键继续...")
        else:
            print("普通管理员权限有限，仅可查看信息")
            input("按回车键返回主菜单...")
    
    else:
        print("登录失败！")
        input("按回车键返回主菜单...")

def main():
    
    """主函数"""
    while True:
        clear_screen()
        main_menu()
        choice = input("请选择功能: ").strip()
        
        if choice == '1':
            clear_screen()
            consumer_management()
        
        elif choice == '2':
            clear_screen()
            shop_management()
        
        elif choice == '3':
            clear_screen()
            admin_login()
        
        elif choice == '0':
            print("感谢使用餐饮订餐系统，再见！")
            break
        
        else:
            print("无效选择，请重新输入！")
            input("按回车键继续...")

def user_operations(user):
    """消费者登录后的操作菜单"""
    om = OrderManagement()
    sm = ShopManagement()
    
    while True:
        print(f"\n{'='*50}")
        print(f"        欢迎 {user.name} - 消费者中心")
        print(f"{'='*50}")
        print("1. 查看所有店铺")
        print("2. 查看店铺菜单")
        print("3. 查看购物车")
        print("4. 提交购物车订单")
        print("5. 查看历史订单")
        print("0. 退出登录")
        print(f"{'='*50}")
        
        choice = input("请选择操作: ").strip()
        
        if choice == "1":
            # 查看所有店铺
            print("\n--- 所有店铺列表 ---")
            shops = sm.list_all_shops()
            if shops:
                print(f"{'ID':<8} {'名称':<20} {'电话':<15} {'地址':<20}")
                print("-" * 75)
                for shop in shops:
                    print(f"{shop.id:<8} {shop.name:<20} {shop.telphone:<15} {shop.address:<20}")
            else:
                print("暂无店铺数据")
        
        elif choice == "2":
            # 查看店铺菜单
            print("\n--- 查看店铺菜单 ---")
            shop_id = input("请输入店铺ID: ").strip()
            
            # 检查店铺是否存在
            shop = sm.get_shop_by_id(shop_id)
            if not shop:
                print("店铺不存在")
                continue
            
            print(f"\n{'='*50}")
            print(f"        {shop.name} (ID: {shop.id}) - 菜单")
            print(f"{'='*50}")
            
            # 获取店铺菜品
            dm = DishManagement(shop.id)
            dishes = dm.list_all_dishes()
            
            if not dishes:
                print("暂无菜品")
                continue
            
            # 显示菜品列表
            print(f"{'ID':<4} {'菜品名称':<15} {'价格':<8} {'类别':<8} {'描述':<20}")
            print("-" * 70)
            for dish in dishes:
                print(f"{dish.id:<4} {dish.name:<15} {dish.price:<8} {dish.category:<8} {dish.description:<20}")
            
            # 添加购物车选项
            print("\n输入菜品ID添加到购物车 (直接回车返回):")
            while True:
                dish_id = input("菜品ID: ").strip()
                if not dish_id:
                    break
                
                # 查找菜品
                dish = dm.get_dish_by_id(dish_id)
                if not dish:
                    print("菜品不存在")
                    continue
                
                # 添加到购物车
                try:
                    quantity = int(input("数量: ").strip() or "1")
                    success = om.add_to_cart(user.id, shop.id, dish.id, dish.name, dish.price, quantity)
                    if success:
                        print(f"\033[92m{dish.name} x {quantity} 已加入购物车\033[0m")
                    else:
                        print(f"\033[91m加入购物车失败\033[0m")
                except ValueError:
                    print("数量格式错误")
        
        elif choice == "3":
            # 查看购物车
            print("\n--- 我的购物车 ---")
            cart_orders = om.get_cart_orders(user.id)
            
            if not cart_orders:
                print("购物车为空")
                continue
            
            # 按店铺分组显示
            cart_by_shop = {}
            for order in cart_orders:
                if order.shop_id not in cart_by_shop:
                    cart_by_shop[order.shop_id] = []
                cart_by_shop[order.shop_id].append(order)
            
            for shop_id, orders in cart_by_shop.items():
                shop = sm.get_shop_by_id(shop_id)
                if shop:
                    print(f"\n{shop.name} (ID: {shop.id}):")
                    print(f"{'菜品ID':<6} {'菜品名称':<15} {'价格':<8} {'数量':<6}")
                    print("-" * 45)
                    
                    total = 0.0
                    for order in orders:
                        price = float(order.price)
                        subtotal = price * order.quantity
                        total += subtotal
                        print(f"{order.dish_id:<6} {order.dish_name:<15} {order.price:<8} {order.quantity:<6} ({subtotal:.2f}元)")
                    
                    print(f"\n总计: {total:.2f} 元")
        
        elif choice == "4":
            # 提交购物车订单
            print("\n--- 提交购物车订单 ---")
            cart_orders = om.get_cart_orders(user.id)
            
            if not cart_orders:
                print("购物车为空")
                continue
            
            # 按店铺分组
            cart_by_shop = {}
            for order in cart_orders:
                if order.shop_id not in cart_by_shop:
                    cart_by_shop[order.shop_id] = []
                cart_by_shop[order.shop_id].append(order)
            
            for shop_id, orders in cart_by_shop.items():
                confirm = input(f"确定要提交{len(orders)}个商品的订单吗？(y/N): ").strip().lower()
                if confirm == "y" or confirm == "yes":
                    success = om.submit_order(user.id, shop_id)
                    if success:
                        print(f"\033[92m订单已提交到店铺 {shop_id}\033[0m")
                    else:
                        print(f"\033[91m提交订单失败\033[0m")
        
        elif choice == "5":
            # 查看历史订单
            print("\n--- 我的历史订单 ---")
            history_orders = om.get_user_orders(user.id)
            
            if not history_orders:
                print("暂无历史订单")
                continue
            
            # 按店铺和订单ID分组
            orders_by_shop = {}
            for order in history_orders:
                if order.status == "购物车":
                    continue
                    
                if order.shop_id not in orders_by_shop:
                    orders_by_shop[order.shop_id] = {}
                if order.order_id not in orders_by_shop[order.shop_id]:
                    orders_by_shop[order.shop_id][order.order_id] = []
                orders_by_shop[order.shop_id][order.order_id].append(order)
            
            for shop_id, orders_dict in orders_by_shop.items():
                shop = sm.get_shop_by_id(shop_id)
                if not shop:
                    continue
                    
                print(f"\n{'='*60}")
                print(f"店铺: {shop.name} (ID: {shop.id})")
                print(f"{'='*60}")
                
                for order_id, order_items in orders_dict.items():
                    # 计算订单总价
                    total = 0.0
                    for item in order_items:
                        try:
                            total += float(item.price) * item.quantity
                        except ValueError:
                            pass
                    
                    print(f"\n订单ID: {order_id}")
                    print(f"状态: {order_items[0].status}")
                    print(f"下单时间: {order_items[0].order_time}")
                    print(f"{'菜品名称':<15} {'价格':<8} {'数量':<6} {'小计':<8}")
                    print("-" * 45)
                    
                    for item in order_items:
                        subtotal = float(item.price) * item.quantity
                        print(f"{item.dish_name:<15} {item.price:<8} {item.quantity:<6} {subtotal:.2f}元")
                    
                    print(f"\n订单总计: {total:.2f} 元")
        
        elif choice == "0":
            print("退出登录")
            break
        
        else:
            print("输入无效，请重新选择")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    print("餐饮订餐系统启动中...")
    ##
    # 0
    # print("系统说明:")
    ##print("1. 消费者：支持注册和登录")
    ##print("2. 店家：支持注册和登录，需要营业执照号")
    ##print("3. 管理员：仅支持登录，不支持注册")
    ##print("   - 默认管理员: admin / admin123")
    ##print("-" * 50)
    input("按回车键进入系统...")
    
    main()