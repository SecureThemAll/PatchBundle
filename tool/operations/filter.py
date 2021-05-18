#!/usr/bin/env python3
from pathlib import Path

from input_parser import add_operation
from base import Base
import pandas as pd


class Filter(Base):
    def __init__(self, merge: bool, **kwargs):
        super().__init__(**kwargs)
        self.merge = merge

    def __call__(self, *args, **kwargs):
        frames = []
        for ds in self.datasets:
            data_set = ds.cls(name=ds.name, paths=self.configs.data_paths)
            frames.append(data_set.filter())
            self.log(f"Filtered data for {ds.name}\n.")

        if self.merge and len(frames) > 1:
            result = pd.concat(frames, ignore_index=True, sort=False)
            result.drop_duplicates(subset="hunk", keep=False, inplace=True)
            print(len(result))
            result.to_pickle(self.configs.data_paths.filtered / Path('merged.pkl'), protocol=4)


def filter_args(input_parser):
    input_parser.add_argument('-m', '--merge', action='store_true', help='Merges the filtered datasets into one.', default=False)


filter_parser = add_operation("filter", Filter, 'Filters the transformed datasets.')
filter_args(filter_parser)
