def quick_sort(arr):
    """快速排序算法实现"""
    if len(arr) <= 1:
        return arr
    # 选择中间元素作为基准值
    pivot = arr[len(arr) // 2]
    # 将数组分成小于、等于和大于基准值的三部分
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    # 递归排序并合并
    return quick_sort(left) + middle + quick_sort(right)


if __name__ == "__main__":
    # 示例用法
    example_array = [3, 6, 8, 10, 1, 2, 1]
    print("排序前:", example_array)
    sorted_array = quick_sort(example_array)
    print("排序后:", sorted_array)