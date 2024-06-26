import heapq
import typing as tp


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    heap: tp.List[tp.Any] = []
    for i in input_streams:
        for j in i:
            st = int(j.decode('UTF-8'))
            heapq.heappush(heap, st)
    while heap:
        output_stream.write((str(heapq.heappop(heap)) + '\n').encode())
