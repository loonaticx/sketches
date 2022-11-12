import subprocess
import os
import time
import sys
import psutil
import argparse

# https://manpages.ubuntu.com/manpages/focal/en/man1/pngcrush.1.html

parser = argparse.ArgumentParser()

parser.add_argument(
    '--selected_folders',
    '--folder',
    '--folders',
    action = 'extend',
    nargs = '+',
    type = str,
    metavar = 'models/',
    help = 'List of folders with subfolders to convert.'
)

parser.add_argument(
    '--rootonly',
    '--root',
    action = 'store_true',
    help = 'Just convert files in the root of the working directory.'
)

args = parser.parse_args()
selectedFolders = args.selected_folders
rootOnly = args.rootonly

allFiles = []

recursive = False
verbose = True

PNGCRUSH_ARGS = ['-brute', '-ow', '-rem', 'alla', '-m', '7',  'filename']
inputFile = '.png'

def convertFolders(folders):
    if recursive:
        for folder in folders:
            if not os.path.exists(folder):
                continue
            for root, _, files in os.walk(folder):
                for file in files:
                    if not file.endswith(inputFile):  # Input file
                        if verbose:
                            print("Skipping %s" % file)
                        continue
                    if verbose:
                        print("Adding %s" % file)
                    file = os.path.join(root, file)
                    allFiles.append(file)
    else:
        for file in os.listdir('.'):
            if not file.endswith(inputFile):
                if verbose:
                    print("Skipping %s" % file)
                continue
            if verbose:
                print("Adding in %s" % file)
            allFiles.append(file)
    for file in allFiles:
        PNGCRUSH_ARGS[6] = file
        subprocess.run(['pngcrush'] + PNGCRUSH_ARGS)

def convertRoot():
    if recursive:
        for root, _, files in os.walk('.'):
            for file in files:
                if not file.endswith(inputFile):  # Input file
                    if verbose:
                        print("Skipping %s" % file)
                    continue
                if verbose:
                    print("Adding %s" % file)
                file = os.path.join(root, file)
                allFiles.append(file)
    else:
        for file in os.listdir('.'):
            if not file.endswith(inputFile):
                if verbose:
                    print("Skipping %s" % file)
                continue
            if verbose:
                print("Adding in %s" % file)
            allFiles.append(file)
    for file in allFiles:
        PNGCRUSH_ARGS[6] = file
        subprocess.run(['pngcrush'] + PNGCRUSH_ARGS)


if selectedFolders:
    convertFolders(selectedFolders)
elif rootOnly:
    convertRoot()
