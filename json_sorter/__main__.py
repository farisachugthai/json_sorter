"""Console script for json_sorter."""
import argparse
import sys


def main():
    """Console script for json_sorter.

    Parse arguments given by the user.

    This implementation still, somehow isn't done. An option for *inplace*
    modifications needs to be added.

    Unfortunately this will be mutually exclusive to the output file option.
    So we'll need to work on learning argparse.mutually_exclusive_groups.

    Returns
    -------
    args : :class:`argparse.NameSpace()`
        Arguments provided by the user and handled by argparse.

    """
    parser = argparse.ArgumentParser(
        prog="JSON sorter",
        description="Take a :mod:`json` file, sort the keys and insert 4 spaces for indents.",
    )

    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="File to parse. Defaults to stdin.",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=sys.stdout,
        type=argparse.FileType(mode="w"),
        help="File to write to. Defaults to stdout.",
    )

    parser.add_argument(
        "-y",
        "--yaml",
        dest="yaml",
        default=sys.stdout,
        type=argparse.FileType(mode="w"),
        help="YAML file to write to. Defaults to stdout.",
    )

    # is there a way to have info printed with this from argparse?
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        dest="log",
        default=False,
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

    return args


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
