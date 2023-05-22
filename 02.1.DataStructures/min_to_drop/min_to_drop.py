import typing as tp
from collections import Counter


def get_min_to_drop(seq: tp.Sequence[tp.Any]) -> int:
    """
    :param seq: sequence of elements
    :return: number of elements need to drop to leave equal elements
    """
    counter = Counter(seq)
    if len(seq) > 0:
        return len(seq) - counter[counter.most_common(1)[0][0]]
    else:
        return 0
