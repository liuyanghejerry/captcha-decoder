#!/usr/bin/env python

# -*- coding: utf-8  -*-

import sys, os, decoder

def print_help():
    info = '''
    You have nothing to give me. We need to talk.

    try_decoder file1 file2 file3
    or
    try_decoder dirname
    '''
    print info

def gen_filenames():
    if len(sys.argv) < 2:
        return []

    s_file = sys.argv[1]

    if os.path.isfile(s_file):
        return sys.argv[1:]
    else:
        files = []
        for f in os.listdir(s_file):
            files.append('%s/%s'%(s_file, f))
        return files

def main():
    files = gen_filenames()
    if not len(files):
        print_help()
        return

    for i, f in enumerate(files):
        ddd = decoder.Decoder()
        result = ddd.tryWholeFile(f)
        print "".join(result)

if __name__ == '__main__':
    main()
