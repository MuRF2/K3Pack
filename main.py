import getpass
import argparse
import filecmp
from requests import get

version_number = '0.1'
g_url = "https://raw.githubusercontent.com/MuRF2/K3Pack/master/packages_list"
g_package_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/package_list_file'


def modify_package_list_file(file_path):
    lines = ['Readme', 'How to write text files in Python']
    with open(file_path, 'a') as f:
        for line in lines:
            f.write(line)
            f.write('\n')


def compare(f1, f2):
    return filecmp.cmp(f1, f2, shallow=False)


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
    return args


class PackageList:

    @staticmethod
    def download(file_path, url):
        with open(file_path, "wb") as file:
            response = get(url)
            file.write(response.content)

    @staticmethod
    def load(file_path):
        return

    def __init__(self):
        self.__c_url = None
        self.__c_package_list_file_path = None
        self.__c_package_list_file = None

    def set_file_path(self, path):
        self.__c_package_list_file_path = path

    def get_file_path(self):
        return self.__c_package_list_file_path

    def set_url(self, url):
        self.__c_url = url

    def get_url(self):
        return self.__c_url

    def set_file(self, file):
        self.__c_package_list_file = file

    def get_file(self):
        return self.__c_package_list_file


def install(operator):
    return "test"


if __name__ == '__main__':
    parsed_argument = arguments()

    ThePackageList = PackageList()
    ThePackageList.set_file_path(g_package_list_file_path)
    ThePackageList.set_url(g_url)

    if parsed_argument.main_operator == 'update':
        ThePackageList.download(ThePackageList.get_file_path(), ThePackageList.get_url())
    elif parsed_argument.main_operator == 'install':
        print('install')
    elif parsed_argument.main_operator == 'uninstall':
        print('uninstall')
    elif parsed_argument.main_operator == 'list-installed':
        print('list-installed')
    elif parsed_argument.main_operator == 'list-available':
        print('list-available')







