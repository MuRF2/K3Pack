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
                        choices=["install", "uninstall", "list-installed", "list-available", "update", "test"],
                        help="main operator to be selected")
    return parser.parse_args()


def init():
    if os.path.exists(g_install_folder_path) is not True:
        create_folder(g_install_folder_path)
    if os.path.exists(g_package_list_file_path) is not True:
        refresh_package_list(g_package_list_file_path, g_package_list_file_url)


def delete_file(path):
    try:
        os.remove(path)
    except OSError as e:
        print(e)


def create_folder(path):
    try:
        os.mkdir(path)
    except OSError as e:
        print(e)


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
            logger.error(e)
            raise


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
    except FileNotFoundError as e:
        print('Empty or no installed packages file.')
        logger.error(e)
        raise


def get_sub_dict_by_package_name(dictionary: dict, package_name: str, depth: int) -> dict or None:
    for key in dictionary:
        if dictionary[key]['name'] == package_name:
            if depth == 1:
                return {key: dictionary[key]}
            if depth == 2:
                return dictionary[key]


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
        with open(path, "a") as file:
            json.dump(dictionary, file, indent=2)
    else:
        data.update(dictionary)
        with open(path, "w") as file:
            json.dump(data, file, indent=2)


def get_package_url(dictionary: dict) -> str:
    return dictionary['url']


def get_package_name(dictionary:dict) -> str:
    return dictionary['name']


def get_package_name_from_url(url):
    return re.findall('([^\/]+)\/?$', url).pop()


def get_package_num(d, package_name):
    return list(get_sub_dict_by_package_name(d, package_name, 1).keys()).pop()


def check_if_installed(package_name):
    d = parse_json_file(g_package_list_file_path)
    sub_d = get_sub_dict_by_package_name(d, package_name, 2)
    if sub_d is not None:
        try:
            i = parse_json_file(g_installed_list_file_path)
            package_name_package_num_as_string = get_package_num(d, package_name)
            all_installed_package_num = list(i.keys())
            if package_name_package_num_as_string in all_installed_package_num:
                return True
            else:
                return False
        except FileNotFoundError:
            print('No packages list of installed programs available')
            return False
    else:
        print('package does not exist')
        return False


def refresh_package_list(file_path: str, url: str):
    delete_file(file_path)
    download(file_path, url)
    print('Package list updated.')


def update(package_name):
    if check_if_installed(package_name) is True:
        d = parse_json_file(g_package_list_file_path)
        sub_d = get_sub_dict_by_package_name(d, package_name, 2)
        i = parse_json_file(g_installed_list_file_path)
        sub_i = get_sub_dict_by_package_name(i, package_name, 2)
        if sub_d['version'] != sub_i['version']:
            print('Updating package "' + package_name + '" version:"' + sub_i['version'] + '" to version:"' + sub_d['version'] + '"')
            uninstall(package_name)
            install(package_name)
        else:
            print('No update available')
    else:
        print('Package not installed')


def install(package_name):
    d = parse_json_file(g_package_list_file_path)
    sub_d = get_sub_dict_by_package_name(d, package_name, 2)
    if sub_d is not None:
        if check_if_installed(package_name) is not True:
            print('installing package named "' + sub_d['name'] + '" version "' + sub_d['version'] + '" from "' + sub_d['url'] + '"')
            download(g_install_folder_path + get_package_name_from_url(sub_d['url']), sub_d['url'])
            reverse_parse_json_file(get_sub_dict_by_package_name(d, package_name, 1), g_installed_list_file_path)
        else:
            print('Package already installed')
    else:
        print('Package does not exist')


def uninstall(package_name):
    d = parse_json_file(g_package_list_file_path)
    sub_d = get_sub_dict_by_package_name(d, package_name, 2)

    if check_if_installed(package_name) is True:
        print('uninstalling package named "' + sub_d['name'] + '" version "' + sub_d['version'] + '"')
        i = parse_json_file(g_installed_list_file_path)
        del i[get_package_num(d, package_name)]
        delete_file(g_installed_list_file_path)
        delete_file(g_install_folder_path + get_package_name_from_url(sub_d['url']))
        reverse_parse_json_file(i, g_installed_list_file_path)
    else:
        print('Packages is not installed')


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
        try:
            update(arguments().package.pop())
        except AttributeError:
            refresh_package_list(g_package_list_file_path, g_package_list_file_url)
    elif arguments().main_operator == 'install':
        init()
        try:
            install(arguments().package.pop())
        except AttributeError:
            print('ERROR: parameter install needs another attribute')
    elif arguments().main_operator == 'uninstall':
        init()
        try:
            uninstall(arguments().package.pop())
        except AttributeError:
            print('ERROR: parameter uninstall needs another attribute')
    elif arguments().main_operator == 'list-installed':
        init()
        list_installed()
    elif arguments().main_operator == 'list-available':
        init()
        list_available()
    elif arguments().main_operator == 'test':
        print('test')
