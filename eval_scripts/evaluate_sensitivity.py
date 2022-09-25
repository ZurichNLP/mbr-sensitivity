import argparse
import json
from collections import defaultdict

import numpy as np


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', type=str, required=True,
                    help='path to results json file')
    ap.add_argument('-o', '--order', type=str, nargs='+', required=False,
                    help='desired output order of error types')
    return ap.parse_args()


def main(args):

    with open(args.file, 'r') as infile:
        results = json.load(infile)

    scores = defaultdict(list)

    for _, result in results.items():
        error_types = result.keys()
        refscore = float(result['reference'][1])

        for error_type in error_types:
            if error_type == 'reference' or result[error_type][0] == '':
                continue

            scores[error_type].append(float(result[error_type][1]) - refscore)

    order = sorted(scores) if not args.order else args.order

    for type in order:
        print(f'{type}\t{str(np.mean(scores[type]))}')


if __name__ == '__main__':
    args = parse_args()
    main(args)
