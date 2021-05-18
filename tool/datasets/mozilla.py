#!/usr/bin/env python3
import re
from pathlib import Path

import pandas as pd
from requests import get

from utils.dataset import Dataset
from utils.decorators.transform import parse_patch_file
from utils.decorators.mozilla import parse_commit, parse_year_number


# DATASET_COLUMNS (P_ID, P_URL, R_ID, P_COMMIT, ERROR_SIMILARITY, SITUATION, RELEASES, DATE,
#                  V_ID,CVE, ID_ADVISORIES, V_CLASSIFICATION, V_IMPACT, VULNERABILITY_URL, PRODUCTS)


def download_patch(url: str, out_path_file: Path):
    url = re.sub('&action=diff', '', url)
    print(f"Downloading from {url}")

    try:
        data = get(url)
        raw_diff = data.content.decode("utf-8")

        with out_path_file.open(mode="w") as out:
            out.write(raw_diff)

    except Exception as e:
        # TODO: fix this, for some reason some files contain strange characters that cannot be written
        with open("exceptions.log", "a") as ex:
            ex.write(f"{out_path_file}:\n{e}\n")


@parse_patch_file
@parse_year_number
@parse_commit
def transform_columns(**record):
    return {'project': record['PRODUCTS']}


class Mozilla(Dataset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def collect(self, source: str):
        dataset = pd.read_csv(self.paths.collected / Path(source))
        dataset["patch_file"] = len(dataset)*[""]

        for i, row in dataset.iterrows():
            print(f"Collecting patch {row['P_ID']} for vuln {row['V_ID']}")
            out_file = self.collected_path / Path(f"{row['P_ID']}_{row['V_ID']}.txt")
            download_patch(url=row['P_URL'], out_path_file=out_file)
            dataset.loc[i, 'patch_file'] = str(out_file)

        dataset.to_csv(str(self.paths.collected / Path(source)))

    def transform(self):
        MOZILLA = self.collected_path / Path("mozilla.csv")
        dataset = pd.read_csv(MOZILLA)
        no_nulls = dataset[dataset['patch_file'].notnull()].reset_index()
        no_nulls.where(pd.notnull(no_nulls), None)
        records = no_nulls.to_dict(orient='records')

        for record in records:
            record['name'] = ''
            record['lang'] = ''
            patch_record_args = transform_columns(**record)
            self.__call__(patch_record_args)

        self.data_to_pickle()
