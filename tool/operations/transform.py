#!/usr/bin/env python3
from pathlib import Path

from input_parser import add_operation
from base import Base


class Transform(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        for ds in self.datasets:
            data_set = ds.cls(name=ds.name, paths=self.configs.data_paths)
            data_set.transform()
            self.log(f"Transformed data for {ds.name}\n.")


def transform_args(input_parser):
    pass


tr_parser = add_operation("transform", Transform, 'Parses the collected data into a generic format.')
transform_args(tr_parser)
