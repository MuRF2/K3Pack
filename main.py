import os
import getpass
import argparse
import requests
from requests import get
import json

version_number = '0.1'
g_package_list_file_url = "https://raw.githubusercontent.com/MuRF2/K3Pack/master/packages_list.json"
g_package_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/package_list_file.json'
g_installed_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/installed_list_file'
g_install_folder_path = '/home/' + getpass.getuser() + '/.k3pack/installed'


def create_folder(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)


def arguments():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help',
                        action='help',
                        default=argparse.SUPPRESS,
                        help='K3Pack is an easy to use packet manager written in Python. Actually just a fun project.')
    parser.add_argument('-v', '--version',
                        action='version',
                        default=argparse.SUPPRESS,
                        version="Version {} is installed.".format(version_number),
                        help='show version number')
    parser.add_argument('-p', '--package',
                        type=str,
                        nargs=1,
                        help="package name for install and uninstall argument")
    parser.add_argument("main_operator",
                        type=str,
                        choices=["install", "uninstall", "list-installed", "list-available", "update"],
                        help="main operator to be selected")
    return parser.parse_args()


def refresh_package_list(file_path, url):
    delete_file(file_path)
    download(file_path, url)
    print('Package list updated.')


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
            print('An error occurred during download.')
            raise SystemExit(e)


def parse_json_file(path):
    try:
        with open(path, 'r') as json_file:
            d = json.load(json_file)
        return d
    except OSError as error:
        print(error)
        print('File not found, maybe you need to update the package list first?')


def install(package_name):
    packages = parse_json_file(g_package_list_file_path)
    available_flag = False
    size = len(packages.items())
    for x in range(0, size):
        value = list(packages.items())[x][1]
        for y in value:
            if y['name'] == package_name:
                available_flag = True
    if not available_flag:
        print("Package could not be found. List all available packages with ./k3pack list-available")


def list_available():
    print_package_names(parse_json_file(g_package_list_file_path))


def print_package_names(dictionary):
    size = len(dictionary.items())
    for x in range(0, size):
        value = list(dictionary.items())[x][1]
        for y in value:
            print(y['name'] + " version: " + str(y['version']))


def print_my_dictionary_value(dictionary, part):
    size = len(dictionary.items())
    for x in range(0, size):
        value = list(dictionary.items())[x][1]
        for y in value:
            print(y[part])


if __name__ == '__main__':

    if arguments().main_operator == 'update':
        refresh_package_list(g_package_list_file_path, g_package_list_file_url)
    elif arguments().main_operator == 'install':
        create_folder(g_install_folder_path)
        install(arguments().package.pop())
    elif arguments().main_operator == 'uninstall':
        print('uninstall')
    elif arguments().main_operator == 'list-installed':
        print('list-installed')
    elif arguments().main_operator == 'list-available':
        list_available()

    # create folder for installations
    # create_folder(g_install_folder_path)




