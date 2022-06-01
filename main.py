from pathlib import Path
import sys
import os
from pprint import pprint
import inquirer
import json
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_path():
    path = Path(__file__).resolve().parent
    print(f'you are here : {path}')
    path_input = input('input path [leave blank if its here]: ')
    if path_input == '' or path_input is None:
        path_input = path
    else:
        if not Path(path_input).exists():
            print('path not exists')
            return None
    return path_input


def get_files(path):
    files_list = os.popen(f'cd {path} && find -perm -g=x').read().replace('./', '').split('\n')
    return files_list


def select_files(files):
    select_files = input('do you want select files[Y/n]: ')
    if select_files == 'y' or select_files == 'Y':
        questions = [
            inquirer.Checkbox(
                "files",
                message="Select suspicious files [space bar for select] then press enter",
                choices=files
            )
        ]
        answers = inquirer.prompt(questions)['files']

    else:
        answers = files
    return answers


def detect_pid(files):
    detected = []
    for item in files:
        a = os.popen('ps -ef | grep -v grep | grep \'####\' | awk \'{print$2}\''.replace('####', item)).read()
        if a.replace('\n', '') is not None and a.replace('\n', '') != '':
            detected.append({item: {'PID': a.replace('\n', '')}})
    return detected


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = get_path()
    if path is None:
        sys.exit()
    files = get_files(path)[1:-1]
    selected = select_files(files)
    print('you select these files : ')
    detected = detect_pid(selected)
    print(json.dumps(detected, indent=2))
    print('Now you can kill with pids')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
