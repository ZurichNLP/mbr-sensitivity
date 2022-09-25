import argparse
import re
from collections import Counter, defaultdict


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--src_file', type=argparse.FileType('r'),
                    required=True, help='file with source sentences')
    ap.add_argument('-f', '--hyp_files', type=argparse.FileType('r'),
                    nargs='+', required=True, help='files with MBR outputs')
    return ap.parse_args()


def main(args):

    results = defaultdict(lambda: {'total_src': 0, 'total_hyp': 0,
                                   'src_in_hyp': 0, 'hyp_in_src': 0})

    punct_match = re.compile(r'[\.\,\']')
    number_match = re.compile(r'\d+\ ?\d*')
    space_match = re.compile(r'\ ')

    for srcline in args.src_file:
        srcnums = [space_match.sub('', num) for num in number_match.findall(punct_match.sub(' ', srcline)) if num != '2']

        for mbr_file in args.hyp_files:
            hypnums = [space_match.sub('', num) for num in number_match.findall(punct_match.sub(' ', mbr_file.readline())) if num != '2']

            results[mbr_file]['total_src'] += len(srcnums)
            results[mbr_file]['total_hyp'] += len(hypnums)

            srcnumsc = Counter(srcnums)

            for num in hypnums:
                if srcnumsc[num] > 0:
                    results[mbr_file]['hyp_in_src'] += 1
                    srcnumsc[num] -= 1

            hypnums = Counter(hypnums)

            for num in srcnums:
                if hypnums[num] > 0:
                    results[mbr_file]['src_in_hyp'] += 1
                    hypnums[num] -= 1

    for mbr_file in args.hyp_files:
        recall = results[mbr_file]['src_in_hyp'] / results[mbr_file]['total_src']
        precision = results[mbr_file]['hyp_in_src'] / results[mbr_file]['total_hyp']
        f1 = (2 * precision * recall)/(precision + recall)*100
        print(f"{mbr_file.name}\t{f1}")


if __name__ == '__main__':
    args = parse_args()
    main(args)
