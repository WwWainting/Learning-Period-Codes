#!/usr/bin/env python3
"""
测试订单功能的脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user.ordermanagement import OrderManagement
from user.usermanagement import UserManagement
from shop.shopmanagement import ShopManagement
from shop.dish.dishmanagement import DishManagement

def test_order_management():
    """测试订单管理功能"""
    print("=" * 50)
    print("测试订单管理功能")
    print("=" * 50)
    
    # 创建测试用户
    um = UserManagement()
    success = um.register("test_user", "password123", "13800138000", "测试地址", "test@example.com")
    # 不管注册是否成功，都尝试登录
    test_user = um.login("test_user", "password123")
    
    if not test_user:
        print("创建/登录测试用户失败")
        return
    
    print(f"测试用户: {test_user.name} (ID: {test_user.id})")
    
    # 创建测试店铺
    sm = ShopManagement()
    success = sm.register("测试店铺", "shop123", "13900139000", "测试店铺地址", "shop@example.com", "1234567890")
    # 不管注册是否成功，都尝试登录
    test_shop = sm.login("测试店铺", "shop123")
    
    if not test_shop:
        print("创建/登录测试店铺失败")
        return
    
    print(f"测试店铺: {test_shop.name} (ID: {test_shop.id})")
    
    # 添加测试菜品
    dm = DishManagement(test_shop.id)
    success = dm.add_dish("宫保鸡丁", "38.00", "热菜", "经典川菜")
    if success:
        print("添加测试菜品: 宫保鸡丁")
    
    # 获取菜品对象（不管是否新添加）
    test_dish = dm.get_dish_by_name("宫保鸡丁")
    
    if not test_dish:
        print("创建/获取测试菜品失败")
        return
    
    print(f"测试菜品: {test_dish.name} (ID: {test_dish.id}, 价格: {test_dish.price})")
    
    # 测试订单功能
    om = OrderManagement()
    
    # 1. 添加到购物车
    print("\n1. 测试添加到购物车...")
    success = om.add_to_cart(test_user.id, test_shop.id, test_dish.id, test_dish.name, test_dish.price, 2)
    if success:
        print("✓ 添加到购物车成功")
    else:
        print("✗ 添加到购物车失败")
        return
    
    # 2. 查看购物车
    print("\n2. 测试查看购物车...")
    cart_orders = om.get_cart_orders(test_user.id)
    if cart_orders:
        print(f"✓ 购物车中有 {len(cart_orders)} 个商品")
        for order in cart_orders:
            print(f"   - {order.dish_name} x {order.quantity} (¥{order.price})")
    else:
        print("✗ 购物车为空")
        return
    
    # 3. 提交订单
    print("\n3. 测试提交订单...")
    success = om.submit_order(test_user.id, test_shop.id)
    if success:
        print("✓ 提交订单成功")
    else:
        print("✗ 提交订单失败")
        return
    
    # 4. 查看用户历史订单
    print("\n4. 测试查看用户历史订单...")
    user_orders = om.get_submitted_orders(test_user.id)
    if user_orders:
        print(f"✓ 用户有 {len(user_orders)} 个订单")
        for order in user_orders:
            print(f"   - 订单ID: {order.order_id}, 菜品: {order.dish_name}, 状态: {order.status}")
    else:
        print("✗ 用户没有订单")
    
    # 5. 测试店铺查看订单
    print("\n5. 测试店铺查看订单...")
    shop_orders = om.get_shop_orders(test_shop.id)
    if shop_orders:
        print(f"✓ 店铺有 {len(shop_orders)} 个订单")
        for order in shop_orders:
            print(f"   - 订单ID: {order.order_id}, 用户ID: {order.user_id}, 菜品: {order.dish_name}, 状态: {order.status}")
    else:
        print("✗ 店铺没有订单")
    
    # 6. 测试标记订单为完成
    print("\n6. 测试标记订单为完成...")
    if shop_orders:
        order_to_complete = shop_orders[0]
        success = om.complete_order(order_to_complete.user_id, order_to_complete.order_id)
        if success:
            print("✓ 标记订单为完成成功")
        else:
            print("✗ 标记订单为完成失败")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    test_order_management()
