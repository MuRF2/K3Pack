import os
import getpass
import argparse
import requests
from requests import get
import json

version_number = '0.1'
g_package_list_file_url = "https://raw.githubusercontent.com/MuRF2/K3Pack/master/packages_list"
g_package_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/package_list_file'
g_installed_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/installed_list_file'
g_install_folder_path = '/home/' + getpass.getuser() + '/.k3pack/installed'


def create_folder(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)


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


def refresh_package_list(file_path, url):
    delete_file(file_path)
    download(file_path, url)


def delete_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def download(file_path, url):
    with open(file_path, "wb") as file:
        try:
            response = get(url)
            file.write(response.content)
        except requests.exceptions.ConnectionError as e:
            print('An error occurred during packet list download')
            raise SystemExit(e)


def parse_json(x_json):
    return json.loads(x_json)


def load_installed_packages(path):
    with open(path) as json_file:
        data = json.load(json_file)

        print("Type:", type(data))

        print("\nname")

def install(operator):
    return "test"


if __name__ == '__main__':

    if arguments().main_operator == 'update':
        refresh_package_list(g_package_list_file_path, g_package_list_file_url)
    elif arguments().main_operator == 'install':
        print('install')
    elif arguments().main_operator == 'uninstall':
        print('uninstall')
    elif arguments().main_operator == 'list-installed':
        print('list-installed')
    elif arguments().main_operator == 'list-available':
        print('list-available')

    # create folder for installations
    # create_folder(g_install_folder_path)
    load_installed_packages(g_package_list_file_path)





