import time
import random
import sys

# 파이썬 기본 재귀 한도를 늘려 퀵 정렬 최악의 경우 대비
sys.setrecursionlimit(20000)

# ==========================================
# 1. 배운 정렬 1: 퀵 정렬 (Quick Sort)
# ==========================================
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + equal + quick_sort(right)

# ==========================================
# 2. 배운 정렬 2: 병합 정렬 (Merge Sort)
# ==========================================
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# ==========================================
# 3. 배우지 않은 정렬: 팀 정렬 (Tim Sort)
# ==========================================
MIN_RUN = 32

def insertion_sort_for_tim(arr, left, right):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and arr[j] > temp:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp

def merge_for_tim(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left_arr = arr[l : l + len1]
    right_arr = arr[m + 1 : m + 1 + len2]

    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left_arr[i]
        k += 1
        i += 1
    while j < len2:
        arr[k] = right_arr[j]
        k += 1
        j += 1

def tim_sort(arr):
    n = len(arr)
    # 최소 크기 단위(Run)로 나누어 삽입 정렬 수행
    for i in range(0, n, MIN_RUN):
        insertion_sort_for_tim(arr, i, min((i + MIN_RUN - 1), (n - 1)))

    size = MIN_RUN
    # 정렬된 Run들을 병합
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min((left + size - 1), (n - 1))
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge_for_tim(arr, left, mid, right)
        size *= 2
    return arr

# ==========================================
# 성능 비교 테스트 진행 함수
# ==========================================
def measure_time(sort_func, data):
    start = time.time()
    sort_func(data)
    end = time.time()
    return end - start

if __name__ == "__main__":
    N = 10000
    print(f"[{N}개 데이터 정렬 성능 비교]")

    datasets = {
        "무작위 배열(Random)": [random.randint(1, 100000) for _ in range(N)],
        "정렬된 배열(Sorted)": list(range(1, N + 1)),
        "역순 배열(Reversed)": list(range(N, 0, -1))
    }

    for name, original_data in datasets.items():
        print(f"\n--- {name} ---")

        # 각 정렬이 원본 배열을 변형하지 않도록 별도의 복사본 사용
        data_for_quick = original_data.copy()
        data_for_merge = original_data.copy()
        data_for_tim = original_data.copy()

        # 1. 퀵 정렬 측정
        try:
            time_quick = measure_time(quick_sort, data_for_quick)
            print(f"퀵 정렬 (Quick Sort)  : {time_quick:.5f} 초")
        except RecursionError:
            print(f"퀵 정렬 (Quick Sort)  : 에러 발생 (재귀 한도 초과 - 최악의 경우)")

        # 2. 병합 정렬 측정
        time_merge = measure_time(merge_sort, data_for_merge)
        print(f"병합 정렬 (Merge Sort)  : {time_merge:.5f} 초")

        # 3. 팀 정렬 측정 (In-place로 구현되었으므로 원본이 정렬됨)
        time_tim = measure_time(tim_sort, data_for_tim)
        print(f"팀 정렬 (Tim Sort)    : {time_tim:.5f} 초")
