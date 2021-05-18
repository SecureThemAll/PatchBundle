#!/usr/bin/env python3

from .code_parser import Patch
from typing import List


class PatchRecord:
    def __init__(self,
                 project: str,
                 commit: str,
                 year: str,
                 number: str,
                 patches: List[Patch],
                 **kwargs):
        self.project = project
        self.commit = commit
        self.year = year
        self.number = number
        self.patches = patches

        if kwargs:
            print(f"Discarded {kwargs}")

    def has_patch(self):
        return self.patches

    def to_dict(self):
        records = []
        for patch in self.patches:
            for diff in patch:
                for hunk in diff:
                    records.append({'project': self.project,
                                    'commit': self.commit,
                                    'cve_year': self.year,
                                    'cve_number': self.number,
                                    'name': diff.name,
                                    'lang': diff.lang,
                                    'hunk': '\n'.join(hunk.lines),
                                    'additions': hunk.additions,
                                    'deletions': hunk.deletions,
                                    'hunk_name': hunk.name,
                                    'changes': hunk.changes
                                    })
        return records
