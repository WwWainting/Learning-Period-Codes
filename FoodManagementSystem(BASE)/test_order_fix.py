import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user.ordermanagement import OrderManagement

# 测试get_shop_orders方法是否正确筛选订单
def test_shop_orders():
    print("Testing get_shop_orders method...")
    
    # 创建OrderManagement实例
    om = OrderManagement()
    
    # 测试不同店铺ID的订单获取
    print("\n1. Testing orders for shop S001:")
    shop1_orders = om.get_shop_orders("S001")
    for order in shop1_orders:
        print(f"   Order ID: {order.order_id}, User ID: {order.user_id}, Shop ID: {order.shop_id}, Dish: {order.dish_name}, Status: {order.status}")
    
    print("\n2. Testing orders for shop S005:")
    shop5_orders = om.get_shop_orders("S005")
    for order in shop5_orders:
        print(f"   Order ID: {order.order_id}, User ID: {order.user_id}, Shop ID: {order.shop_id}, Dish: {order.dish_name}, Status: {order.status}")
    
    print("\n3. Testing orders for shop S002:")
    shop2_orders = om.get_shop_orders("S002")
    if not shop2_orders:
        print("   No orders found for shop S002")
    else:
        for order in shop2_orders:
            print(f"   Order ID: {order.order_id}, User ID: {order.user_id}, Shop ID: {order.shop_id}, Dish: {order.dish_name}, Status: {order.status}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_shop_orders()