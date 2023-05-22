from typing import Iterable, Generator, Any, List


def flat_it(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    stack: List[(Any, Any)] = [(sequence, iter(sequence))]
    while stack:
        sequence, sequence_iter = stack.pop()
        while True:
            try:
                item = next(sequence_iter)
            except StopIteration:
                break

            try:
                item_iter = iter(item)
            except TypeError:
                yield item
                continue

            if item != sequence:
                stack.append((sequence, sequence_iter))
                stack.append((item, item_iter))
            else:
                yield item
            break
