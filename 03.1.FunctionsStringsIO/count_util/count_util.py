import re
import typing as tp


def count_util(text: str, flags: tp.Optional[str] = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
"""

    if flags is None or flags == "":
        flags = "-mlLw"
    sorted(flags)

    results = {}

    if "m" in flags:
        results["chars"] = len(text)

    if "l" in flags:
        results["lines"] = len(text.split("\n")) - 1

    if "L" in flags:
        lines = text.split("\n")
        longest_line = max(lines, key=len)
        results["longest_line"] = len(longest_line)

    if "w" in flags:
        results["words"] = len(re.findall(r'\b\w+\b', text))

    return results
