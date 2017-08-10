# coding=utf-8
from __future__ import unicode_literals

import argparse
import io
import json
import os
from pprint import pprint

from snips_nlu import SnipsNLUEngine
from snips_nlu.languages import Language


def debug_training(dataset_path, text=None):
    if isinstance(text, str):
        text = text.decode("utf8")
    with io.open(os.path.abspath(dataset_path), "r", encoding="utf8") as f:
        dataset = json.load(f)
    language = Language.from_iso_code(dataset["language"])
    engine = SnipsNLUEngine(language).fit(dataset)
    if text is not None:
        pprint(engine.parse(text))


def debug_inference(engine_path, text):
    if isinstance(text, str):
        text = text.decode("utf8")
    with io.open(os.path.abspath(engine_path), "r", encoding="utf8") as f:
        engine_dict = json.load(f)
    engine = SnipsNLUEngine.from_dict(engine_dict)
    parse = engine.parse(text)
    print("Text: %s" % text)
    pprint("Parse: %s" % parse)


def main_debug():
    parser = argparse.ArgumentParser(description="Debug snippets")
    parser.add_argument("mode", type=unicode,
                        choices=["training", "inference"],
                        help="'training' to debug training and 'inference to "
                             "debug inference'")
    parser.add_argument("path", type=unicode,
                        help="Path to the dataset or trained assistant")
    parser.add_argument("--text", required=False, help="Input to parse")
    args = vars(parser.parse_args())
    mode = args.pop("mode")
    if mode == "training":
        debug_training(*args.values())
    elif mode == "inference":
        debug_inference(*args.values())
    else:
        raise ValueError("Invalid mode %s" % mode)


if __name__ == '__main__':
    main_debug()