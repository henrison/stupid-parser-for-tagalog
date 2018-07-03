#!/usr/bin/python
"""
Main script file
Currently not functional
"""
import re
import regexps as res
import argparse

def read_file(fname):
    print "Opening file: ", fname
    sents = []
    with open(fname, "r") as f:
        punct = re.compile(r"[.,:;?!]")
        for line in f:
            line = line.strip()
            line = punct.sub("", line)
            if not line:
                continue
            sents.append(line[0].lower() + line[1:])
    if not sents:
        print "No sentences found. Exiting..."
        quit()
    for sent in sents: print sent
    return sents



def find_replace(sents, regexps):
    for expr, repl in res.morphology:
        expr.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semi-automatically perform morphological parsing of Tagalog sentences")
    parser.add_argument("-p", "--parse", action="store_true",
                        help="Run parsing algorithm; assumes preprocessed "
                             "sentences, runs before glossing algorithm")
    parser.add_argument("-g", "--gloss", action="store_true",
                        help="Run glossing algorithm; assumes morphologically "
                             "parsed input, or runs after parser")
    parser.add_argument("file", help="File to parse")

    args = parser.parse_args()
    fname = args.file

    sents = read_file(fname)
