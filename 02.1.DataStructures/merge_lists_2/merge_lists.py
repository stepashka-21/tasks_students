import typing as tp
import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    heap: tp.List[tp.Any] = []
    for i, lst in enumerate(seq):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    res = []
    while heap:
        val, list_index, elem_index = heapq.heappop(heap)
        res.append(val)
        elem_index += 1
        if elem_index < len(seq[list_index]):
            heapq.heappush(heap, (seq[list_index][elem_index], list_index, elem_index))
    return res
