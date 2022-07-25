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


def refresh_package_list(file_path: str, url: str):
    delete_file(file_path)
    download(file_path, url)
    print('Package list updated.')


def delete_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def download(file_path: str, url: str):
    """

    :param file_path:
    :param url:
    """
    with open(file_path, "wb") as file:
        try:
            response = get(url)
            file.write(response.content)
        except requests.exceptions.ConnectionError as e:
            print('ERROR: An error occurred during download.')
            raise SystemExit(e)


def parse_json_file(path: str) -> dict:
    """
    This function opens the file in json format specified with the path string and reads it into a dictionary.
    The .json file should be formatted as follows:
    {
        "package1":[
             {
                "name":"HelloWorld",
                "url":"https://yoururl.com",
                "version":1,
                "various":"-"
            }
        ]
    }
    The output dictionary would be:
    {'package1': [{'name': 'HelloWorld', 'url': 'https://yoururl.com', 'version': 1, 'various': '-'}]}
    :param path:
    :return: for k3pack parsed dictionary
    """
    try:
        with open(path, 'r') as json_file:
            d = json.load(json_file)
        return d
    except OSError as error:
        print('ERROR: File not found, maybe you need to update the package list first?')


def get_package_url(dictionary: dict, package_name: str) -> str:
    """
    This function searches in a provided dictionary for the given name string for the matching url string.
    The given dictionary should be parsed using def parse_json_file(path: str) -> dict.
    :param dictionary: parsed by def parse_json_file(path: str) -> dict
    :param package_name: search name - type: str
    :return: url - type: str
    """
    for x in range(0, len(dictionary.items())):
        for y in list(dictionary.items())[x][1]:
            if y['name'] == package_name:
                return y['url']


def install(package_name):
    d = parse_json_file(g_package_list_file_path)
    url = get_package_url(d, package_name)
    if url is None:
        print('ERROR: Package could not be found. List all available packages with ./k3pack list-available')
    if url is not None:
        print(url)


def list_available():
    print_package_names_and_version(parse_json_file(g_package_list_file_path))


def print_package_names_and_version(dictionary):
    for x in range(0, len(dictionary.items())):
        for y in list(dictionary.items())[x][1]:
            print(y['name'] + " version: " + str(y['version']))


if __name__ == '__main__':

    if arguments().main_operator == 'update':
        refresh_package_list(g_package_list_file_path, g_package_list_file_url)
    elif arguments().main_operator == 'install':
        try:
            install(arguments().package.pop())
        except AttributeError as error:
            print('ERROR: parameter install needs another attribute')

    elif arguments().main_operator == 'uninstall':
        print('uninstall')
    elif arguments().main_operator == 'list-installed':
        print('list-installed')
    elif arguments().main_operator == 'list-available':
        list_available()
