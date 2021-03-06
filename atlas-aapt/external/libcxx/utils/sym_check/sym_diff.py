#!/usr/bin/env python
"""
sym_diff - Compare two symbol lists and output the differences.
"""
from argparse import ArgumentParser
import sys
from sym_check import diff, util


def main():
    parser = ArgumentParser(
        description='Extract a list of symbols from a shared library.')
    parser.add_argument(
        '--names-only', dest='names_only',
        help='Only print symbol names',
        action='store_true', default=False)
    parser.add_argument(
        '-o', '--output', dest='output',
        help='The output file. stdout is used if not given',
        type=str, action='store', default=None)
    parser.add_argument(
        '--demangle', dest='demangle', action='store_true', default=False)
    parser.add_argument(
        'old_syms', metavar='old-syms', type=str,
        help='The file containing the old symbol list or a library')
    parser.add_argument(
        'new_syms', metavar='new-syms', type=str,
        help='The file containing the new symbol list or a library')
    args = parser.parse_args()

    old_syms_list = util.extract_or_load(args.old_syms)
    new_syms_list = util.extract_or_load(args.new_syms)

    added, removed, changed = diff.diff(old_syms_list, new_syms_list)
    report, is_break = diff.report_diff(added, removed, changed,
                                        names_only=args.names_only,
                                        demangle=args.demangle)
    if args.output is None:
        print(report)
    else:
        with open(args.output, 'w') as f:
            f.write(report + '\n')
    sys.exit(is_break)


if __name__ == '__main__':
    main()
