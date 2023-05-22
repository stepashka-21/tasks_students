import typing as tp


def filter_list_by_list(lst_a: tp.Union[list[int], range], lst_b: tp.Union[list[int], range]) -> list[int]:

    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    i, j = 0, 0
    str = []
    while i < len(lst_a) and j < len(lst_b):
        if lst_a[i] == lst_b[j]:
            i += 1
            j += 1
        elif lst_a[i] < lst_b[j]:
            str.append(lst_a[i])
            i += 1
        else:
            j += 1
    while i < len(lst_a):
        str.append(lst_a[i])
        i += 1
    return str