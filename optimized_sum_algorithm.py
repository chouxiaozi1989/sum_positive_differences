import random
import time
from typing import List

def calculate_positive_differences_sum_efficient(arr: List[int]) -> int:
    """
    高效算法：O(n log n)时间复杂度
    使用归并排序的思想，在合并过程中计算贡献
    
    核心思想：
    对于每个元素arr[j]，计算有多少个在它之前的元素arr[i] (i<j) 满足arr[j] > arr[i]
    以及这些差值的总和
    """
    n = len(arr)
    if n <= 1:
        return 0
    
    # 创建索引数组，保持原始位置信息
    indexed_arr = [(arr[i], i) for i in range(n)]
    
    total_sum = 0
    
    def merge_and_count(left_half, right_half):
        nonlocal total_sum
        merged = []
        i = j = 0
        
        while i < len(left_half) and j < len(right_half):
            left_val, left_idx = left_half[i]
            right_val, right_idx = right_half[j]
            
            if left_idx < right_idx:  # 保证i < j的条件
                if right_val > left_val:  # arr[j] - arr[i] > 0
                    # right_val会与left_half中所有剩余元素形成正差值
                    for k in range(i, len(left_half)):
                        if left_half[k][1] < right_idx:  # 确保索引条件
                            diff = right_val - left_half[k][0]
                            if diff > 0:
                                total_sum += diff
                merged.append(right_half[j])
                j += 1
            else:
                merged.append(left_half[i])
                i += 1
        
        merged.extend(left_half[i:])
        merged.extend(right_half[j:])
        return merged
    
    def merge_sort_with_count(arr_segment):
        if len(arr_segment) <= 1:
            return arr_segment
        
        mid = len(arr_segment) // 2
        left = merge_sort_with_count(arr_segment[:mid])
        right = merge_sort_with_count(arr_segment[mid:])
        
        return merge_and_count(left, right)
    
    # 由于上述归并方法复杂度较高，我们使用更直接的优化方法
    # 使用Fenwick Tree (Binary Indexed Tree) 来优化
    return calculate_with_coordinate_compression(arr)

def calculate_with_coordinate_compression(arr: List[int]) -> int:
    """
    使用坐标压缩和树状数组的高效算法
    时间复杂度: O(n log n)
    """
    n = len(arr)
    if n <= 1:
        return 0
    
    # 坐标压缩
    sorted_values = sorted(set(arr))
    value_to_rank = {v: i + 1 for i, v in enumerate(sorted_values)}
    
    # Fenwick Tree for counting and sum
    class FenwickTree:
        def __init__(self, size):
            self.size = size
            self.count_tree = [0] * (size + 1)
            self.sum_tree = [0] * (size + 1)
        
        def update(self, idx, val):
            while idx <= self.size:
                self.count_tree[idx] += 1
                self.sum_tree[idx] += val
                idx += idx & (-idx)
        
        def query_count(self, idx):
            count = 0
            while idx > 0:
                count += self.count_tree[idx]
                idx -= idx & (-idx)
            return count
        
        def query_sum(self, idx):
            total = 0
            while idx > 0:
                total += self.sum_tree[idx]
                idx -= idx & (-idx)
            return total
    
    ft = FenwickTree(len(sorted_values))
    total_sum = 0
    
    for j in range(n):
        current_val = arr[j]
        current_rank = value_to_rank[current_val]
        
        # 查询所有小于current_val的元素
        if current_rank > 1:
            smaller_count = ft.query_count(current_rank - 1)
            smaller_sum = ft.query_sum(current_rank - 1)
            
            # 计算当前元素与之前所有较小元素的正差值之和
            contribution = current_val * smaller_count - smaller_sum
            total_sum += contribution
        
        # 将当前元素加入树状数组
        ft.update(current_rank, current_val)
    
    return total_sum

def calculate_positive_differences_sum_simple_optimized(arr: List[int]) -> int:
    """
    简化的优化算法：通过数学方法减少计算量
    对于大数组仍然是O(n^2)，但有常数优化
    """
    n = len(arr)
    total_sum = 0
    
    # 对每个位置j，计算所有i<j且arr[j]>arr[i]的差值和
    for j in range(1, n):
        current = arr[j]
        for i in range(j):
            if current > arr[i]:
                total_sum += current - arr[i]
    
    return total_sum

def generate_random_array(size: int, max_value: int) -> List[int]:
    """
    生成指定大小和最大值的随机整数数组
    """
    return [random.randint(0, max_value) for _ in range(size)]

def test_algorithms():
    """
    测试不同算法的正确性
    """
    print("测试算法正确性...")
    
    test_cases = [
        [1, 3, 2, 4],
        [5, 1, 3, 2],
        [1, 2, 3, 4, 5],
        [10, 5, 8, 3, 7]
    ]
    
    for i, test_case in enumerate(test_cases):
        result_simple = calculate_positive_differences_sum_simple_optimized(test_case)
        result_efficient = calculate_with_coordinate_compression(test_case)
        
        print(f"测试用例 {i+1}: {test_case}")
        print(f"简单算法结果: {result_simple}")
        print(f"高效算法结果: {result_efficient}")
        print(f"结果一致: {result_simple == result_efficient}")
        print()

def main():
    """
    处理400000长度的数组
    """
    print("=" * 60)
    print("高效算法处理400000长度数组")
    print("=" * 60)
    
    # 首先测试算法正确性
    test_algorithms()
    
    # 生成400000长度的数组
    array_size = 400000
    max_element_value = 100000000
    
    print(f"\n生成长度为{array_size}，最大值为{max_element_value}的随机数组...")
    arr = generate_random_array(array_size, max_element_value)
    
    print("\n使用高效算法计算...")
    start_time = time.time()
    
    result = calculate_with_coordinate_compression(arr)
    
    end_time = time.time()
    
    print(f"\n计算完成！")
    print(f"数组长度: {array_size}")
    print(f"元素最大值: {max_element_value}")
    print(f"所有正差值的累加和: {result}")
    print(f"计算耗时: {end_time - start_time:.4f}秒")
    
    # 验证结果的合理性
    print(f"\n结果验证:")
    print(f"平均每个元素: {max_element_value // 2}")
    print(f"预期数量级: 约 {array_size * array_size // 4} * {max_element_value // 4}")
    
    return result

if __name__ == "__main__":
    main()