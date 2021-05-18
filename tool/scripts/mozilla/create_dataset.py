#!/usr/bin/env python3

from pathlib import Path

import pandas as pd
import argparse

#from utils.functions import parse_cve_id
#from .parse import parse_classification, parse_date

# VULNERABILITIES (V_ID,CVE,ID_ADVISORIES,V_CLASSIFICATION,V_IMPACT,VULNERABILITY_URL,PRODUCTS)
# PATCHES (P_ID,P_URL,V_ID,R_ID,P_COMMIT,ERROR_SIMILARITY,SITUATION,RELEASES,DATE)
# DATASET_COLUMNS (P_ID, P_URL, R_ID, P_COMMIT, ERROR_SIMILARITY, SITUATION, RELEASES, DATE,
#                  V_ID,CVE, ID_ADVISORIES, V_CLASSIFICATION, V_IMPACT, VULNERABILITY_URL, PRODUCTS)


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-op', '--out_path', type=str, help='Absolute path to write the dataset.', required=True)


def match_patch_vuln(out_path: str):
    vulns = pd.read_csv("assets/vulns.csv", sep=",")
    patches = pd.read_csv("assets/patches.csv", sep=",")
    # patches = patches.drop(columns=["R_ID", "SITUATION", "ERROR_SIMILARITY", "DATE"])
    # matched = patches.astype(str).join(other=vulns.astype(str), on="V_ID", how="inner")
    matched = pd.merge(left=patches, right=vulns, on="V_ID", how="inner")
    matched.to_csv(path_or_buf=Path(out_path, "mozilla.csv"))


if __name__ == '__main__':
    args = parser.parse_args()
    match_patch_vuln(out_path=args.out_path)
