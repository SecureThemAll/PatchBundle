#!/usr/bin/env python3

import pandas as pd
import re

from collections import Callable
from datetime import datetime
from functools import wraps

from utils.patterns import advisories_pattern
from utils.functions import parse_cve_id


def parse_advisories(id_advs: str):
    match = re.match(advisories_pattern, id_advs)
    if match:
        return match.group(1), match.group(2)

    return "", ""


def parse_commit(func: Callable):
    @wraps(func)
    def wrapper_parse_commit(*args, **kwargs):
        patch_record_args = func(*args, **kwargs)
        commit = ""

        if 'P_COMMIT' in kwargs:
            commit = kwargs['P_COMMIT']

            if commit in ["files not c/c++", "log or number not found", "not found similar commit"]:
                commit = ""

        patch_record_args.update({
            'commit': commit
        })

        return patch_record_args
    return wrapper_parse_commit


def year_from_date(p_date: str):
    try:
        datetime_object = datetime.strptime(p_date, '%d-%m-%y %H:%M')
        return str(datetime_object.year)
    except ValueError or TypeError as e:
        print(e)
        return ""


def parse_year_number(func: Callable):
    @wraps(func)
    def wrapper_parse_year_number(*args, **kwargs):
        patch_record_args = func(*args, **kwargs)
        year, number = "", ""

        if 'CVE' in kwargs and pd.notnull(kwargs["CVE"]):
            year, number = parse_cve_id(kwargs['CVE'])
        elif 'DATE' in kwargs and pd.notnull(kwargs["DATE"]):
            year = year_from_date(kwargs["DATE"])
        else:
            year, number = parse_advisories(kwargs["ID_ADVISORIES"])

        patch_record_args.update({'year': year, 'number': number})

        return patch_record_args

    return wrapper_parse_year_number
