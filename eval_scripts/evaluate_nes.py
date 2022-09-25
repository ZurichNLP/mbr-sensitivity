import argparse
import re
from collections import Counter, defaultdict

import spacy


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--ref_file', type=argparse.FileType('r'),
                    required=True, help='file with reference sentences')
    ap.add_argument('-f', '--hyp_files', type=argparse.FileType('r'), nargs='+',
                    required=True, help='files with MBR outputs')
    ap.add_argument('-l', '--lang', type=str, required=True,
                    help='target language code')
    return ap.parse_args()


def main(args):

    if args.lang == 'de':
        nlp = spacy.load("de_core_news_lg")
        tag = 'PER'
    elif args.lang == 'en':
        nlp = spacy.load("en_core_web_lg")
        tag = 'PERSON'

    results = defaultdict(lambda: {'total_ref': 0, 'total_hyp': 0,
                                   'ref_in_hyp': 0, 'hyp_in_ref': 0})

    for refline in args.ref_file:
        refnes = [ent.text for ent in nlp(refline).ents if ent.label_ == tag]

        for mbr_file in args.hyp_files:
            hypnes = [ent.text for ent in nlp(mbr_file.readline()).ents if ent.label_ == tag]

            results[mbr_file]['total_ref'] += len(refnes)
            results[mbr_file]['total_hyp'] += len(hypnes)

            refnesc = Counter(refnes)

            for ent in hypnes:
                if refnesc[ent] > 0:
                    results[mbr_file]['hyp_in_ref'] += 1
                    refnesc[ent] -= 1

            hypnes = Counter(hypnes)

            for ent in refnes:
                if hypnes[ent] > 0:
                    results[mbr_file]['ref_in_hyp'] += 1
                    hypnes[ent] -= 1

    for mbr_file in args.hyp_files:
        recall = results[mbr_file]['ref_in_hyp'] / results[mbr_file]['total_ref']
        precision = results[mbr_file]['hyp_in_ref'] / results[mbr_file]['total_hyp']
        f1 = (2 * precision * recall)/(precision + recall)*100
        print(f"{mbr_file.name}\t{f1}")


if __name__ == '__main__':
    args = parse_args()
    main(args)
