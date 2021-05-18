#!/usr/bin/env python3
from pathlib import Path
from typing import List, AnyStr
from config import Config


class Base:
    def __init__(self, configs: Config, name: str, datasets: List[AnyStr] = None, verbose: bool = False,
                 log_file: str = None, **kwargs):
        """
        :type log_file: str
        :type verbose: bool
        :type configs: Config
        :type sets: List[AnyStr]
        :type name: str
        :type out_path: str
        """
        self.configs = configs
        self.datasets = self.configs.get_data_sets(datasets)
        self.name = name
        self.verbose = verbose
        self.log_file = Path(log_file) if log_file else log_file

        if kwargs:
            self.log(f"Unknown arguments: {kwargs}\n")

    def log(self, msg: str):
        if msg and self.log_file:
            with self.log_file.open(mode="a") as lf:
                lf.write(msg)
