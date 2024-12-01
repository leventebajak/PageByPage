import argparse
import os.path
import sys
import tkinter as tk
from tkinter import filedialog

from processing import process


def parse_page_param(pages: str) -> set[int]:
    result = set()
    for part in pages.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.update(range(start, end + 1))
        else:
            result.add(int(part))
    if len(result) == 0:
        raise ValueError('No pages selected.')
    return result


def yes_no_question(question: str) -> bool:
    while True:
        answer = input(f'{question} [Y/n] ').lower()
        if answer == '':
            print('Yes')
            return True
        if answer == 'y' or answer == 'yes':
            return True
        if answer == 'n' or answer == 'no':
            return False


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process a document page-by-page using an LLM.')
    parser.add_argument('document', type=str, help='The path to the document to process.')
    parser.add_argument('prompt', type=str, help='The prompt to use for generation.')
    parser.add_argument('--pages', type=str, default='all', help='The pages to process.')
    parser.add_argument('--output', type=str, help='The path to save the output to.')
    args = parser.parse_args()

    document = args.document
    if not os.path.isfile(document):
        parser.error(f'The document {document} does not exist.')

    prompt = args.prompt

    all_pages = args.pages == 'all'
    try:
        pages = parse_page_param(args.pages) if not all_pages else None
    except ValueError:
        parser.error('Invalid page parameter.')

    output = args.output
    if output is not None:
        if os.path.isdir(output):
            parser.error(f'The output path {output} is a directory.')
        if os.path.exists(output):
            overwrite = yes_no_question(f'The output file {output} already exists. Overwrite?')
            if not overwrite:
                print('Exiting.')
                sys.exit(1)

    return document, prompt, pages, output


def ask_parameters():
    output = None
    save_output = yes_no_question('Would you like to save the output to a file?')

    try:
        root = tk.Tk()
        root.withdraw()
        root.lift()
        root.attributes('-topmost', True)

        project_directory = os.path.dirname(os.path.abspath(__file__))

        document = filedialog.askopenfilename(title='Select the document to process',
                                              initialdir=project_directory,
                                              filetypes=[('PDF files', '*.pdf')])
        if document == '':
            print('No document selected.')
            sys.exit(1)
        print('Using document', document)

        if save_output:
            output = filedialog.asksaveasfilename(title='Select the file to save the output to',
                                                  initialdir=project_directory,
                                                  defaultextension='.txt',
                                                  filetypes=[('Text files', '*.txt')])
            if output == '':
                print('No output file selected.')
                sys.exit(1)
            print('Saving output to', output)
    except tk.TclError:
        document = None
        while not os.path.isfile(document):
            document = input('Enter the path to the document to process: ')
        if save_output:
            while not os.path.isfile(output):
                output = input('Enter the path to save the output to: ')

    all_pages = yes_no_question('Do you want to process all pages?')

    pages = None
    if not all_pages:
        while pages is None:
            try:
                pages = parse_page_param(input('Enter the pages to process (e.g. 1-3,5,7-10): '))
            except ValueError:
                pass

    prompt = input('Enter the prompt to use for generation:\n')

    return document, prompt, pages, output


if __name__ == '__main__':
    document, prompt, pages, output = parse_arguments() if len(sys.argv) > 1 else ask_parameters()

    print('Processing...')

    process(document, prompt, pages, output)
