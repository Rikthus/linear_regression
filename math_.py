import numpy as np


def mean(arr: np.array) -> float:
    n = len(arr)
    arr_sum = 0
    for val in arr:
        arr_sum += val
    return arr_sum / n
