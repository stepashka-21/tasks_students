import sys
import math
from typing import Any, Optional

PROMPT = '>>> '


def run_calc(context: Optional[dict[str, Any]] = None) -> None:
    """Run interactive calculator session in specified namespace"""
    while True:
        sys.stdout.write(PROMPT)
        input = sys.stdin.readline()
        if not input.strip():
            sys.stdout.write('\n')
            break
        try:
            eval(input, {'__builtins__': {}}, context)
        except NameError as e:
            sys.stderr.write(f"{e}")
            raise e
        sys.stdout.write(str(eval(input, {'__builtins__': {}}, context)) + '\n')


if __name__ == '__main__':
    context = {'math': math}
    run_calc(context)
