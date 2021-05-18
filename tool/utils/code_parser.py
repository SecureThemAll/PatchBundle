#!/usr/bin/env python3

import re
from pathlib import Path

from .functions import is_comment


class Hunk:
    def __init__(self, name: str, additions: int = 0, deletions: int = 0):
        self.name = name
        self.lines = []
        self.additions = additions
        self.deletions = deletions
        self.changes = 0
        self.prev = ''

    def __call__(self, line: str):
        # deletions
        if line.startswith('-'):
            self.deletions += 1
            if not self.prev == '-':
                self.changes += 1
        # additions
        elif line.startswith('+'):
            self.additions += 1
            if not self.prev == '+':
                self.changes += 1

        self.prev = line[0]
        self.lines.append(line)


class DiffParser:
    def __init__(self, name: str, lang: str):
        self.name = name
        self.lang = lang
        self.current = Hunk(self.name)
        self.hunks = [self.current]

    def __call__(self, line):
        # hunk header
        if line.startswith('@@'):
            # self.hunks += 1
            match = re.match(r"^@@.*@@\s*(.*)$", line)
            name = match.group(1) if match else line

            if name in self.hunks:
                name += "+"

            self.current = Hunk(name)
            self.hunks.append(self.current)
            return True

        if not (line.strip() == '' or
                line.startswith("index") or
                is_comment(line) or
                line.startswith('+++') or
                line.startswith('---')):
            self.current(line)

    def __iter__(self):
        # since list is already iterable
        return (hunk for hunk in self.hunks if hunk.lines)


class Patch:
    def __init__(self, name: str = '', lang: str = ''):
        self.jump = 0
        self.name = name
        self.lang = lang
        self.current = DiffParser(name=name, lang=lang)
        self.diffs = [self.current]

    def __call__(self, line):
        if self.jump > 0:
            self.jump -= 1
        elif line.strip().startswith("Index") or line.strip().startswith("index"):
            file = Path(line.strip().split()[-1])
            if file.suffix == '' or not file.suffix:
                self.jump = 3
            else:
                self.current = DiffParser(name=file.stem, lang=file.suffix)
                self.jump = 4
        elif line.startswith("diff"):
            line_split = line.split()

            if len(line_split) < 4:
                return

            file_a = line_split[2][1:]
            file_b = line_split[3][1:]

            if file_a != file_b:
                return

            file = Path(file_b)
            self.current = DiffParser(name=file.stem, lang=file.suffix)
            self.diffs.append(self.current)
        elif self.current:
            self.current(line)

    def __iter__(self):
        # since list is already iterable
        return (diff for diff in self.diffs)
