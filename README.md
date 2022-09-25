# mbr-sensitivity
Data and code for the paper ["Identifying Weaknesses in Machine Translation Metrics Through Minimum Bayes Risk Decoding: A Case Study for COMET"](https://arxiv.org/pdf/2202.05148.pdf)

# Motivation

Neural metrics have achieved impressive correlation with human judgements in the evaluation of machine translation systems, but before we can safely optimise towards such metrics, we should be aware of (and ideally eliminate) biases toward bad translations that receive high scores. This repository provides all data and code to reproduce our [analysis](https://arxiv.org/pdf/2202.05148.pdf) that showed that [COMET](https://github.com/Unbabel/COMET) is not sensitive enough towards changes in numbers and named entities.

# Installation

To install this repository and its submodule.

git clone --recursive https://github.com/ZurichNLP/mbr-sensitivity

The evaluation scripts need numpy and [spaCy](https://spacy.io/) (to run named entity recognition). Please install numpy, spaCy and the corresponding language packages as follows:

    pip install numpy
    pip install spacy

    python -m spacy download de_core_news_lg
    python -m spacy download en_core_web_lg

To run MBR decoding with our fork of COMET, install COMET locally:

    cd COMET-mbr
    poetry install

# Automatic Analysis

If you want to reproduce the results of our automatic analysis (Tables 2 and 5 in the [paper](https://arxiv.org/pdf/2202.05148.pdf)), you can run the following command for numbers:

    python eval_scripts/evaluate_numbers.py -s paper_results/automatic_analysis/src.LANGPAIR.txt -f paper_results/automatic_analysis/METRIC.LANGPAIR.txt

and the following command for named entities:

    python eval_scripts/evaluate_nes.py -l TRGLANG -r paper_results/automatic_analysis/ref.LANGPAIR.txt -f paper_results/automatic_analysis/METRIC.LANGPAIR.txt

where `TRGLANG` is either "de" or "en",`LANGPAIR` is either "de-en" or "en-de" and `METRIC` is one of the following:

- `ref` for the reference translation.
- `alt` for the alternative translation.
- `beam-1` for the 1-best beam search outputs.
- `chrf++.mbr` for the MBR outputs with chrf++ as utility function.
- `chrf++.oracle` for the oracle outputs with chrf++ as utility function.
- `bleu.mbr` for the MBR outputs with bleu as utility function.
- `bleu.oracle` for the oracle outputs with bleu as utility function.
- `wmt20-comet-da.mbr` for the MBR outputs with wmt20-comet-da as utility function.
- `wmt20-comet-da.oracle` for the oracle outputs with wmt20-comet-da as utility function.
- `wmt21-comet-mqm.mbr` for the MBR outputs with wmt21-comet-mqm as utility function.
- `wmt21-comet-mqm.oracle` for the oracle outputs with wmt21-comet-mqm as utility function.
- `retrain-comet-da-0.2.mbr` for the MBR outputs with the COMET model retrained on 10% synthetic data and with a penalty of 0.2 as utility function.
- `retrain-comet-da-0.2.oracle` for the oracle outputs with the COMET model retrained on 10% synthetic data and with a penalty of 0.2 as utility function.
- `retrain-comet-da-0.5.mbr` for the MBR outputs with the COMET model retrained on 10% synthetic data and with a penalty of 0.5 as utility function.
- `retrain-comet-da-0.5.oracle` for the oracle outputs with the COMET model retrained on 10% synthetic data and with a penalty of 0.5 as utility function.
- `retrain-comet-da-0.8.mbr` for the MBR outputs with the COMET model retrained on 10% synthetic data and with a penalty of 0.8 as utility function.
- `retrain-comet-da-0.8.oracle` for the oracle outputs with the COMET model retrained on 10% synthetic data and with a penalty of 0.8 as utility function.

You can also provide multiple files for the `-f` argument. The script will print the results for every file to stdout (one file per line).

Note that newer spaCy model versions can result in different scores for the named entity evaluation but the gaps between the different metrics should be similarly large as in the [paper](https://arxiv.org/pdf/2202.05148.pdf).

If you want to compare a new utility function to our results, you can run MBR decoding using the samples provided under `paper_results/automatic_analysis/samples.de-en.txt` and `paper_results/automatic_analysis/samples.en-de.txt`.

If you want to evaluate on other test sets with these scripts, you need the source sentences, reference sentences and translations (and/or MBR outputs). The files should be parallel, in one-sentence-per-line format.

# Sensitivity Analysis

If you want to reproduce the results of our sensitivity analysis (as reported in Tables 3, 8, 9 and 10 and Figures 1 and 2 in the [paper](https://arxiv.org/pdf/2202.05148.pdf)), you can run the following command:

    python eval_scripts/evaluate_sensitivity.py -f paper_results/sensitivity_analysis/METRIC.TYPE.LANGPAIR.json

where `LANGPAIR` is either "de-en" or "en-de", `TYPE` is either "samples-as-support" (comparing each candidate to all other samples as in sampling-based MBR) or "references-as-support" (comparing each candidate against the two references as in oracle setup) and `METRIC` is one of the following:

- `wmt20-comet-da` for the MBR outputs with wmt20-comet-da as utility function.
- `wmt21-comet-mqm` for the MBR outputs with wmt21-comet-mqm as utility function.
- `retrain-comet-da-0.2` for the MBR outputs with COMET model retrained on 10% synthetic data and with a penalty of 0.2 as utility function.
- `retrain-comet-da-0.5` for the MBR outputs with COMET model retrained on 10% synthetic data and with a penalty of 0.5 as utility function.
- `retrain-comet-da-0.8` for the MBR outputs with COMET model retrained on 10% synthetic data and with a penalty of 0.8 as utility function.

The script prints the sensitivity scores for all error types to stdout. The rows will be ordered alphabetically after the names of the error types. You can also change the order of the rows by using the `-o/--order` argument or select only a subset of rows, e.g. only rows related to character-level named entity errors:

    python eval_scripts/evaluate_sensitivity.py -f paper_results/sensitivity_analysis/METRIC.TYPE.LANGPAIR.json -o ne-add ne-del ne-sub


# MBR with COMET

COMET now has an [official implementation of MBR decoding](https://github.com/Unbabel/COMET#scoring-mt-outputs) using the `comet-mbr` command. You may want to use this implementation for your own experiments with COMET as a utility function in MBR decoding.

Alternatively, you can use the scripts that we provide in the included submodule with our (older) fork of COMET. Our implementation of MBR decoding with COMET allows the candidates to be different from the support hypotheses. For general MBR decoding, where you have a source sentence, a set of X samples as candidates and a set of Y samples as support you can use this command:

    python COMET-mbr/run_mbr.py -s src.txt -c candidates.txt -t support.txt -nc X -ns Y -o mbr_out.txt

The format is one sentence per line. The number of lines in the candidate and support files need to be a multiple of the number of lines in the source file (line 1 = source sent "one", line 1-100 = candidates for source sentence "one" with 100 samples).

The output will be a file in one-sentence-per-line format with the MBR outputs (candidates with the highest utility / MBR score) for every source sentence.

Additionally, you can control the following arguments:

- `--batch_size` How many segments should be processed at the same timeß (default: 8)
- `--gpus` Number of GPUs to use, 0 = run on CPU (default: 1)
- `--model_name` Name of a COMET model or path to a checkpoint (default: 'wmt20-comet-da')

To get the individual MBR scores for the sensitivity analysis (with a potentially variable number of candidates), construct a json file of the following format containing the source sentence and at least one candidate. The candidates can be named arbitrarily:

    {
      "0": {
        "src": "Dem Feuer konnte Einhalt geboten werden",
        "cand-1": "The fire could be stopped",
        "cand-2": "They were able to control the fire."
      },
      "1": {
          "src": "Schulen und Kindergärten sind geöffnet",
          "cand-1": "Schools and kindergartens were open",
          "cand-2": "Schools and kindergartens opened"
      },
      ...
    }

If you set the batch size to 1, you can also use different numbers of candidates per sentence.

Then you can run the following script and it will return a json file of the same structure with a list where the first element is the sentence and the second the MBR score.

    python COMET-mbr/run_mbr_for_sensitivity.py -j candidates.json -t support.txt -ns Y -o mbr_out.json

If you want to reproduce the sensitivity scores in our paper, you can run the following command for sampling-based MBR decoding:

    python COMET-mbr/run_mbr_for_sensitivity.py -j paper_results/sensitivity_analysis/samples-as-support.de-en.json -t paper_results/sensitivity_analysis/samples-as-support.de-en.txt -ns 100 -o wmt20-comet-da.samples-as-support.json

and the following command for comparing to the two references:

    python COMET-mbr/run_mbr_for_sensitivity.py -j paper_results/sensitivity_analysis/references-as-support.de-en.json -t paper_results/sensitivity_analysis/references-as-support.de-en.txt -ns 2 -o wmt20-comet-da.references-as-support.json


# Retraining COMET

First, download the training data with the added synthetic data:

- [penalty 0.2](https://files.ifi.uzh.ch/cl/amrhein/mbr_paper/perturbed.2020.0.2.csv)
- [penalty 0.5](https://files.ifi.uzh.ch/cl/amrhein/mbr_paper/perturbed.2020.0.5.csv)
- [penalty 0.8](https://files.ifi.uzh.ch/cl/amrhein/mbr_paper/perturbed.2020.0.8.csv)

Fill in the missing paths in `train_scripts/train_perturbed_da.yaml` and `train_scripts/model_checkpoint_da.yaml`. Then start training using:

    comet-train --cfg train_scripts/train_perturbed_da.yaml

You can then specify the retrained checkpoint when calling `comet-score` via the `--model` argument or provide the new model path to the COMET MBR scripts above with the `--model_name` argument.

You can also download the checkpoints for the models we retrained for the paper:

- [retrain-comet-da-0.2](https://files.ifi.uzh.ch/cl/amrhein/mbr_paper/retrain-comet-da-0.2.zip)
- [retrain-comet-da-0.5](https://files.ifi.uzh.ch/cl/amrhein/mbr_paper/retrain-comet-da-0.5.zip)
- [retrain-comet-da-0.8](https://files.ifi.uzh.ch/cl/amrhein/mbr_paper/retrain-comet-da-0.8.zip)

# Citation

If you use this code or data, please cite our [paper](https://arxiv.org/pdf/2202.05148.pdf):

    @inproceedings{amrhein-sennrich-2022-identifying,
    title = "Identifying Weaknesses in Machine Translation Metrics Through Minimum Bayes Risk Decoding: A Case Study for {COMET}",
    author = {Amrhein, Chantal  and
      Sennrich, Rico},
    booktitle = "2nd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 12th International Joint Conference on Natural Language Processing",
    month = nov,
    year = "2022",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    eprint = {2202.05148}
    }
