import os
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
    :param path: storage location of json file
    :return: for k3pack parsed dictionary
    """
    try:
        with open(path, 'r') as json_file:
            d = json.load(json_file)
        return d
    except OSError as error:
        print('ERROR: File not found.')


def reverse_parse_json_file(dictionary: dict, path: str):
    """
    This function reads in a dictionary and passes it to a json file. The Dictionary will be attached to the file.
    :param dictionary: values which will be parsed to json file
    :param path: storage location of new created file - type: str
    """
    with open(path, 'a') as file:
        json.dump(dictionary, file, indent=2)


def get_sub_dictionary_by_package_name(dictionary, package_name):
    for x in range(0, len(dictionary.items())):
        for y in list(dictionary.items())[x][1]:
            if y['name'] == package_name:
                return dict(zip(list(dictionary.items())[x][0], list(dictionary.items())[x][1]))


def get_package_url(dictionary: dict, package_name: str) -> str:
    """
    This function searches in a provided dictionary for the given name string for the matching url string.
    The given dictionary should be parsed using def parse_json_file(path: str) -> dict.
    If no matching package name is found, None is returned.
    :param dictionary: parsed by def parse_json_file(path: str) -> dict
    :param package_name: search name - type: str
    :return: url - type: str or None
    """
    for x in range(0, len(dictionary.items())):
        for y in list(dictionary.items())[x][1]:
            if y['name'] == package_name:
                return y['url']


def get_package_name(dictionary):
    for x in range(0, len(dictionary.items())):
        for y in list(dictionary.items())[x][1]:
            return y['name']


def get_package_name_from_url(url):
    return re.findall('([^\/]+)\/?$', url).pop()


def print_package_names_and_version(dictionary):
    for x in range(0, len(dictionary.items())):
        for y in list(dictionary.items())[x][1]:
            print(y['name'] + " version: " + str(y['version']))


def refresh_package_list(file_path: str, url: str):
    delete_file(file_path)
    download(file_path, url)
    print('Package list updated.')


def install(package_name):
    d = parse_json_file(g_package_list_file_path)
    url = get_package_url(d, package_name)
    if url is None:
        print('ERROR: Package could not be found. List all available packages with ./k3pack list-available')
    if url is not None:
        if os.path.exists(g_install_folder_path + get_package_name_from_url(url)) is True:
            # check version in installed_package_file
            print("File / program already installed.")
        else:
            download(g_install_folder_path + get_package_name_from_url(url), url)
            print("downloaded...")


def list_available():
    print_package_names_and_version(parse_json_file(g_package_list_file_path))


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
        data = parse_json_file(g_package_list_file_path)
        print(data)
        data2 = get_sub_dictionary_by_package_name(data, 'HelloWorld')
        print(data2)
        print('---------get url')
        print(get_package_url(data2, 'HelloWorld'))

        #list1 = list(data.items())[0][0]
        #list2 = list(data.items())[0][1]

        #print(list1)
        #print(list2)

    elif arguments().main_operator == 'list-installed':
        print('list-installed')
    elif arguments().main_operator == 'list-available':
        list_available()
