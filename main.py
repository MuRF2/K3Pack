import getpass
import argparse
import requests
from requests import get

version_number = '0.1'
g_package_list_file_url = "https://raw.githubusercontent.com/MuRF2/K3Pack/master/packages_list"
g_package_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/package_list_file'
g_installed_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/installed_list_file'


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
    return parser.parse_args()


def download(file_path, url):
    with open(file_path, "wb") as file:
        try:
            response = get(url)
            file.write(response.content)
        except requests.exceptions.ConnectionError as e:
            print('An error occurred during packet list download')
            raise SystemExit(e)


def install(operator):
    return "test"


if __name__ == '__main__':

    if arguments().main_operator == 'update':
        download(g_package_list_file_path, g_package_list_file_url)
    elif arguments().main_operator == 'install':
        print('install')
    elif arguments().main_operator == 'uninstall':
        print('uninstall')
    elif arguments().main_operator == 'list-installed':
        print('list-installed')
    elif arguments().main_operator == 'list-available':
        print('list-available')







