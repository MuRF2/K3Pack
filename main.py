import argparse
import requests


version_number = '0.1'
url=""


def arguments():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='K3Pack is an easy to use packet manager written in Python. '
                             'Actually just a fun project.')
    parser.add_argument('-v', '--version', action='version', default=argparse.SUPPRESS,
                        version="Version {} is installed.".format(version_number), help='show version number')
    parser.add_argument("main_operator", type=str, choices=["install", "uninstall", "list-installed",
                                                            "list-available", "update"],
                        help="main operator to be selected")
    args = parser.parse_args()
    print(args.main_operator)

    return parser.parse_args()


class PackageList:
    def __init__(self):
        return

    def download(self, url, filename):
        return



def install(operator):
    return "test"


if __name__ == '__main__':
    print(arguments())





