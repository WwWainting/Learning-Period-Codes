"""
菜品管理模块 - 实现菜品的添加、浏览、更新、删除等功能（支持多店家）
"""

from shop.dish.dish import DishManagement

def dish_menu(shop_name: str, shop_id: str):
    """
    菜品管理主菜单（基于店家ID）
    Args:
        shop_name: 店家名称，用于显示
        shop_id: 店家ID，用于关联独立菜单
    """
    dm = DishManagement(shop_id)
    
    while True:
        print(f"\n{'='*50}")
        print(f"        {shop_name} (ID: {shop_id}) - 菜品管理")
        print(f"{'='*50}")
        print("1. 添加菜品")
        print("2. 浏览所有菜品")
        print("3. 查找菜品")
        print("4. 更新菜品信息")
        print("5. 删除菜品")
        print("6. 按类别浏览菜品")
        print("7. 查看菜单统计")
        print("0. 返回上一级")
        print(f"{'='*50}")
        
        choice = input("请选择操作: ").strip()
        
        if choice == "1":
            add_dish(dm)
        elif choice == "2":
            browse_all_dishes(dm)
        elif choice == "3":
            search_dish(dm)
        elif choice == "4":
            update_dish(dm)
        elif choice == "5":
            delete_dish(dm)
        elif choice == "6":
            browse_by_category(dm)
        elif choice == "7":
            show_menu_stats(dm)
        elif choice == "0":
            print("退出菜品管理")
            break
        else:
            print("输入无效，请重新选择")
        
        input("\n按回车键继续...")

def add_dish(dm: DishManagement):
    """添加菜品"""
    print("\n--- 添加新菜品 ---")
    name = input("请输入菜品名称: ").strip()
    if not name:
        print("菜品名称不能为空")
        return
    
    # 检查菜品是否已存在
    existing_dish = dm.get_dish_by_name(name)
    if existing_dish:
        print(f"菜品'{name}'已存在，ID为{existing_dish.id}")
        return
    
    price = input("请输入菜品价格: ").strip()
    if not price:
        print("价格不能为空")
        return
    
    # 验证价格格式
    try:
        float(price)
    except ValueError:
        print("价格格式不正确，请输入数字")
        return
    
    category = input("请输入菜品类别 (如: 热菜、凉菜、汤类、饮料、主食): ").strip()
    if not category:
        print("类别不能为空")
        return
    
    description = input("请输入菜品描述: ").strip()
    if not description:
        print("描述不能为空")
        return
    
    success = dm.add_dish(name, price, category, description)
    if success:
        print(f"菜品'{name}'添加成功！")
    else:
        print("菜品添加失败！")

def browse_all_dishes(dm: DishManagement):
    """浏览所有菜品"""
    print(f"\n--- 店家 {dm.shop_id} 的所有菜品列表 ---")
    dishes = dm.list_all_dishes()
    
    if not dishes:
        print("暂无菜品数据")
        return
    
    print(f"{'ID':<4} {'菜品名称':<15} {'价格':<8} {'类别':<8} {'描述':<20}")
    print("-" * 70)
    
    for dish in dishes:
        print(f"{dish.id:<4} {dish.name:<15} {dish.price:<8} {dish.category:<8} {dish.description:<20}")
    
    print(f"\n总计: {len(dishes)} 道菜品")
    print(f"菜单文件: {dm.get_csv_file_path()}")

def search_dish(dm: DishManagement):
    """查找菜品"""
    print("\n--- 查找菜品 ---")
    print("1. 按菜品名称查找")
    print("2. 按菜品ID查找")
    choice = input("请选择查找方式: ").strip()
    
    if choice == "1":
        name = input("请输入菜品名称: ").strip()
        if not name:
            print("菜品名称不能为空")
            return
        
        dish = dm.get_dish_by_name(name)
        if dish:
            print(f"\n找到菜品:")
            print(f"ID: {dish.id}")
            print(f"名称: {dish.name}")
            print(f"价格: {dish.price}")
            print(f"类别: {dish.category}")
            print(f"描述: {dish.description}")
        else:
            print(f"未找到名为'{name}'的菜品")
    
    elif choice == "2":
        dish_id = input("请输入菜品ID: ").strip()
        if not dish_id:
            print("菜品ID不能为空")
            return
        
        dish = dm.get_dish_by_id(dish_id)
        if dish:
            print(f"\n找到菜品:")
            print(f"ID: {dish.id}")
            print(f"名称: {dish.name}")
            print(f"价格: {dish.price}")
            print(f"类别: {dish.category}")
            print(f"描述: {dish.description}")
        else:
            print(f"未找到ID为'{dish_id}'的菜品")
    
    else:
        print("无效选择")

def update_dish(dm: DishManagement):
    """更新菜品信息"""
    print("\n--- 更新菜品信息 ---")
    dish_id = input("请输入要更新的菜品ID: ").strip()
    
    if not dish_id:
        print("菜品ID不能为空")
        return
    
    # 先查看菜品是否存在
    dish = dm.get_dish_by_id(dish_id)
    if not dish:
        print(f"未找到ID为'{dish_id}'的菜品")
        return
    
    print(f"当前菜品信息:")
    print(f"ID: {dish.id}")
    print(f"名称: {dish.name}")
    print(f"价格: {dish.price}")
    print(f"类别: {dish.category}")
    print(f"描述: {dish.description}")
    
    print("\n请输入新的信息 (直接回车保持原值):")
    
    name = input(f"新名称 [{dish.name}]: ").strip()
    price = input(f"新价格 [{dish.price}]: ").strip()
    category = input(f"新类别 [{dish.category}]: ").strip()
    description = input(f"新描述 [{dish.description}]: ").strip()
    
    # 构建更新参数
    update_params = {}
    if name:
        update_params['name'] = name
    if price:
        # 验证价格格式
        try:
            float(price)
            update_params['price'] = price
        except ValueError:
            print("价格格式不正确，保持原值")
    if category:
        update_params['category'] = category
    if description:
        update_params['description'] = description
    
    if update_params:
        success = dm.update_dish_info(dish_id, **update_params)
        if success:
            print("菜品信息更新成功！")
        else:
            print("菜品信息更新失败！")
    else:
        print("没有更新任何信息")

def delete_dish(dm: DishManagement):
    """删除菜品"""
    print("\n--- 删除菜品 ---")
    dish_id = input("请输入要删除的菜品ID: ").strip()
    
    if not dish_id:
        print("菜品ID不能为空")
        return
    
    # 先查看菜品是否存在
    dish = dm.get_dish_by_id(dish_id)
    if not dish:
        print(f"未找到ID为'{dish_id}'的菜品")
        return
    
    print(f"即将删除菜品: {dish.name}")
    confirm = input("确认删除吗？(y/N): ").strip().lower()
    
    if confirm == 'y' or confirm == 'yes':
        success = dm.delete_dish(dish_id)
        if success:
            print("菜品删除成功！")
        else:
            print("菜品删除失败！")
    else:
        print("取消删除操作")

def browse_by_category(dm: DishManagement):
    """按类别浏览菜品"""
    print("\n--- 按类别浏览菜品 ---")
    
    # 获取所有菜品
    dishes = dm.list_all_dishes()
    if not dishes:
        print("暂无菜品数据")
        return
    
    # 统计各类别
    categories = {}
    for dish in dishes:
        if dish.category not in categories:
            categories[dish.category] = []
        categories[dish.category].append(dish)
    
    # 显示类别列表
    print("可用类别:")
    for i, category in enumerate(categories.keys(), 1):
        print(f"{i}. {category} ({len(categories[category])}道菜)")
    
    choice = input("请选择类别编号 (直接回车显示所有): ").strip()
    
    if choice:
        try:
            category_index = int(choice) - 1
            category_list = list(categories.keys())
            if 0 <= category_index < len(category_list):
                selected_category = category_list[category_index]
                dishes_to_show = categories[selected_category]
                print(f"\n--- {selected_category} 类菜品 ---")
            else:
                print("无效选择")
                return
        except ValueError:
            print("无效输入")
            return
    else:
        dishes_to_show = dishes
        print("\n--- 所有菜品 ---")
    
    # 显示菜品
    print(f"{'ID':<4} {'菜品名称':<15} {'价格':<8} {'描述':<20}")
    print("-" * 60)
    
    for dish in dishes_to_show:
        print(f"{dish.id:<4} {dish.name:<15} {dish.price:<8} {dish.description:<20}")
    
    print(f"\n显示: {len(dishes_to_show)} 道菜品")

def show_menu_stats(dm: DishManagement):
    """显示菜单统计信息"""
    print(f"\n--- 店家 {dm.shop_id} 菜单统计 ---")
    
    dishes = dm.list_all_dishes()
    if not dishes:
        print("暂无菜品数据")
        return
    
    # 统计各类别数量
    categories = {}
    total_value = 0.0
    
    for dish in dishes:
        # 类别统计
        if dish.category not in categories:
            categories[dish.category] = 0
        categories[dish.category] += 1
        
        # 总价值统计
        try:
            total_value += float(dish.price)
        except ValueError:
            pass
    
    # 显示统计信息
    print(f"菜品总数: {len(dishes)}")
    print(f"菜单总价值: {total_value:.2f} 元")
    
    print("\n各类别分布:")
    for category, count in categories.items():
        percentage = (count / len(dishes)) * 100
        print(f"  {category}: {count}道 ({percentage:.1f}%)")
    
    print(f"\n菜单文件路径: {dm.get_csv_file_path()}")


# 测试代码
if __name__ == "__main__":
    print("菜品管理系统测试")
    dish_menu("测试店家", "S001")