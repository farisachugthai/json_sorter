#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main module."""
import argparse
import csv
import json
import logging
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
# from tkinter import messagebox

from . import __version__


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
        "input", help="JSON file to parse.",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=sys.stdout,
        type=argparse.FileType(mode="w"),
        help="File to write to. Defaults to stdout.",
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
        help="Turn logging on and print to console.",
    )

    parser.add_argument(
        "-ll",
        "--log_level",
        dest="log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
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
        if hasattr(args, "log"):
            LOG_LEVEL = "WARNING"
        else:
            # Don't log
            LOG_LEVEL = 99
    else:
        LOG_LEVEL = args.log_level
    LOGGER = logging.Logger(name=__name__)
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
    import yaml
    yaml_text = yaml.dump(yaml.load(converted_json_data),
                          default_flow_style=False)
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
    if not Path(f).is_file():
        raise FileNotFoundError

    with open(file_obj) as f:
        csv_file = list(csv.reader(f))
        return json.dumps(csv_file)


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


def text_writer(plaintext, output_file=sys.stdout):
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
    output_file.write(plaintext)
    logging.info("File written is: " + str(output_file))


def getJSON(file_to_open):
    import_file_path = filedialog.askopenfilename()
    return import_file_path


def save_sorted_json(text):
    export_file_path = filedialog.asksaveasfilename(defaultextension=".json")
    with open(export_file_path, "wt") as f:
        f.write(sort_json(text))


def gui_main():
    root = tk.Tk()
    canvas1 = tk.Canvas(root, width=300, height=300, bg="lightsteelblue")
    canvas1.pack()

    label1 = tk.Label(root, text="File conversion tool")
    label1.config(font=("helvetica", 20))
    canvas1.create_window(150, 60, window=label1)

    browseButton_JSON = tk.Button(text="Select JSON file.", command=getJSON)
    canvas1.create_window(150, 130, window=browseButton_JSON)

    saveAsButton = tk.Button(
        text="Save sorted JSON to...", command=save_sorted_json)

    canvas1.create_window(150, 180, window=saveAsButton)

    def exitApplication():
        MsgBox = tk.messagebox.askquestion("Exit Application?")
        if MsgBox == "yes":
            root.destroy()

    exitButton = tk.Button(
        root, text="Exit application, command=exitApplication")
    canvas1.create_window(150, 230, window=exitButton)

    root.mainloop()


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
    plaintext = sort_json(args.input)

    logging.debug("Plaintext is: " + str(plaintext))
    text_writer(plaintext, args.output)


if __name__ == "__main__":
    # TODO: refactor GUI to new application
    # gui_main()
    main()
