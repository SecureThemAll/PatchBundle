#!/usr/bin/env python3

import re
from pathlib import Path
from typing import List

import pandas as pd

from .patterns import *

cpp_extensions = ['cc', "cpp", 'C', 'cxx', 'c++', 'hh', 'H', 'hxx', "h++", "hpp"]
c_extensions = ['c', 'h']
frame_columns = ['project', 'patch', 'cve_year', 'cve_number', 'name', 'lang', 'hunk', 'additions', 'deletions',
                 'hunk_name']


def parse_cve_id(cve_id: str):
    match = re.search(cve_pattern, cve_id)

    if match is None:
        return "", ""

    return match.group(1), match.group(2)


def check_extension(ext):
    ext = ''.join(ext.split("."))
    return ext in (cpp_extensions + c_extensions)


def is_comment(string: str):
    if string.startswith('+') or string.startswith('-'):
        string = string[1:].strip()
    else:
        string = string.strip()
    return (re.match(comment_pattern, string) or
            re.match(comment_pattern, string))


def is_func_def(string: str):
    if string.startswith('+') or string.startswith('-'):
        string = string[1:].strip()
    return re.match(function_pattern, string)


def get_func_name(string: str):
    result = re.search(func_name_pattern, string)
    if result is not None:
        return result.group(1)
    return result


def comment_remover(code: str):
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
    return re.sub(pattern, replacer, code)


def to_frame(data: List, name: str, out_path: Path):
    frame = pd.DataFrame(data, columns=frame_columns)
    print(f"Hunks count: {len(frame)}")
    frame.drop_duplicates(subset="hunk", keep=False, inplace=True)
    print(f"Unique hunks count: {len(frame)}")
    frame.to_pickle(f"{out_path}/{name}.pkl")


def get_name_lang(diff_file):
    match = re.search(ext_pattern, diff_file)

    if match:
        return match.group(1), match.group(2)

    print("No match for: ", diff_file)

    return "", ""

