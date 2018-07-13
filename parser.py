#!/usr/bin/python
"""
Main script file
Currently not functional
"""
import re
import regexps as res
import argparse
import logging
logging.basicConfig()

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

def write_file(fname, sents):
    print "Writing to file:", fname
    with open(fname, "w") as f:
        for sent in sents:
            f.write(' '.join(sent) + '\n')

def try_expr(expr, repl, sents):
    skip_words = []
    repl_words = []

    for sent in sents:
        print 'Current Sentence:', ' '.join(sent)
        for j, word in enumerate(sent):
            if word not in skip_words and expr.search(word):
                # Match found and not skipped
                new_word = expr.sub(repl, word)
                if word not in repl_words:
                    # This word hasn't been set to be ignored or replaced yet
                    print 'Match found: {} --> {}'.format(word, new_word)
                    replace = confirm('Replace')
                    remember = confirm('Remember this choice')
                    if remember:
                        (repl_words if replace else skip_words).append(word)
                    if not replace:
                        continue
                log.info('Replacing: {} --> {}'.format(word, new_word))
                sent[j] = new_word
        log.debug("Result: " + ' '.join(sent))
        print

def do_expr(expr, repl, sents):
    """
    Replacement function that doesn't ask for user confirmation. Intended for
    debugging, to cut down on the need for user input.
    --> I feel like there should be a way to create some common functions that can be called by either X_expr() function...
    """
    for sent in sents:
        print 'Current Sentence:', ' '.join(sent)
        for j, word in enumerate(sent):
            if expr.search(word):
                new_word = expr.sub(repl, word)
                print 'Replacing: {} --> {}'.format(word, new_word)
                sent[j] = new_word
        log.debug("Result: " + ' '.join(sent))
        print


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


def find_replace(sents, non_interactive=False):
    split_sents = [sent.split() for sent in sents]
    run_expr = do_expr if non_interactive else try_expr
    for expr, repl in res.morphology:
        log.debug('Current REGEXP: ' + repr(expr.pattern))
        run_expr(expr, repl, split_sents)
    return split_sents


def main():
    parser = argparse.ArgumentParser(description="Semi-automatically perform morphological parsing of Tagalog sentences")
    parser.add_argument("-p", "--parse", action="store_true",
                        help="Run parsing algorithm; assumes preprocessed "
                             "sentences, runs before glossing algorithm")
    parser.add_argument("-g", "--gloss", action="store_true",
                        help="Run glossing algorithm; assumes morphologically "
                             "parsed input, or runs after parser")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print debugging messages")
    parser.add_argument("-n", "--non-interactive", action="store_true",
                        help="Disable confirmation messages; all matches will "
                        "be automatically replaced")
    parser.add_argument("file", help="File to parse")

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    fname = args.file
    sents = read_file(fname)
    log.debug('SENTENCES:\n  ' + '\n  '.join(sents))

    sents = find_replace(sents, non_interactive=args.non_interactive)
    write_file(fname + '.parsed', sents)

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    main()
