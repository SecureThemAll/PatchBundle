#!/usr/bin/env python3

import argparse
from base import Base

parser = argparse.ArgumentParser(prog="PatchBundle",
                                 description='Framework for dataset collection, creation, parsing and analysis for patches in C code.')

patch_parser = argparse.ArgumentParser(add_help=False)
patch_parser.add_argument('-ds', '--datasets', type=str, nargs='+', help='Name of the datasets.', required=True)
patch_parser.add_argument('-v', '--verbose', help='Verbose output.', action='store_true')
patch_parser.add_argument('-l', '--log_file', type=str, default=None, help='Log file to write the results to.')

subparsers = parser.add_subparsers()


def add_operation(name: str, operation: Base, description: str):
    operation_parser = subparsers.add_parser(name=name, help=description, parents=[patch_parser])
    operation_parser.set_defaults(operation=operation)
    operation_parser.set_defaults(name=name)

    return operation_parser


def run(operation: Base, **kwargs):
    opr = operation(**kwargs)
    opr()


import operations.collect
import operations.filter
import operations.transform
