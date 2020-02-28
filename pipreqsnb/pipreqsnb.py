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


def generate_pipreqs_str(path, options):
    extra_args = ' '.join(options)
    return '{} {}'.format(path, extra_args)


def run_pipreqs(args):
    print('pipreqs {}'.format(args))
    os.system('pipreqs {}'.format(args))


def main(path, extra_args):
    ipynb_files = [f for f in glob.glob(path + "**/*.ipynb", recursive=True)]
    temp_file_name = '{}/_pipreqsnb_temp_file.py'.format(path)
    imports = []
    for test_file in ipynb_files:
        nb = json.load(open(test_file, 'r'))
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                valid_lines = clean_invalid_lines_from_list_of_lines(cell['source'])
                source = ''.join(valid_lines)
                imports += get_import_string_from_source(source)

    try:
        with open(temp_file_name, 'a') as temp_file:
            for import_line in imports:
                temp_file.write('{}\n'.format(import_line))
        pipreqs_args = generate_pipreqs_str(path, extra_args)
        run_pipreqs(pipreqs_args)
        os.remove(temp_file_name)
    except Exception as e:
        if os.path.isfile(temp_file_name):
            os.remove(temp_file_name)
        raise e


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args, unknown_args = parser.parse_known_args()
    if len(vars(args)) != 1:
        raise Exception('only one argument supported: path')
    main(args.path, unknown_args)
