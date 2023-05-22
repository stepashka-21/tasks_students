import typing as tp


def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    str = []
    for i in range(len(elements)):
        str.append(elements[i]**2)
    return str

# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    str = []
    for i in range(1, len(elements) + 1):
        str.append(i)
    return str


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """
    ind = -1
    x = 0
    for i in range(len(elements)):
        if elements[i] > x:
            ind = i
            x = elements[i]
    if ind == -1:
        return None
    else:
        return ind

# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    str = []
    for i in range(1, len(elements), 2):
        str.append(elements[i])
    return str


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    ind = -1
    for i in range(len(elements)):
        if elements[i] == 3:
            ind = i
            break
    if ind == -1:
        return None
    else:
        return ind


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    ind = -1
    for i in range(len(elements) - 1, -1, -1):
        if elements[i] == 3:
            ind = i
            break
    if ind == -1:
        return None
    else:
        return ind


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)


# ====================================================================================================


def get_min_max(elements: list[int], default: tp.Optional[int]) -> tuple[tp.Optional[int], tp.Optional[int]]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    if len(elements) == 0:
        return default, default
    else:
        mi, ma = elements[0], elements[0]
        for i in range(1, len(elements)):
            mi = min(mi, elements[i])
            ma = max(ma, elements[i])
        return mi, ma
# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    return None if len(elements) < i else x if (x := elements[i]) > boundary else None



