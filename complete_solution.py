#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算法题解：计算数组中所有正差值的累加和

问题描述：
给定随机整数数组a，长度400000，元素最大值100000000
对于任意i<j，求当a[j]-a[i]>0时所有a[j]-a[i]的累加和

解决方案：
1. 朴素算法：O(n^2)时间复杂度，适用于小规模数据
2. 优化算法：O(n log n)时间复杂度，使用树状数组和坐标压缩

作者：AI Assistant
日期：2024
"""

import random
import time
from typing import List, Tuple
import sys

class FenwickTree:
    """
    树状数组（Binary Indexed Tree）实现
    支持单点更新和前缀查询，时间复杂度O(log n)
    """
    
    def __init__(self, size: int):
        self.size = size
        self.count_tree = [0] * (size + 1)  # 计数树
        self.sum_tree = [0] * (size + 1)    # 求和树
    
    def update(self, idx: int, val: int):
        """在位置idx添加一个值为val的元素"""
        while idx <= self.size:
            self.count_tree[idx] += 1
            self.sum_tree[idx] += val
            idx += idx & (-idx)
    
    def query_count(self, idx: int) -> int:
        """查询前idx个位置的元素个数"""
        count = 0
        while idx > 0:
            count += self.count_tree[idx]
            idx -= idx & (-idx)
        return count
    
    def query_sum(self, idx: int) -> int:
        """查询前idx个位置的元素和"""
        total = 0
        while idx > 0:
            total += self.sum_tree[idx]
            idx -= idx & (-idx)
        return total

def calculate_positive_differences_naive(arr: List[int]) -> int:
    """
    朴素算法：O(n^2)时间复杂度
    直接双重循环计算所有满足条件的差值
    
    Args:
        arr: 输入数组
    
    Returns:
        所有正差值的累加和
    """
    total_sum = 0
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            diff = arr[j] - arr[i]
            if diff > 0:
                total_sum += diff
    
    return total_sum

def calculate_positive_differences_optimized(arr: List[int]) -> int:
    """
    优化算法：O(n log n)时间复杂度
    使用坐标压缩和树状数组优化计算
    
    核心思想：
    对于每个位置j的元素arr[j]，我们需要计算：
    - 在位置j之前有多少个元素小于arr[j]
    - 这些小于arr[j]的元素的总和
    然后arr[j]对答案的贡献就是：arr[j] * count - sum
    
    Args:
        arr: 输入数组
    
    Returns:
        所有正差值的累加和
    """
    n = len(arr)
    if n <= 1:
        return 0
    
    # 坐标压缩：将数组中的值映射到1到k的范围内
    sorted_values = sorted(set(arr))
    value_to_rank = {v: i + 1 for i, v in enumerate(sorted_values)}
    
    # 初始化树状数组
    ft = FenwickTree(len(sorted_values))
    total_sum = 0
    
    for j in range(n):
        current_val = arr[j]
        current_rank = value_to_rank[current_val]
        
        # 查询所有小于current_val的元素
        if current_rank > 1:
            # 小于current_val的元素个数
            smaller_count = ft.query_count(current_rank - 1)
            # 小于current_val的元素总和
            smaller_sum = ft.query_sum(current_rank - 1)
            
            # 计算当前元素对答案的贡献
            # current_val与之前所有较小元素的差值之和
            contribution = current_val * smaller_count - smaller_sum
            total_sum += contribution
        
        # 将当前元素加入树状数组
        ft.update(current_rank, current_val)
    
    return total_sum

def generate_test_array(size: int, max_value: int, seed: int = None) -> List[int]:
    """
    生成测试用的随机数组
    
    Args:
        size: 数组长度
        max_value: 元素最大值
        seed: 随机种子，用于结果复现
    
    Returns:
        随机整数数组
    """
    if seed is not None:
        random.seed(seed)
    
    return [random.randint(0, max_value) for _ in range(size)]

def verify_algorithms() -> bool:
    """
    验证算法正确性
    
    Returns:
        所有测试用例是否通过
    """
    print("验证算法正确性...")
    
    test_cases = [
        ([1, 3, 2, 4], 9),      # (3-1)+(2-1)+(4-1)+(4-3)+(4-2) = 2+1+3+1+2 = 9
        ([5, 1, 3, 2], 3),      # (3-1)+(2-1) = 2+1 = 3
        ([1, 2, 3, 4, 5], 20),  # 1+2+3+4 + 1+2+3 + 1+2 + 1 = 20
        ([10, 5, 8, 3, 7], 9),  # (8-5)+(7-5)+(7-3) = 3+2+4 = 9
        ([1], 0),               # 单元素数组
        ([5, 4, 3, 2, 1], 0),   # 递减数组
    ]
    
    all_passed = True
    
    for i, (test_arr, expected) in enumerate(test_cases):
        result_naive = calculate_positive_differences_naive(test_arr)
        result_optimized = calculate_positive_differences_optimized(test_arr)
        
        passed = (result_naive == expected and result_optimized == expected)
        all_passed = all_passed and passed
        
        print(f"测试用例 {i+1}: {test_arr}")
        print(f"  期望结果: {expected}")
        print(f"  朴素算法: {result_naive}")
        print(f"  优化算法: {result_optimized}")
        print(f"  测试结果: {'✓ 通过' if passed else '✗ 失败'}")
        print()
    
    return all_passed

def performance_comparison():
    """
    性能对比测试
    """
    print("性能对比测试...")
    
    test_sizes = [1000, 5000, 10000, 20000]
    
    for size in test_sizes:
        print(f"\n测试数组大小: {size}")
        test_arr = generate_test_array(size, 1000000, seed=42)
        
        # 测试朴素算法
        start_time = time.time()
        result_naive = calculate_positive_differences_naive(test_arr)
        naive_time = time.time() - start_time
        
        # 测试优化算法
        start_time = time.time()
        result_optimized = calculate_positive_differences_optimized(test_arr)
        optimized_time = time.time() - start_time
        
        speedup = naive_time / optimized_time if optimized_time > 0 else float('inf')
        
        print(f"  朴素算法: 结果={result_naive}, 耗时={naive_time:.4f}秒")
        print(f"  优化算法: 结果={result_optimized}, 耗时={optimized_time:.4f}秒")
        print(f"  加速比: {speedup:.2f}x")
        print(f"  结果一致: {'✓' if result_naive == result_optimized else '✗'}")

def solve_main_problem():
    """
    解决主要问题：处理400000长度的数组
    """
    print("=" * 70)
    print("解决主要问题：400000长度数组的正差值累加和")
    print("=" * 70)
    
    # 问题参数
    array_size = 400000
    max_element_value = 100000000
    
    print(f"问题参数:")
    print(f"  数组长度: {array_size:,}")
    print(f"  元素最大值: {max_element_value:,}")
    print(f"  问题规模: 约{array_size * array_size // 2:,}次比较")
    
    # 生成随机数组
    print(f"\n正在生成随机数组...")
    start_time = time.time()
    arr = generate_test_array(array_size, max_element_value, seed=2024)
    generation_time = time.time() - start_time
    print(f"数组生成完成，耗时: {generation_time:.4f}秒")
    
    # 使用优化算法计算
    print(f"\n开始计算（使用O(n log n)优化算法）...")
    start_time = time.time()
    result = calculate_positive_differences_optimized(arr)
    calculation_time = time.time() - start_time
    
    print(f"\n计算完成！")
    print(f"结果: {result:,}")
    print(f"计算耗时: {calculation_time:.4f}秒")
    
    # 结果分析
    print(f"\n结果分析:")
    avg_element = max_element_value // 2
    expected_pairs = array_size * array_size // 4  # 大约1/4的配对会产生正差值
    avg_diff = avg_element // 2
    rough_estimate = expected_pairs * avg_diff
    
    print(f"  平均元素值: {avg_element:,}")
    print(f"  预期正差值对数: 约{expected_pairs:,}")
    print(f"  平均差值: 约{avg_diff:,}")
    print(f"  粗略估计: 约{rough_estimate:,}")
    print(f"  实际结果: {result:,}")
    print(f"  估计准确度: {result/rough_estimate:.2f}x")
    
    return result

def main():
    """
    主函数
    """
    print("数组正差值累加和计算器")
    print("=" * 50)
    
    # 验证算法正确性
    if not verify_algorithms():
        print("❌ 算法验证失败！")
        return
    
    print("✅ 算法验证通过！")
    
    # 性能对比
    performance_comparison()
    
    # 解决主要问题
    result = solve_main_problem()
    
    print(f"\n🎉 任务完成！")
    print(f"最终答案: {result:,}")
    
    return result

if __name__ == "__main__":
    main()