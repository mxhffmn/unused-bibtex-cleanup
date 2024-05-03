#!/usr/bin/env python3

import argparse
import os
import re
from typing import Set

from pybtex.database.input import bibtex


def get_citations_from_file(file_path: str) -> Set[str]:
    """
    Returns a set of cited keys for the given file. Citations within a comment are ignored.
    :param file_path: the path to the file to search in
    :return: a set of all found citation keys
    """
    citations = set()

    regex = '\\\\(?:cite|citet|citet\\*|citep\\*|citep|citeauthor|citeyear)(?:\\[.*?\\])*{(.+?)}'

    # load content of file
    file_content = ''
    with (open(file_path, 'r')) as file:
        # read file line by line and do not look at lines that contain comments
        while True:
            line = file.readline()
            if not line:
                break

            if '%' not in line:
                file_content += line
            else:
                file_content += line.split('%', maxsplit=1)[0]

    # find all matches
    for match in re.findall(regex, file_content):
        # go through all matches and get group 0
        groups = match.split(',')
        for g in groups:
            citations.add(g.strip())

    return citations


def get_citations_in_folder(folder_path: str) -> Set[str]:
    """
    Returns a set of cited keys for all files in this folder or its sub folders.
    All files in there that have the ending .tex are searched. Citations within a comment are ignored.
    :param folder_path: the path to the root folder to search through
    :return: a set of all found citation keys
    """
    sub_folders = []
    tex_files = []
    with os.scandir(folder_path) as it:
        for f in it:
            if f.is_dir():
                sub_folders.append(f.name)
            if f.is_file() and f.name.endswith('.tex'):
                tex_files.append(f.name)

    # search all .tex files
    citations = set()
    for tex_file in tex_files:
        citations = citations.union(get_citations_from_file(os.path.join(folder_path, tex_file)))

    # recursively call all sub folders
    for folder in sub_folders:
        citations = citations.union(get_citations_in_folder(os.path.join(folder_path, folder)))

    return citations


def parse_args() -> argparse.Namespace:
    """
    Parses the arguments that were given via the command line.
    :return: the parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog='unused_bibtex_cleanup.py',
        usage='unused_bibtex_cleanup.py my_bibtex_file.bib my_folder_with_tex_files',
        description='Deletes unreferenced entries from a bibtex file. '
                    'References are searched in all files with the ending .tex in the given folder. '
                    'The behavior of the tool can be customized by multiple parameters.')
    parser.add_argument(dest='bib_file', type=str,
                        help='the path to the bibtex file. Can be absolute or relative.')
    parser.add_argument(dest='tex_folder', type=str,
                        help='the path to the folder of tex files to look through. '
                             'The path is searched recursively. Can be absolute or relative.')
    parser.add_argument('--no_comments', dest='no_comments', action='store_true',
                        help='if set, the unused entries will not remain in the output as comments.')
    parser.add_argument('--dry_run', dest='dry_run', action='store_true',
                        help='if set, the tool will perform a dry-run, only printing its actions '
                             'without actually performing them. This is useful for testing and debugging.')
    return parser.parse_args()


def unused_bibtex_cleanup():
    """
    Main method that is called when the script is executed
    """
    args = parse_args()

    if args.dry_run:
        print('Starting dry-run: no files will be created/no actions performed!')

    all_citations = get_citations_in_folder(args.tex_folder)

    print('Found the following citations in the files:')
    for cit in all_citations:
        print(cit)

    write_new_bibtex_file(all_citations, args.bib_file, args.no_comments, args.dry_run)


def write_new_bibtex_file(all_citations: Set[str], bib_file_path: str, no_comments: bool, dry_run: bool,
                          export_file_path: str = None):
    """
    Serializes the new content of the bibtex file and only includes those entries where keys are cited.
    :param all_citations: a set of all cited keys to include in the export
    :param bib_file_path: the file path to the bib file to read and write to
    :param no_comments: whether to omit unused entries as comments or not
    :param dry_run: whether to perform a dry-run, i.e., without file modifications
    :param export_file_path: a separate export file path (for testing purposes)
    """
    # load the bibtex file
    bib_file = bibtex.Parser().parse_file(bib_file_path)

    # iterate through all files and print the used ones as they are and the unused ones as a comment
    if not dry_run:
        if not export_file_path:
            f = open(bib_file_path, 'w')
        else:
            f = open(export_file_path, 'w')
        f.write('%%%%%%%%%%%%%%%%%%%%%%%\n')
        f.write('%%% MODIFIED BIBTEX %%%\n')
        f.write('%%%%%%%%%%%%%%%%%%%%%%%\n')
        f.write('\n')
    for entry in bib_file.entries:
        if entry in all_citations:
            # print original
            print(f'Printing entry of used key \'{entry}\'')
            if not dry_run:
                f.write(bib_file.entries[entry].to_string('bibtex'))
                f.write('\n')
        elif not no_comments:
            # print as comment
            print(f'Printing comment of entry of unused key \'{entry}\'')
            if not dry_run:
                ser_comm_entry: str = bib_file.entries[entry].to_string('bibtex')
                ser_comm_entry = ser_comm_entry[1:]  # alter original type to avoid problems with some parsers
                ser_comm_entry = '%' + ser_comm_entry.strip().replace('\n', '\n%') + '\n\n'  # add every line as comment
                f.write(ser_comm_entry)

    if not dry_run:
        f.close()


if __name__ == "__main__":
    unused_bibtex_cleanup()
