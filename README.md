# pipreqsnb

This is a very simple fully compatible pipreqs wrapper that supports python files and jupyter notebooks.

- All the arguments and options are the same as pipreqs.
- pipreqs commands are still valid

__Please__ see [pipreqs](https://github.com/bndr/pipreqs/) documenation for more information.

## New
 - v 0.2.1: Single file support. You can either target a single python `file.py` or a single jupyter notebook
  `notebook.ipynb`, `<path>=single_file_path`.
- v 0.2.4: bugfix: bugfix for args with `-`
  
## Installation

    pip install pipreqsnb

## Usage


    Usage:
        pipreqsnb [options] <path> 
    
    Options:
        --use-local           Use ONLY local package info instead of querying PyPI
        --pypi-server <url>   Use custom PyPi server
        --proxy <url>         Use Proxy, parameter will be passed to requests library. You can also just set the
                              environments parameter in your terminal:
                              $ export HTTP_PROXY="http://10.10.1.10:3128"
                              $ export HTTPS_PROXY="https://10.10.1.10:1080"
        --debug               Print debug information
        --ignore <dirs>...    Ignore extra directories (sepparated by comma no space)
        --encoding <charset>  Use encoding parameter for file open
        --savepath <file>     Save the list of requirements in the given file
        --print               Output the list of requirements in the standard output
        --force               Overwrite existing requirements.txt
        --diff <file>         Compare modules in requirements.txt to project imports.
        --clean <file>        Clean up requirements.txt by removing modules that are not imported in project.
        --no-pin              Omit version of output packages.
