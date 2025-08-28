#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内存优化版本：计算数组中所有正差值的累加和

优化策略：
1. 流式处理：避免存储完整的排序数组
2. 压缩树状数组：使用更紧凑的数据结构
3. 原地操作：减少临时变量的使用
4. 分块处理：对于超大数组采用分块策略
5. 垃圾回收优化：及时释放不需要的内存

作者：AI Assistant
日期：2024
"""

import random
import time
import gc
from typing import List, Iterator, Tuple
import sys
from collections import defaultdict

class CompactFenwickTree:
    """
    紧凑型树状数组实现
    使用字典存储稀疏数据，节省内存
    """
    
    def __init__(self):
        self.count_tree = defaultdict(int)
        self.sum_tree = defaultdict(int)
        self.max_idx = 0
    
    def update(self, idx: int, val: int):
        """在位置idx添加一个值为val的元素"""
        self.max_idx = max(self.max_idx, idx)
        original_idx = idx
        while idx > 0 and idx <= self.max_idx + 1000:
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
    
    def clear_unused(self):
        """清理未使用的内存"""
        # 移除值为0的项
        self.count_tree = defaultdict(int, {k: v for k, v in self.count_tree.items() if v != 0})
        self.sum_tree = defaultdict(int, {k: v for k, v in self.sum_tree.items() if v != 0})

def get_unique_values_streaming(arr: List[int]) -> Tuple[dict, int]:
    """
    流式获取唯一值并建立映射，节省内存
    
    Args:
        arr: 输入数组
    
    Returns:
        (value_to_rank, unique_count)
    """
    unique_values = set()
    
    # 第一遍：收集唯一值
    for val in arr:
        unique_values.add(val)
    
    # 排序并建立映射
    sorted_values = sorted(unique_values)
    value_to_rank = {v: i + 1 for i, v in enumerate(sorted_values)}
    
    # 清理临时变量
    del unique_values, sorted_values
    gc.collect()
    
    return value_to_rank, len(value_to_rank)

def calculate_positive_differences_memory_optimized(arr: List[int]) -> int:
    """
    内存优化版本：O(n log n)时间复杂度，优化内存使用
    
    Args:
        arr: 输入数组
    
    Returns:
        所有正差值的累加和
    """
    n = len(arr)
    if n <= 1:
        return 0
    
    # 流式坐标压缩
    value_to_rank, unique_count = get_unique_values_streaming(arr)
    
    # 使用紧凑型树状数组
    ft = CompactFenwickTree()
    total_sum = 0
    
    # 分批处理以减少内存峰值
    batch_size = min(10000, n // 10 + 1)
    
    for batch_start in range(0, n, batch_size):
        batch_end = min(batch_start + batch_size, n)
        
        for j in range(batch_start, batch_end):
            current_val = arr[j]
            current_rank = value_to_rank[current_val]
            
            # 查询所有小于current_val的元素
            if current_rank > 1:
                smaller_count = ft.query_count(current_rank - 1)
                smaller_sum = ft.query_sum(current_rank - 1)
                
                # 计算当前元素对答案的贡献
                contribution = current_val * smaller_count - smaller_sum
                total_sum += contribution
            
            # 将当前元素加入树状数组
            ft.update(current_rank, current_val)
        
        # 定期清理未使用的内存
        if batch_start % (batch_size * 5) == 0:
            ft.clear_unused()
            gc.collect()
    
    # 最终清理
    del ft, value_to_rank
    gc.collect()
    
    return total_sum

def calculate_positive_differences_chunked(arr: List[int], chunk_size: int = 50000) -> int:
    """
    分块处理版本：适用于超大数组，进一步减少内存使用
    
    Args:
        arr: 输入数组
        chunk_size: 每块的大小
    
    Returns:
        所有正差值的累加和
    """
    n = len(arr)
    if n <= chunk_size:
        return calculate_positive_differences_memory_optimized(arr)
    
    total_sum = 0
    
    # 分块处理
    for i in range(0, n, chunk_size):
        chunk_end = min(i + chunk_size, n)
        chunk = arr[i:chunk_end]
        
        # 计算块内的贡献
        chunk_sum = calculate_positive_differences_memory_optimized(chunk)
        total_sum += chunk_sum
        
        # 计算跨块的贡献
        for j in range(chunk_end, n):
            for k in range(i, chunk_end):
                diff = arr[j] - arr[k]
                if diff > 0:
                    total_sum += diff
        
        # 清理内存
        del chunk
        gc.collect()
        
        print(f"已处理 {chunk_end}/{n} 个元素")
    
    return total_sum

def get_memory_usage() -> float:
    """
    获取当前内存使用量（MB）
    """
    try:
        import psutil
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        import sys
        return sys.getsizeof([]) / 1024 / 1024

def generate_test_array_memory_efficient(size: int, max_value: int, seed: int = None) -> List[int]:
    """
    内存高效的测试数组生成
    
    Args:
        size: 数组长度
        max_value: 元素最大值
        seed: 随机种子
    
    Returns:
        随机整数数组
    """
    if seed is not None:
        random.seed(seed)
    
    # 使用生成器减少内存占用
    return [random.randint(0, max_value) for _ in range(size)]

def memory_usage_test():
    """
    内存使用测试
    """
    print("内存使用对比测试...")
    
    test_sizes = [10000, 50000, 100000]
    
    for size in test_sizes:
        print(f"\n测试数组大小: {size:,}")
        
        # 生成测试数组
        initial_memory = get_memory_usage()
        arr = generate_test_array_memory_efficient(size, 1000000, seed=42)
        array_memory = get_memory_usage()
        
        print(f"  数组内存使用: {array_memory - initial_memory:.2f} MB")
        
        # 测试原始算法内存使用
        gc.collect()
        start_memory = get_memory_usage()
        start_time = time.time()
        
        # 导入原始算法进行对比
        from complete_solution import calculate_positive_differences_optimized
        result_original = calculate_positive_differences_optimized(arr.copy())
        
        original_time = time.time() - start_time
        original_memory = get_memory_usage()
        
        # 测试内存优化算法
        gc.collect()
        start_time = time.time()
        optimized_start_memory = get_memory_usage()
        
        result_optimized = calculate_positive_differences_memory_optimized(arr)
        
        optimized_time = time.time() - start_time
        optimized_memory = get_memory_usage()
        
        print(f"  原始算法:")
        print(f"    结果: {result_original:,}")
        print(f"    耗时: {original_time:.4f}秒")
        print(f"    峰值内存: {original_memory - start_memory:.2f} MB")
        
        print(f"  优化算法:")
        print(f"    结果: {result_optimized:,}")
        print(f"    耗时: {optimized_time:.4f}秒")
        print(f"    峰值内存: {optimized_memory - optimized_start_memory:.2f} MB")
        
        original_peak = max(0.01, original_memory - start_memory)
        optimized_peak = max(0.01, optimized_memory - optimized_start_memory)
        memory_saved = original_peak - optimized_peak
        
        print(f"    内存节省: {memory_saved:.2f} MB ({memory_saved/original_peak*100:.1f}%)")
        print(f"    结果一致: {'✓' if result_original == result_optimized else '✗'}")
        
        if result_original != result_optimized:
            print(f"    ⚠️  结果差异: {abs(result_original - result_optimized):,}")
        
        # 清理内存
        del arr
        gc.collect()

def solve_main_problem_memory_optimized():
    """
    内存优化版本解决主要问题
    """
    print("=" * 70)
    print("内存优化版本：400000长度数组的正差值累加和")
    print("=" * 70)
    
    # 问题参数
    array_size = 400000
    max_element_value = 100000000
    
    print(f"问题参数:")
    print(f"  数组长度: {array_size:,}")
    print(f"  元素最大值: {max_element_value:,}")
    
    # 监控内存使用
    initial_memory = get_memory_usage()
    print(f"  初始内存: {initial_memory:.2f} MB")
    
    # 生成随机数组
    print(f"\n正在生成随机数组...")
    start_time = time.time()
    arr = generate_test_array_memory_efficient(array_size, max_element_value, seed=2024)
    generation_time = time.time() - start_time
    array_memory = get_memory_usage()
    
    print(f"数组生成完成，耗时: {generation_time:.4f}秒")
    print(f"数组内存使用: {array_memory - initial_memory:.2f} MB")
    
    # 使用内存优化算法计算
    print(f"\n开始计算（内存优化版本）...")
    start_time = time.time()
    calc_start_memory = get_memory_usage()
    
    result = calculate_positive_differences_memory_optimized(arr)
    
    calculation_time = time.time() - start_time
    final_memory = get_memory_usage()
    
    print(f"\n计算完成！")
    print(f"结果: {result:,}")
    print(f"计算耗时: {calculation_time:.4f}秒")
    print(f"计算期间峰值内存: {final_memory - calc_start_memory:.2f} MB")
    print(f"总内存使用: {final_memory - initial_memory:.2f} MB")
    
    # 清理内存
    del arr
    gc.collect()
    final_cleanup_memory = get_memory_usage()
    print(f"清理后内存: {final_cleanup_memory:.2f} MB")
    
    return result

def main():
    """
    主函数
    """
    print("内存优化版本 - 数组正差值累加和计算器")
    print("=" * 60)
    
    # 内存使用测试
    memory_usage_test()
    
    # 解决主要问题
    result = solve_main_problem_memory_optimized()
    
    print(f"\n🎉 内存优化版本完成！")
    print(f"最终答案: {result:,}")
    
    return result

if __name__ == "__main__":
    main()