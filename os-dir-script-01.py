#

import os
import re
import typing
import argparse
from zipfile import ZipFile


# file/directory operations
# list files in directory
def get_directory_content(input_dir: str) -> typing.List[str]:
    dir_path = os.getcwd()
    directory_content = os.listdir(input_dir)
    
    return directory_content


# process files in directory
def process_file(
    input_list_files: typing.List[str], regex_expression: str
    ) -> typing.List[str]:
    _list = [f for f in input_list_files if re.match(regex_expression, f)]
    
    return _list


# process file list
def process_file_list(
    input_list: typing.List[str], strip_pattern: str, match_char: str, replace_char: str) -> typing.List[str]:
    l = [s.replace(match_char, replace_char).strip(strip_pattern).lower() for s in input_list]
    _dict = dict(zip(l, input_list))
    return _dict


# create new directory
def create_new_directory(
    input_dict: typing.Dict[str, str], new_dir_path: str='.') -> None:
    _list = [os.path.join(new_dir_path, d) for d in input_dict.keys()]
    for d in _list:
        os.makedirs(d, exist_ok=True)

    return _list

# move files to new directory
def move_file(_src, _dst) -> None:
    os.rename(_src, _dst)


# unzip files
def unzip_file(input_file: str, file_mode: str='r', dst_dir: str='.') -> None:
    with ZipFile(input_file, file_mode) as zipObj:
        zipObj.extractall(dst_dir)


# argparse
parser = argparse.ArgumentParser(
    description='Script to list files in a directory')
parser.add_argument(
    '-d', '--dir', help='Directory to list files', required=True)
args = parser.parse_args()
argparse_error_msg = 'Error: Directory does not exist'


# run script
if __name__ == '__main__':
    try:
        if os.path.isdir(args.dir):
            print('Directory: ' + args.dir)
            print('Files: ')
            for file in os.listdir(args.dir):
                pass
        else:
            print(argparse_error_msg)
    except Exception as e:
        print(e)

    f = get_directory_content(args.dir)

    r_str = r"^\d{2}\-(stu|evr)\_.*\.zip$"
    r = re.compile(r_str, re.IGNORECASE)

    l = process_file(f, r)
    s = process_file_list(l, '.zip', '_', '-')

    _dlist = create_new_directory(s, './tmp')

    _d = dict(zip(s, _dlist))

    # _dict = {k: "{0}/{1}".format(v, x) for k, v in _d.items() for x in l}

    for i in l:
        x = i.replace('_', '-').strip('.zip').lower()
        for k in _d.keys():
            if x == k:
                _dst = "{0}/{1}".format(_d[k], i)
                print(_dst)
                unzip_file(i, dst_dir=_d[k])
                move_file(i, _dst)
