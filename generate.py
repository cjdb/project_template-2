#!/usr/bin/env python3

import sys
from args import parse_args
from new_project import new_project


def main():
    args = parse_args()
    if args.command == 'new-project':
        new_project(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
