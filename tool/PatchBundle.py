#!/usr/bin/env python3


from config import configurations
from input_parser import parser, run


if __name__ == "__main__":
    args = parser.parse_args()
    vars_args = dict(vars(args))
    vars_args.update({"configs": configurations})
    run(**vars_args)
