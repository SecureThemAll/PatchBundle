import json
from pathlib import Path

import pandas as pd

from collections import Callable
from datetime import datetime
from functools import wraps

from utils.functions import parse_cve_id
from utils.decorators.code import split_lines, remove_comments
from utils.decorators.transform import create_patch


def year_from_date(p_date: str):
    try:
        datetime_object = datetime.strptime(p_date, '%y-%m-%d')
        return str(datetime_object.year)
    except ValueError or TypeError as e:
        print(e)
        return ""


def parse_year_number(func: Callable):
    @wraps(func)
    def wrapper_parse_year_number(*args, **kwargs):
        patch_record_args = func(*args, **kwargs)
        year, number = "", ""

        if 'cve_id' in kwargs and pd.notnull(kwargs["cve_id"]):
            year, number = parse_cve_id(kwargs['cve_id'])
        elif 'publish_date' in kwargs and pd.notnull(kwargs["publish_date"]):
            year = year_from_date(kwargs["publish_date"])

        patch_record_args.update({'year': year, 'number': number})

        return patch_record_args

    return wrapper_parse_year_number


@create_patch
@split_lines
@remove_comments
def change_to_patch(code: str, name: str, lang: str):
    return code


def changes_to_patches(func: Callable):
    @wraps(func)
    def wrapper_changes_to_patches(*args, **kwargs):
        patch_record_args = func(*args, **kwargs)
        patches = []

        try:
            files_changed = kwargs['files_changed']
            files_changed = files_changed.split("<_**next**_>")
            changes = [json.loads(file) for file in files_changed]

            for change in changes:
                if "patch" not in change:
                    continue
                filename = Path(change["filename"])
                patch = change_to_patch(code=change["patch"], name=filename.stem, lang=filename.suffix)

                if patch:
                    patches.append(patch)

        except AttributeError as ae:
            print(ae)

        patch_record_args.update({'patches': patches})

        return patch_record_args

    return wrapper_changes_to_patches
