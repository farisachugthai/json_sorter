#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main module."""
import argparse
import json
import logging
import os
import sys
from pathlib import Path

import yaml

from pyutil.__about__ import __version__

LOGGER = logging.Logger(name=__name__)


def _parse_arguments():
    """Parse arguments given by the user.

    Returns
    -------
    args : :class:`argparse.NameSpace()`
        Arguments provided by the user and handled by argparse.

    """
    parser = argparse.ArgumentParser(
        prog="JSON sorter",
        description="Take a json file, sort the keys and insert 4 spaces for indents.",
    )

    parser.add_argument(
        "input",
        help="JSON file to parse.",
    )

    parser.add_argument(
        "-o",
        "--output",
        # default=sys.stdout,
        # type=argparse.FileType(mode="w"),
        help="File to write to. Defaults to stdout.",
    )

    filetypes = parser.add_mutually_exclusive_group()
    filetypes.add_argument(
            "-c",
            "--csv",
            action='store_true',
            help="Convert the sorted output to csv.",
        )

    filetypes.add_argument(
            "-y",
            "--yaml",
            action='store_true',
            help="Convert the sorted output to yaml.",
            )

    # Should probably implement this and CSV as subcommands
    # parser.add_argument(
    #     "--yaml-file",
    #     dest="yaml",
    #     default=sys.stdout,
    #     type=argparse.FileType(mode="w"),
    #     help="YAML file to write to. Defaults to stdout.",
    # )

    # is there a way to have info printed with this from argparse?
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        dest="log",
        default=False,
        help="Turn logging on and print to console.",
    )

    log_levels = parser.add_mutually_exclusive_group()
    log_levels.add_argument(
        "-ll",
        "--log_level",
        dest="log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )

    log_levels.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Shorthand for setting default log level to DEBUG."
        )

    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s" + __version__
    )

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    # Handling the arguments prematurely. If this begins running away
    # in complexity do this and maybe even parse_args in a separate function
    if args.log_level is None:
        # no LOG_LEVEL specified but -l was specified
        if hasattr(args, 'log'):
            LOG_LEVEL = "WARNING"
    else:
        LOG_LEVEL = args.log_level
    LOGGER.setLevel(level=LOG_LEVEL)

    return args


def convert_to_yaml(file_obj):
    """Convert a :mod:`json` file to a YAML string.

    Parameters
    ----------
    file_obj : str
        The file to read in

    Returns
    -------
    yaml_object : str
        Converted :mod:`PyYAML` text.

    """
    converted_json_data = sort_json(file_obj)
    # output yaml
    yaml_text = yaml.dump(yaml.load(converted_json_data), default_flow_style=False)
    return yaml_text


def csv_to_json(file_obj):
    """Convert a csv file to json.

    Parameters
    ----------
    file_obj : Path
        A path to a csv file

    Returns
    -------
    str
        JSON encoded object

    """
    import csv
    if not Path(f).is_file():
        raise FileNotFoundError

    with open(file_obj) as f:
        csv_file = list(csv.reader(f))
        return json.dumps(csv_file)


def write_csv(data, filename):
    import csv
    data = json.loads(data)
    with open(filename, "wt") as f:
        writer = csv.DictWriter(f, data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def convert_to_csv(json_string):
    import csv
    import tempfile
    # csv module expects file objects so write it to a tempfile and work off of that
    tmp = tempfile.NamedTemporaryFile(mode="wt")
    tmp.write(json_string)
    csv_list = []
    with open(tmp.name) as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                csv_list.append(row)
        except csv.Error as e:
            print('line{}: {}'.format(reader.line_num, e))
    return csv_list


def sort_json(file_obj):
    """Read in a :mod:`json` object, sort it and write it back to a new file.

    By writing to a new file, the user is allowed the opportunity to inspect
    the file and ensure that the desired results have been achieved.

    Parameters
    ----------
    file_obj : str
        The file to read in

    Returns
    -------
    json_text : str
        Correctly formmated :mod:`json` text.

    """
    with open(file_obj) as f:
        settings = json.loads(f.read())

    json_str = json.dumps(settings, indent=4, sort_keys=True)

    logging.debug("Formatted json: %s\n" % str(json_str))
    return json_str


def text_writer(plaintext, output_file=None, csv=False, yaml=False):
    """Write the previously inputted text to a file.

    This function could easily be utilized over the whole package though.

    Parameters
    ----------
    plaintext : io.TextIOWrapper
        The file to read in as represented by an already open file handle.
        Needed to be done this way in case we write to sys.stdout and running
        ``open(path)`` raises an error.
        Alternatively handle the 2 situations where we get an io object and a
        Path object together in this function.
    output_file : os.PathLike
        Text file to write formatted :mod:`json` to.
        It will only write to the file if the filename currently doesn't exist.

    """
    # UGHH this is so fucked up because at every level of this program i have to check sys.stdout or path i need to open fuck
    if csv is True:
        if output_file is None:
            output_file = sys.stdout
        write_csv(plaintext, output_file)

    if output_file is None:
        output_file = sys.stdout
        output_file.write(plaintext)
    else:
        with open(output_file, "wt") as f:
            f.write(plaintext)
    logging.info("File written is: " + str(output_file))


def main():
    """Handles user args, sets up logging and calls other functions."""
    args = _parse_arguments()

    # TODO:
    # try:
    #     yaml = args.yaml
    # except AttributeError:
    #     plaintext = sort_json(fobj)
    # else:
    #     plaintext = convert_to_yaml(yaml)
    if args.csv is True:
        plaintext = convert_to_csv(sort_json(args.input))
    if args.yaml is True:
        plaintext = convert_to_yaml(sort_json(args.input))
    else:
        plaintext = sort_json(args.input)

    logging.debug("Plaintext is: " + str(plaintext))
    text_writer(plaintext, args.output, args.csv, args.yaml)


if __name__ == "__main__":
    main()
