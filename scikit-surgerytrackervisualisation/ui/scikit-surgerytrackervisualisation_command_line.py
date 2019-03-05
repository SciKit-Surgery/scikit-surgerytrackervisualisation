# coding=utf-8

"""Command line processing"""


import argparse
from scikit-surgerytrackervisualisation import __version__
from scikit-surgerytrackervisualisation.application.scikit-surgerytrackervisualisation import run


def main(args=None):
    """Entry point for scikit-surgerytrackervisualisation application"""

    parser = argparse.ArgumentParser(description='scikit-surgerytrackervisualisation')

    # ADD OPTINAL ARGUMENTS
    parser.add_argument("-c", "--config",
                        action="store_true",
                        help="A configuration file."
                        )

    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable verbose output",
                        )

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgerytrackervisualisation version ' + friendly_version_string)

    args = parser.parse_args(args)

    run(args.config, args.verbose)
