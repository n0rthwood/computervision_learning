import argparse
import json
import os
from pygments import highlight, lexers, formatters

import config as config


def picture_loading_arg_process(basedir):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input",required=True, default="./",
                    help="path to input batch of image if not provided, current path will be used")
    ap.add_argument("-o", "--output", default=config.temp_path,
                    help="path to output batch of images, if not provided default system temp path")
    ap.add_argument("-f", "--filename_filter", default="*",
                    help="Filter for image files name, if not provided default *")

    ap.add_argument("-r", "--row", default=4, help="Row count of the image if not provided default 4")
    ap.add_argument("-co", "--column", default=6, help="Column count of the image if not provided default 6")
    ap.add_argument("-g", "--genre", default="general", help="Genre of the image if not provided default general")
    ap.add_argument("-ca", "--category", default="general",
                    help="Category of the image if not provided default general")

    parsed_arg = ap.parse_args()


    dirname = os.path.dirname(basedir)
    input_path = os.path.join(dirname, parsed_arg.input)
    output_path = os.path.join(dirname, parsed_arg.output)
    parsed_arg.input = input_path
    parsed_arg.output = output_path

    print('Using cmd options: ')
    formatted_json = json.dumps(vars(parsed_arg), indent=4)

    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)
    return parsed_arg
