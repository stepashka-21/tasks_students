from typing import List


def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    tokens = path.split("/")
    stack: List[str] = []

    for token in tokens:
        if token:
            if token != '.':
                if token == '..':
                    if stack:
                        if stack[-1] == token:
                            if not (len(tokens) > 0 and tokens[0] == ""):
                                stack.append(token)
                        else:
                            stack.pop()
                    else:
                        if path[0] == '/':
                            continue
                        if not (len(tokens) > 0 and tokens[0] == ""):
                            stack.append(token)
                else:
                    stack.append(token)
    if stack == tokens:
        if len(tokens) > 1 and tokens[-1] != '..' and (token == '..' for token in tokens):
            stack = tokens[:-2]
    if path == '':
        return '.'
    elif path[0] == '/':
        return '/' + '/'.join(stack)
    else:
        return '/'.join(stack) or '.'


