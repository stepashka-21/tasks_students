import typing as tp


def find_value(nums: tp.Union[list[int], range], value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    start, finish = 0, len(nums) - 1
    k = False
    while start <= finish:
        i = (start + finish) // 2
        if nums[i] > value:
            finish = i - 1
        elif nums[i] < value:
            start = i + 1
        else:
            k = True
            break
    return k
