import types
import dis
from collections import Counter


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """

    result = Counter()
    for instruction in dis.get_instructions(source_code):
        result.update([instruction.opname])
        if isinstance(instruction.argval, types.CodeType):
            result.update(count_operations(instruction.argval))
    return dict(result)
