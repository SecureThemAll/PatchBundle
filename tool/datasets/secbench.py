#!/usr/bin/env python3
from collections import Callable
from functools import wraps
from urllib import request

import pandas as pd
from pathlib import Path
from github import Github
from os.path import dirname

from utils.dataset import Dataset
from utils.functions import check_extension, parse_cve_id, comment_remover
from utils.decorators.transform import parse_patch_file


ROOT_DIR = dirname(dirname(__file__))

# readk token from file

with open(f'{ROOT_DIR}/token.txt', 'r') as t:
    token = t.read().splitlines()[0]

git = Github(token)


class Patch:
    def __init__(self, row: pd.Series, out_dir: Path):
        self.owner = row["owner"]
        self.project = row["project"]
        self.sha = row["sha"]
        self.sha_p = row["sha-p"]
        self.year = row["Year"]
        self.lang = row["Language"]
        self.cve_year, self.cve_number = parse_cve_id(row["Code"]) if isinstance(row["Code"], str) else ("", "")
        self.cwe = row["CWE"]
        self.repo = f"{self.owner}/{self.project}"
        self.out_dir = out_dir

    def __call__(self) -> str:
        # print(f"Getting repo {self.repo};")
        repo = git.get_repo(self.repo)
        patch_commit = repo.get_commit(sha=self.sha)
        print(f"Getting commit {self.sha} files for repo {self.repo}")
        # print(f"Processing commit {self.sha};")
        patch_dir = self.out_dir / Path(f"{self.owner}_{self.project}_{self.year}_{self.cwe}")
        print(f"Preparing folder {patch_dir}")
        patch_dir.mkdir(parents=True, exist_ok=True)
        for file in patch_commit.files:
            patch_file = patch_dir / Path(file.filename).name

            if not check_extension(patch_file.suffix):
                continue

            if file.patch is None:
                continue

            print(f"Writing file {file.filename}.")

            with patch_file.open(mode="w") as p:
                p.write(file.patch)

        return str(patch_dir)


def parse_number(func: Callable):
    @wraps(func)
    def wrapper_parse_year_number(*args, **kwargs):
        patch_record_args = func(*args, **kwargs)
        number = ""

        if 'Code' in kwargs and pd.notnull(kwargs["Code"]):
            _, number = parse_cve_id(kwargs['Code'])

        patch_record_args.update({'number': number})

        return patch_record_args

    return wrapper_parse_year_number


@parse_patch_file
@parse_number
def transform_columns(**record):
    return {'project': record['project'], 'commit': record['sha'], 'year': record['Year']}


class SecBench(Dataset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def collect(self, source: str):
        self.collected_path.mkdir(parents=True, exist_ok=True)
        out_file = source.split("/")[-1]
        out_file_path = self.collected_path / Path(out_file)
        print(f"Downloading from source {source}")
        request.urlretrieve(source, str(out_file_path))
        commit_dataset = pd.read_csv(str(out_file_path))
        print(f"Filtering by language.")
        filtered_ext = commit_dataset[commit_dataset.apply(lambda x: check_extension(x.Language), axis=1)].copy(
            deep=True)
        filtered_ext["dir"] = len(filtered_ext) * [""]

        for i, row in filtered_ext.iterrows():
            patch = Patch(row, self.collected_path)
            filtered_ext.loc[i, 'dir'] = patch()

        filtered_ext.to_csv(str(out_file_path))

    def transform(self):
        SECBENCH = self.collected_path / Path("secbench.csv")
        commit_dataset = pd.read_csv(SECBENCH)
        records = commit_dataset.to_dict(orient='records')

        for record in records:
            patch_dir = Path(record['dir'])

            for f in patch_dir.iterdir():
                if f.is_dir():
                    continue
                record['patch_file'] = f
                record['lang'] = f.suffix
                record['name'] = f.stem
                patch_record_args = transform_columns(**record)
                self.__call__(patch_record_args)

        self.data_to_pickle()
