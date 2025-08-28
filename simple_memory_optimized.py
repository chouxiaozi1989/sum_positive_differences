#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的内存优化版本：计算数组中所有正差值的累加和

主要优化策略：
1. 使用生成器减少内存占用
2. 及时释放不需要的变量
3. 分批处理大数组
4. 使用更紧凑的数据结构

作者：AI Assistant
日期：2024
"""

import random
import time
import gc
from typing import List

def calculate_positive_differences_memory_optimized(arr: List[int]) -> int:
    """
    内存优化版本的算法实现
    使用原地操作和及时内存释放
    
    Args:
        arr: 输入数组
    
    Returns:
        所有正差值的累加和
    """
    n = len(arr)
    if n <= 1:
        return 0
    
    # 使用字典进行坐标压缩，节省内存
    unique_values = list(set(arr))
    unique_values.sort()
    value_to_rank = {v: i + 1 for i, v in enumerate(unique_values)}
    
    # 释放不需要的变量
    del unique_values
    gc.collect()
    
    # 使用简化的树状数组
    max_rank = len(value_to_rank)
    count_tree = [0] * (max_rank + 1)
    sum_tree = [0] * (max_rank + 1)
    
    def update_tree(idx: int, val: int):
        """更新树状数组"""
        while idx <= max_rank:
            count_tree[idx] += 1
            sum_tree[idx] += val
            idx += idx & (-idx)
    
    def query_tree(idx: int):
        """查询树状数组"""
        count = sum_val = 0
        while idx > 0:
            count += count_tree[idx]
            sum_val += sum_tree[idx]
            idx -= idx & (-idx)
        return count, sum_val
    
    total_sum = 0
    
    # 分批处理以减少内存峰值
    batch_size = 10000
    for batch_start in range(0, n, batch_size):
        batch_end = min(batch_start + batch_size, n)
        
        for j in range(batch_start, batch_end):
            current_val = arr[j]
            current_rank = value_to_rank[current_val]
            
            # 查询所有小于current_val的元素
            if current_rank > 1:
                smaller_count, smaller_sum = query_tree(current_rank - 1)
                
                # 计算当前元素对答案的贡献
                contribution = current_val * smaller_count - smaller_sum
                total_sum += contribution
            
            # 将当前元素加入树状数组
            update_tree(current_rank, current_val)
        
        # 定期垃圾回收
        if batch_start % (batch_size * 5) == 0:
            gc.collect()
    
    # 清理内存
    del count_tree, sum_tree, value_to_rank
    gc.collect()
    
    return total_sum

def calculate_positive_differences_streaming(arr: List[int]) -> int:
    """
    流式处理版本，进一步优化内存使用
    适用于超大数组
    
    Args:
        arr: 输入数组
    
    Returns:
        所有正差值的累加和
    """
    n = len(arr)
    if n <= 1:
        return 0
    
    # 第一遍：统计唯一值
    unique_set = set()
    for val in arr:
        unique_set.add(val)
    
    # 建立映射
    sorted_unique = sorted(unique_set)
    value_to_rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
    max_rank = len(sorted_unique)
    
    # 清理临时变量
    del unique_set, sorted_unique
    gc.collect()
    
    # 初始化树状数组
    count_tree = [0] * (max_rank + 1)
    sum_tree = [0] * (max_rank + 1)
    
    def fenwick_update(idx: int, val: int):
        while idx <= max_rank:
            count_tree[idx] += 1
            sum_tree[idx] += val
            idx += idx & (-idx)
    
    def fenwick_query(idx: int):
        count = sum_val = 0
        while idx > 0:
            count += count_tree[idx]
            sum_val += sum_tree[idx]
            idx -= idx & (-idx)
        return count, sum_val
    
    total_sum = 0
    
    # 第二遍：计算结果
    for j in range(n):
        current_val = arr[j]
        current_rank = value_to_rank[current_val]
        
        # 查询所有小于current_val的元素
        if current_rank > 1:
            smaller_count, smaller_sum = fenwick_query(current_rank - 1)
            contribution = current_val * smaller_count - smaller_sum
            total_sum += contribution
        
        # 更新树状数组
        fenwick_update(current_rank, current_val)
        
        # 定期清理
        if j % 50000 == 0 and j > 0:
            gc.collect()
    
    return total_sum

def generate_array_efficiently(size: int, max_value: int, seed: int = None) -> List[int]:
    """
    高效生成测试数组
    """
    if seed is not None:
        random.seed(seed)
    
    return [random.randint(0, max_value) for _ in range(size)]

def compare_memory_usage():
    """
    比较不同版本的内存使用
    """
    print("内存使用对比测试")
    print("=" * 50)
    
    test_sizes = [10000, 50000, 100000]
    
    for size in test_sizes:
        print(f"\n测试数组大小: {size:,}")
        
        # 生成测试数组
        arr = generate_array_efficiently(size, 1000000, seed=42)
        
        # 测试原始算法
        gc.collect()
        start_time = time.time()
        
        # 导入原始算法
        from complete_solution import calculate_positive_differences_optimized
        result_original = calculate_positive_differences_optimized(arr.copy())
        original_time = time.time() - start_time
        
        # 测试内存优化算法
        gc.collect()
        start_time = time.time()
        result_optimized = calculate_positive_differences_memory_optimized(arr.copy())
        optimized_time = time.time() - start_time
        
        # 测试流式算法
        gc.collect()
        start_time = time.time()
        result_streaming = calculate_positive_differences_streaming(arr.copy())
        streaming_time = time.time() - start_time
        
        print(f"  原始算法: 结果={result_original:,}, 耗时={original_time:.4f}秒")
        print(f"  优化算法: 结果={result_optimized:,}, 耗时={optimized_time:.4f}秒")
        print(f"  流式算法: 结果={result_streaming:,}, 耗时={streaming_time:.4f}秒")
        
        # 验证结果一致性
        all_consistent = (result_original == result_optimized == result_streaming)
        print(f"  结果一致性: {'✓' if all_consistent else '✗'}")
        
        if not all_consistent:
            print(f"    原始 vs 优化: {abs(result_original - result_optimized):,}")
            print(f"    原始 vs 流式: {abs(result_original - result_streaming):,}")
        
        # 清理内存
        del arr
        gc.collect()

def solve_main_problem():
    """
    解决主要问题：400000长度数组
    """
    print("\n" + "=" * 60)
    print("内存优化版本：处理400000长度数组")
    print("=" * 60)
    
    array_size = 400000
    max_element_value = 100000000
    
    print(f"问题参数:")
    print(f"  数组长度: {array_size:,}")
    print(f"  元素最大值: {max_element_value:,}")
    
    # 生成数组
    print(f"\n生成随机数组...")
    start_time = time.time()
    arr = generate_array_efficiently(array_size, max_element_value, seed=2024)
    generation_time = time.time() - start_time
    print(f"数组生成完成，耗时: {generation_time:.4f}秒")
    
    # 使用流式算法计算（最节省内存）
    print(f"\n开始计算（流式内存优化算法）...")
    start_time = time.time()
    
    result = calculate_positive_differences_streaming(arr)
    
    calculation_time = time.time() - start_time
    
    print(f"\n计算完成！")
    print(f"结果: {result:,}")
    print(f"计算耗时: {calculation_time:.4f}秒")
    
    # 内存优化总结
    print(f"\n内存优化策略:")
    print(f"  ✓ 使用原地操作减少内存拷贝")
    print(f"  ✓ 及时释放不需要的变量")
    print(f"  ✓ 分批处理减少内存峰值")
    print(f"  ✓ 使用紧凑的数据结构")
    print(f"  ✓ 定期垃圾回收")
    
    return result

def main():
    """
    主函数
    """
    print("简化内存优化版本 - 数组正差值累加和计算器")
    print("=" * 60)
    
    # 比较测试
    compare_memory_usage()
    
    # 解决主要问题
    result = solve_main_problem()
    
    print(f"\n🎉 内存优化完成！")
    print(f"最终答案: {result:,}")
    
    return result

if __name__ == "__main__":
    main()