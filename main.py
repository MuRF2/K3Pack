import os
import logging
import getpass
import argparse
import requests
from requests import get
import json
import re

version_number = '0.1'
g_package_list_file_url = "https://raw.githubusercontent.com/MuRF2/K3Pack/master/packages_list.json"
g_package_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/package_list_file.json'
g_installed_list_file_path = '/home/' + getpass.getuser() + '/.k3pack/installed/installed_list_file.json'
g_install_folder_path = '/home/' + getpass.getuser() + '/.k3pack/installed/'

logger = logging.getLogger(__name__)


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


def delete_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def create_folder(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)


def download(file_path: str, url: str):
    """
    This function downloads and creates a file. The file location and download url is passed to the function.
    The filename is part of the path.
    :param file_path: storage location of new created file - type: str
    :param url: for get request - type:str
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
        "package1":
             {
                "name":"HelloWorld",
                "url":"https://yoururl.com",
                "version":1,
                "various":"-"
            }
    }
    The output dictionary would be:
    {'package1': {'name': 'HelloWorld', 'url': 'https://raw.githubusercontent.com/MuRF2/toolbox/main/HelloWorld.sh', 'version': 1, 'various': '-'}}
    :param path: storage location of json file
    :return: dict...
    """
    try:
        with open(path, 'r') as json_file:
            d = json.load(json_file)
        return d
    except FileNotFoundError as error:
        logger.error(error)
        raise


def get_sub_dict_by_package_name(dictionary: dict, package_name: str) -> dict or None:
    """

    :param dictionary:
    :param package_name:
    :return: dict or None
    """
    for key in dictionary:
        if dictionary[key]['name'] == package_name:
            return {key: dictionary[key]}


def reverse_parse_json_file(dictionary: dict, path: str):
    """
    This function reads in a dictionary and passes it to a json file. The Dictionary will be attached to the file.
    :param dictionary: values which will be parsed to json file
    :param path: storage location of new created file - type: str
    """
    try:
        with open(path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print('creating package file, initialization...')
        with open(path, "a") as file:
            json.dump(dictionary, file, indent=2)
    else:
        data.update(dictionary)
        with open(path, "w") as file:
            json.dump(data, file, indent=2)


def get_package_url(dictionary: dict, package_name: str) -> str or None:
    for key in dictionary:
        if dictionary[key]['name'] == package_name:
            return dictionary[key]['url']


def get_package_name_from_url(url):
    return re.findall('([^\/]+)\/?$', url).pop()


def refresh_package_list(file_path: str, url: str):
    delete_file(file_path)
    download(file_path, url)
    print('Package list updated.')


def install(package_name):
    d = parse_json_file(g_package_list_file_path)
    try:
        i = parse_json_file(g_installed_list_file_path)
    except FileNotFoundError:
        pass
    url = get_package_url(d, package_name)
    if url is None:
        print('ERROR: Package could not be found. List all available packages with ./k3pack list-available')
    if url is not None:
        if os.path.exists(g_install_folder_path + get_package_name_from_url(url)) is True:
            print("File / program already installed.")
        else:
            download(g_install_folder_path + get_package_name_from_url(url), url)
            print("downloaded...")
            reverse_parse_json_file(get_sub_dict_by_package_name(d, package_name), g_installed_list_file_path)


def list_installed():
    try:
        i = parse_json_file(g_installed_list_file_path)
        for key in i:
            print(i[key]['name'] + ' version: ' + i[key]['version'])
    except FileNotFoundError:
        print('No package installed')


def list_available():
    d = parse_json_file(g_package_list_file_path)
    for key in d:
        print(d[key]['name'] + ' version: ' + d[key]['version'])


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
        list_installed()
    elif arguments().main_operator == 'list-available':
        list_available()
