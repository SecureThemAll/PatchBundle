#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Dataset:
    name: str
    source: str
    cls: object


@dataclass
class DataPaths:
    root: Path
    collected: Path
    transformed: Path
    filtered: Path
