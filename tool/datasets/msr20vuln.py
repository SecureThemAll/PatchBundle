#!/usr/bin/env python3

import urllib.request as request
import pandas as pd

from pathlib import Path

from utils.dataset import Dataset
# Decorators
from utils.decorators.msr20 import changes_to_patches, parse_year_number


@parse_year_number
@changes_to_patches
def transform_columns(**record):
    return {'project': record['project'], 'commit': record['commit_id']}


class MSR20Vuln(Dataset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def collect(self, source: str):
        self.collected_path.mkdir(parents=True, exist_ok=True)
        out_file_path = self.collected_path / Path("msr20.csv")
        print(f"Downloading from source {source}")
        request.urlretrieve(source, str(out_file_path))

    def transform(self):
        MSR20 = self.collected_path / Path("msr20.csv")
        commit_dataset = pd.read_csv(str(MSR20))
        records = commit_dataset.to_dict(orient='records')

        for record in records:
            patch_record_args = transform_columns(**record)
            self.__call__(patch_record_args)
        self.data_to_pickle()
