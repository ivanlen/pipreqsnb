#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ast
import shutil
import json
import os

pipreqs_options_store = ['use-local', 'debug', 'print', 'force', 'no-pin']
pipreqs_options_args = ['pypi-server', 'proxy', 'ignore', 'encoding', 'savepath', 'diff', 'clean']


def clean_invalid_lines_from_list_of_lines(list_of_lines):
    invalid_starts = ['!', '%']
    valid_python_lines = []
    for line in list_of_lines:
        if not any([line.startswith(x) for x in invalid_starts]):
            valid_python_lines.append(line)
    return valid_python_lines


def get_import_string_from_source(source):
    imports = []
    splitted = source.splitlines()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if any([isinstance(node, ast.Import), isinstance(node, ast.ImportFrom)]):
            imports.append(splitted[node.lineno - 1])
    return imports


def generate_pipreqs_str(args):
    pipreqs_str = ''
    for arg, val in args.__dict__.items():
        if arg.replace('_','-') in pipreqs_options_store and val:
            pipreqs_str += ' --{}'.format(arg.replace('_','-'))
        elif arg.replace('_','-') in pipreqs_options_args and val is not None:
            pipreqs_str += ' --{} {}'.format(arg.replace('_','-'), val)
    pipreqs_str += ' {}'.format(args.path)
    return pipreqs_str


def run_pipreqs(args):
    print('pipreqs {}'.format(args))
    os.system('pipreqs {}'.format(args))


def get_ipynb_files(path, ignore_dirs=None):
    parsed_ignore = ['.ipynb_checkpoints']

    if ignore_dirs:
        parsed_ignore_dirs = ignore_dirs.split(',')
        parsed_ignore.extend(parsed_ignore_dirs)

    ipynb_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in parsed_ignore]
        for name in files:
            f_path = os.path.realpath(os.path.join(root, name))
            ext = os.path.splitext(f_path)[1]
            if ext == '.ipynb':
                ipynb_files.append(f_path)
    return ipynb_files


def path_is_file(path):
    if os.path.isdir(path):
        return False, None
    elif os.path.isfile(path):
        extension = os.path.splitext(path)[1]
        if extension == '.py':
            is_nb = False
        elif extension == '.ipynb':
            is_nb = True
        else:
            raise Exception('file {} has an invalid extension {}'.format(path, extension))
        return True, is_nb
    else:
        raise Exception('{} if an invalid path'.format(path))


def set_requirements_savepath(args):
    if args.savepath is None:
        return os.path.join(os.path.dirname(args.path), 'requirements.txt')
    return args.savepath


def main():
    parser = argparse.ArgumentParser()
    for preqs_opt in pipreqs_options_store:
        parser.add_argument('--{}'.format(preqs_opt), action='store_true')
    for preqs_opt in pipreqs_options_args:
        parser.add_argument('--{}'.format(preqs_opt), type=str)
    parser.add_argument('path', nargs='?', default=os.getcwd())
    args = parser.parse_args()
    input_path = args.path
    is_file, is_nb = path_is_file(input_path)

    temp_file_name = '_pipreqsnb_temp_file.py'
    temp_path_folder_name = '__temp_pipreqsnb_folder'
    ignore_dirs = args.ignore if 'ignore' in args else None
    if is_file:
        temp_saving_path = os.path.join(os.getcwd(), temp_path_folder_name)
        if is_nb:
            ipynb_files = [input_path]
        else:
            ipynb_files = []
            os.makedirs(temp_saving_path, exist_ok=True)
            shutil.copyfile(input_path, os.path.join(temp_saving_path, temp_file_name))
    else:
        ipynb_files = get_ipynb_files(input_path, ignore_dirs=ignore_dirs)
        temp_saving_path = os.path.join(input_path, temp_path_folder_name)
    temp_file = os.path.join(temp_saving_path, temp_file_name)
    imports = []
    open_file_args = {}
    if args.encoding is not None:
        open_file_args['encoding'] = args.encoding
    for nb_file in ipynb_files:
        nb = json.load(open(nb_file, 'r', **open_file_args))
        try:
            for n_cell, cell in enumerate(nb['cells']):
                if cell['cell_type'] == 'code':
                    valid_lines = clean_invalid_lines_from_list_of_lines(cell['source'])
                    source = ''.join(valid_lines)
                    imports += get_import_string_from_source(source)
        except Exception as e:
            print(
                "Exception occurred while working on file {}, cell {}/{}".format(nb_file, n_cell + 1, len(nb['cells'])))
            raise e

    # hack to remove the indents if imports are inside functions
    imports = [i.lstrip() for i in imports]

    if is_file:
        args.savepath = set_requirements_savepath(args)
        args.path = temp_saving_path
    try:
        os.makedirs(temp_saving_path, exist_ok=True)
        with open(temp_file, 'a') as temp_file:
            for import_line in imports:
                temp_file.write('{}\n'.format(import_line))
        pipreqs_args = generate_pipreqs_str(args)
        run_pipreqs(pipreqs_args)
        shutil.rmtree(temp_saving_path)
    except Exception as e:
        if os.path.isfile(temp_file):
            os.remove(temp_file)
        raise e


if __name__ == '__main__':
    main()
