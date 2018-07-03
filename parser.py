#!/usr/bin/python
"""
Main script file
Currently not functional
"""
import re
import regexps as res
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)

def read_file(fname):
    print "Opening file:", fname
    sents = []
    with open(fname, "r") as f:
        punct = re.compile(r"[.,:;?!]")
        for line in f:
            line = line.strip()
            line = punct.sub("", line)
            if not line:
                continue
            line = line[0].lower() + line[1:]
            sents.append(line)
    if not sents:
        print "No sentences found. Exiting..."
        quit()
    return sents



def find_replace(sents, regexps):
    split_sents = [sent.split() for sent in sents]
    for expr, repl in res.morphology:
        log.debug('Current REGEXP: ' + repr(expr.pattern))
        for i, sent in enumerate(split_sents):
            # log.debug('Current Sentence: ' + sents[i])
            for j, word in enumerate(sent):
                match = expr.search(word)
                if match:
                    log.debug('Match found:\n  {!r:50}{}'.format(
                        expr.pattern, word))
                    log.debug('{:37}{}'.format(
                        'Sub result', expr.sub(repl, word)))
                else:
                    continue

def main():
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

    log = logging.getLogger(__name__)

    sents = read_file(fname)
    log.debug('SENTENCES:\n  ' + '\n  '.join(sents))

    find_replace(sents, None)

if __name__ == "__main__":
    main()
