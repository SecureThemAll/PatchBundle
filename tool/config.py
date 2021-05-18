#!/usr/bin/env python3

from dataclasses import dataclass
from os.path import dirname, abspath
from pathlib import Path
from typing import List, AnyStr, Dict, Tuple

from utils.data_structs import DataPaths, Dataset
import datasets


ROOT_DIR = dirname(dirname(__file__))
TOOL_DIR = dirname(abspath(__file__))


@dataclass
class Config:
    data_paths: DataPaths
    data_sets: Dict[Dataset, Tuple]

    def get_data_sets(self, datasets: List[AnyStr] = None):
        if not datasets:
            return [self.data_sets[ds] for ds in datasets]
        return [self.data_sets[ds] for ds in datasets if ds in self.data_sets]


# (name, source, class)
data_sets = {"nvd": ("https://github.com/VulDeePecker/Comparative_Study/raw/master/Source%20programs/NVD.zip", datasets.NVD),
             "secbench": ("https://github.com/TQRG/secbench/raw/master/dataset/secbench.csv", datasets.SecBench),
             "mozilla": ("mozilla/mozilla.csv", datasets.Mozilla),
             "secretpatch": ("https://github.com/SecretPatch/Dataset/raw/master/SecurityDataset.zip", datasets.SecretPatch),
             "msr20vuln": ("https://github.com/ZeoVan/MSR_20_Code_vulnerability_CSV_Dataset/raw/master/" +
                           "all_c_cpp_release2.0.csv", datasets.MSR20Vuln)
             }

data_root_path = Path(ROOT_DIR, "data")
data_paths = DataPaths(root=data_root_path,
                       collected=Path(data_root_path, "collected"),
                       transformed=Path(data_root_path, "transformed"),
                       filtered=Path(data_root_path, "filtered"))


configurations = Config(data_paths=data_paths,
                        data_sets={name: Dataset(name=name, source=src, cls=cls) for name, (src, cls) in data_sets.items()})
