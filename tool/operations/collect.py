#!/usr/bin/env python3

from input_parser import add_operation
from base import Base


class Collect(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        for ds in self.datasets:
            data_set = ds.cls(name=ds.name, paths=self.configs.data_paths)
            data_set.collect(ds.source)
            self.log(f"Collected data for {ds.name}\n.")


def collect_args(input_parser):
    pass


co_parser = add_operation("collect", Collect, 'Collects the data for a given set name.')
collect_args(co_parser)
