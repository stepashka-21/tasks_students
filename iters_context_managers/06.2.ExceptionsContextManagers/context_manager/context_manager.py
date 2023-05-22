import sys
import traceback
from contextlib import contextmanager
from typing import Iterator, Optional, TextIO, Type


@contextmanager
def supresser(*types_: Type[BaseException]) -> Iterator[None]:
    try:
        yield
    except types_:
        pass


@contextmanager
def retyper(type_from: Type[BaseException], type_to: Type[BaseException]) -> Iterator[None]:
    try:
        yield
    except type_from:
        val, trace = sys.exc_info()[1], sys.exc_info()[2]
        if isinstance(val, type_from):
            raise type_to(*val.args).with_traceback(trace)
        raise


@contextmanager
def dumper(stream: Optional[TextIO] = None) -> Iterator[None]:
    if stream is None:
        stream = sys.stderr
    try:
        yield
    except Exception:
        tp, val = sys.exc_info()[0], sys.exc_info()[1]
        stream.write(''.join(traceback.format_exception_only(tp, val)))
        raise
