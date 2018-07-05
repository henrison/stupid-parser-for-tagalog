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
        try_expr(expr, repl, split_sents)


def try_expr(expr, repl, sents):
    skip_words = []
    repl_words = []
    for sent in sents:
        print 'Current Sentence: ' + ' '.join(sent)
        for j, word in enumerate(sent):
            if word in skip_words:
                continue
            match = expr.search(word)
            if match:
                new_word = expr.sub(repl, word)
                if word in repl_words:
                    log.info('Replacing: {} --> {}'.format(word, new_word))
                    sent[j] = new_word
                else:
                    print 'Match found: {} --> {}'.format(word, new_word)
                    replace = confirm('Replace')
                    remember = confirm('Remember this choice')
                    if remember:
                        (repl_words if replace else skip_words).append(word)
                    if replace:
                        sent[j] = new_word
            else:
                continue
        log.debug(' '.join(sent))

def confirm(msg, default=True):
    skip = 'a'
    while skip:
        if skip in 'nN':
            return False
        elif skip in 'yY':
            return True
        else:
            skip = raw_input('  {} ({})? '.format(
                msg, 'Y/n' if default else 'y/N'))
    else:
        return default

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

    sents = read_file(fname)
    log.debug('SENTENCES:\n  ' + '\n  '.join(sents))

    find_replace(sents, None)

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    main()
