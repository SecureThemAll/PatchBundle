import difflib
import itertools
import urllib.request as request

from zipfile import ZipFile
from pathlib import Path

from utils.dataset import Dataset
from utils.functions import check_extension

# Decorators
from utils.decorators.code import remove_comments, split_lines
from utils.decorators.transform import create_patch


class CVEFile:
    def __init__(self, file: Path):
        self.file = file

        name_split = self.file.stem.split("CVE")
        self.project = name_split[0].replace('_', '')
        cve_split = name_split[1].replace('-', '_').split('_')

        self.year = cve_split[1]
        self.number = cve_split[2]
        self.status = cve_split[3] if cve_split[3] in ["VULN", "PATCHED"] else None
        self.name = ''.join(cve_split[4:]) if self.status else ''.join(cve_split[3:])
        self.lang = self.file.suffix

    def __eq__(self, other):
        if not isinstance(other, CVEFile):
            return NotImplemented

        return self.project == other.project and self.year == other.year and self.number == other.number \
               and self.name == other.name and self.lang == other.lang

    def __str__(self):
        return self.file.name


@split_lines
@remove_comments
def read_cve_file(file_path: Path, replace_target: str):
    with file_path.open(mode="r") as f:
        code = f.read()
        code = code.replace(replace_target, '')
        return code


@create_patch
def files_to_patch(vuln: CVEFile, patched: CVEFile, name: str, lang: str):
    vuln_lines = read_cve_file(vuln.file, 'VULN_')
    patched_lines = read_cve_file(patched.file, 'PATCHED_')

    # TODO: ADD number of context lines to diff
    return difflib.unified_diff(vuln_lines,
                                patched_lines, fromfile=vuln.file.name, tofile=patched.file.name)


class NVD(Dataset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapping = {}

    def collect(self, source: str):
        out_path = self.paths.collected / Path(self.name)
        out_file = source.split("/")[-1]
        out_file_path = out_path / Path(out_file)
        out_path.mkdir(parents=True, exist_ok=True)
        request.urlretrieve(source, str(out_file_path))

        with ZipFile(str(out_file_path), 'r') as zf:
            print("Extracting zip.")
            zf.extractall(path=out_path)

        out_file_path.unlink()

    def transform(self):
        self._map()

        for i, (folder, cve_files) in enumerate(self.mapping.items()):
            if len(cve_files) >= 2:
                for a, b in itertools.combinations(cve_files, 2):
                    if not a == b:
                        continue

                    pair = {a.status.lower(): a, b.status.lower(): b}

                    if len(pair) == 1:
                        continue

                    patch = files_to_patch(**pair, name=a.name, lang=a.lang)
                    patch_record_args = {'project': a.project, 'commit': '', 'year': a.year, 'number': a.number,
                                         'patches': [patch]}
                    self.__call__(patch_record_args)

        self.data_to_pickle()

    def _map(self):
        for folder in self.collected_path.iterdir():
            self.mapping[folder.name] = [CVEFile(file) for file in folder.iterdir() if check_extension(file.suffix)]

