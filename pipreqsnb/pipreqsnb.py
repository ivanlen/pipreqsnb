#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ast
import glob
import json
import os


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


def process_known_args(args):
    proc_args = ''
    for k, v in vars(args).items():
        if k != 'path':
            proc_args += '--{} {} '.format(k, v)
    proc_args += args.path
    return proc_args


def generate_pipreqs_str(args, options):
    known_args = process_known_args(args)
    extra_args = ' '.join(options)
    return '{} {}'.format(extra_args, known_args)


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore')
    parser.add_argument('path')
    args, unknown_args = parser.parse_known_args()
    path = args.path

    ignore_dirs = args.ignore if 'ignore' in args else None
    ipynb_files = get_ipynb_files(path, ignore_dirs=ignore_dirs)
    temp_file_name = '{}/_pipreqsnb_temp_file.py'.format(path)
    imports = []
    for nb_file in ipynb_files:
        nb = json.load(open(nb_file, 'r'))
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                valid_lines = clean_invalid_lines_from_list_of_lines(cell['source'])
                source = ''.join(valid_lines)
                imports += get_import_string_from_source(source)

    try:
        with open(temp_file_name, 'a') as temp_file:
            for import_line in imports:
                temp_file.write('{}\n'.format(import_line))
        pipreqs_args = generate_pipreqs_str(args, unknown_args)
        run_pipreqs(pipreqs_args)
        os.remove(temp_file_name)
    except Exception as e:
        if os.path.isfile(temp_file_name):
            os.remove(temp_file_name)
        raise e


if __name__ == '__main__':
    main()
