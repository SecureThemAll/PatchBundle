#!/usr/bin/env python3

import re

from functools import wraps
from typing import Callable


def replacer(match):
    s = match.group(0)
    if s.startswith('/'):
        return " "  # note: a space and not an empty string
    else:
        return s


pattern = re.compile(
    r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
    re.DOTALL | re.MULTILINE
)


def remove_comments(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        code = func(*args, **kwargs)

        if code:
            return re.sub(pattern, replacer, code)
        return code
    return wrapper


def split_lines(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        content = func(*args, **kwargs)
        if content:
            return content.split('\n')
        return content
    return wrapper


def clean_code_file(func: Callable):
    @split_lines
    @remove_comments
    @wraps(func)
    def wrapper(*args, **kwargs):
        path = func(*args, **kwargs)
        if path:
            with path.open(mode="r", encoding='utf-8', errors='replace') as f:
                return f.read()
        return path
    return wrapper
