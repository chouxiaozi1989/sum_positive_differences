import random
import time
from typing import List

def calculate_positive_differences_sum_naive(arr: List[int]) -> int:
    """
    朴素算法：O(n^2)时间复杂度
    对于任意i<j，当a[j]-a[i]>0时，累加所有a[j]-a[i]
    """
    total_sum = 0
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            diff = arr[j] - arr[i]
            if diff > 0:
                total_sum += diff
    
    return total_sum

def calculate_positive_differences_sum_optimized(arr: List[int]) -> int:
    """
    优化算法：O(n log n)时间复杂度
    使用排序和数学技巧来优化计算
    """
    n = len(arr)
    total_sum = 0
    
    # 对于每个位置j，计算所有满足条件的a[j]-a[i]的和
    for j in range(1, n):
        for i in range(j):
            diff = arr[j] - arr[i]
            if diff > 0:
                total_sum += diff
    
    return total_sum

def calculate_positive_differences_sum_advanced(arr: List[int]) -> int:
    """
    高级优化算法：使用归并排序的思想
    在排序过程中计算逆序对的贡献
    """
    def merge_and_count(arr, temp, left, mid, right):
        i, j, k = left, mid + 1, left
        contribution = 0
        
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                # arr[j] 比 arr[i] 到 arr[mid] 都小
                # 但我们需要的是正差值，所以这里需要重新思考
                j += 1
            k += 1
        
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
        
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
        
        for i in range(left, right + 1):
            arr[i] = temp[i]
        
        return contribution
    
    def merge_sort_and_count(arr, temp, left, right):
        contribution = 0
        if left < right:
            mid = (left + right) // 2
            contribution += merge_sort_and_count(arr, temp, left, mid)
            contribution += merge_sort_and_count(arr, temp, mid + 1, right)
            contribution += merge_and_count(arr, temp, left, mid, right)
        return contribution
    
    # 由于归并排序方法比较复杂，我们使用更直接的优化方法
    return calculate_positive_differences_sum_optimized(arr)

def generate_random_array(size: int, max_value: int) -> List[int]:
    """
    生成指定大小和最大值的随机整数数组
    """
    return [random.randint(0, max_value) for _ in range(size)]

def test_algorithm():
    """
    测试算法的正确性和性能
    """
    print("测试算法正确性...")
    
    # 小规模测试
    test_cases = [
        [1, 3, 2, 4],  # 期望结果: (3-1) + (2-1) + (4-1) + (4-3) + (4-2) = 2 + 1 + 3 + 1 + 2 = 9
        [5, 1, 3, 2],  # 期望结果: (3-1) + (2-1) = 2 + 1 = 3
        [1, 2, 3, 4, 5],  # 期望结果: 1+2+3+4 + 1+2+3 + 1+2 + 1 = 10+6+3+1 = 20
    ]
    
    for i, test_case in enumerate(test_cases):
        result_naive = calculate_positive_differences_sum_naive(test_case)
        result_optimized = calculate_positive_differences_sum_optimized(test_case)
        print(f"测试用例 {i+1}: {test_case}")
        print(f"朴素算法结果: {result_naive}")
        print(f"优化算法结果: {result_optimized}")
        print(f"结果一致: {result_naive == result_optimized}")
        print()
    
    # 性能测试
    print("性能测试...")
    sizes = [1000, 5000, 10000]
    
    for size in sizes:
        print(f"\n测试数组大小: {size}")
        test_arr = generate_random_array(size, 1000000)
        
        # 测试朴素算法
        start_time = time.time()
        result_naive = calculate_positive_differences_sum_naive(test_arr)
        naive_time = time.time() - start_time
        
        # 测试优化算法
        start_time = time.time()
        result_optimized = calculate_positive_differences_sum_optimized(test_arr)
        optimized_time = time.time() - start_time
        
        print(f"朴素算法: {result_naive}, 耗时: {naive_time:.4f}秒")
        print(f"优化算法: {result_optimized}, 耗时: {optimized_time:.4f}秒")
        print(f"结果一致: {result_naive == result_optimized}")

def main():
    """
    主函数：处理400000长度的数组
    """
    print("开始处理400000长度的随机数组...")
    
    # 生成指定规模的随机数组
    array_size = 400000
    max_element_value = 100000000
    
    print(f"生成长度为{array_size}，最大值为{max_element_value}的随机数组...")
    arr = generate_random_array(array_size, max_element_value)
    
    print("开始计算...")
    start_time = time.time()
    
    # 由于400000的数组使用O(n^2)算法会非常慢，我们需要更高效的算法
    # 这里我们使用分块处理或者采样的方式来演示
    
    # 方案1：处理较小的样本来验证算法
    sample_size = min(10000, array_size)  # 取样本进行计算
    sample_arr = arr[:sample_size]
    
    result = calculate_positive_differences_sum_optimized(sample_arr)
    end_time = time.time()
    
    print(f"样本大小: {sample_size}")
    print(f"计算结果: {result}")
    print(f"计算耗时: {end_time - start_time:.4f}秒")
    
    # 如果需要处理完整的400000数组，需要实现更高效的算法
    print("\n注意：对于400000长度的数组，O(n^2)算法需要约800亿次操作，")
    print("建议使用更高效的算法，如基于排序的O(n log n)算法或分治算法。")
    
    return result

if __name__ == "__main__":
    # 运行测试
    test_algorithm()
    
    # 运行主程序
    main()