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


def write_file(fname, sents, infix_paren):
    print "Writing to file:", fname
    with open(fname, "w") as f:
        for sent in sents:
            joined = ' '.join(sent)
            if infix_paren:
                joined = (
                    joined.replace('<', infix_paren).replace('>', infix_paren))
            f.write(joined + '\n')


def parse_morphology(sents, interactive=True):
    for expr, repl in res.morphology:
def parse_gloss(sents, interactive=True):
    try_exprs(res.glosses, sents, interactive=interactive)


        log.debug('Current REGEXP: {!r} --> {!r}'.format(expr.pattern, repl))
        try_expr(expr, repl, sents, interactive=interactive)
    try_suffixes(sents, interactive=interactive)


def try_expr(expr, repl, sents, interactive=True):
    skip_words = []
    repl_words = []
    for sent in sents:
        sent_msg = '\nCurrent Sentence: {}\n'.format(' '.join(sent))
        for j, word in enumerate(sent):
            if word not in skip_words and expr.search(word):
                new_word = expr.sub(repl, word)
                if interactive and word not in repl_words:
                    # This word hasn't been set to be ignored or replaced yet
                    replace, remember = conf_replace(sent_msg, word, new_word)
                    sent_msg = ''
                    if remember:
                        (repl_words if replace else skip_words).append(word)
                    if not replace:
                        continue
                log.info('Replacing: {} --> {}'.format(word, new_word))
                sent[j] = new_word
        log.debug("Result: " + ' '.join(sent))


def conf_replace(curr_sent_msg, word, new_word):
    print '{}Match found: {} --> {}'.format(curr_sent_msg, word, new_word)
    replace = yes_no("Replace (Y/n)?")
    remember = yes_no("Remember this choice (Y/n)? [U]ndo?", extra='u')
    while remember is None:
        replace = not replace
        print "Replacement changed to: {}".format("YES" if replace else "NO")
        remember = yes_no("Remember this choice (Y/n)? [U]ndo?", extra='u')
    return replace, remember


def try_suffixes(split_sents, interactive=True):
    words = {}
    for sent in split_sents:
        for j, word in enumerate(sent):
            if '@' in word:
                if word in words:
                    pass # Do nothing, just let the replacement happen
                elif not interactive:
                    words[word] = word.replace('@', '')
                else:
                    modify, new_word = conf_modify(word)
                    words[word] = new_word if modify else word.replace('@','')
                sent[j] = words[word]


def modify_loop(word):
def conf_modify(word):
    print "\nFound word with suffix:", word
    while True:
        modify = yes_no("Modify root (y/N)?", default=False)
        if modify:
            break
        if yes_no("Are you sure (Y/n)?"):
            return modify, None
    while True:
        repl = res.suffix[1].format(raw_input("Enter new root: ").lower())
        new_word = res.suffix[0].sub(repl, word)
        if repl and yes_no(
                "Confirm change: {} --> {} (Y/n)? ".format(word, new_word)):
            return modify, new_word


def yes_no(msg, default=True, extra=None):
    response = 'no response'
    while response:
        if response in 'nN':
            return False
        elif response in 'yY':
            return True
        elif extra and response.lower() in extra:
            return None
        else:
            response = raw_input(msg + ' ')
    else:
        return default


def can_interrupt(f, sents, fname, infix, interactive=True):
    try:
        f(sents, interactive=interactive)
    except KeyboardInterrupt:
        if yes_no("\n\nKeyboardInterrupt caught. Output intermediate "
                  "results to a file (y/N)?", default=False):
           write_file(fname, sents, infix)
        exit()
    write_file(fname, sents, infix)


def parse_args():
    parser = argparse.ArgumentParser(description="Semi-automatically perform morphological parsing of Tagalog sentences")
    parser.add_argument("-p", "--only-parse", action="store_true",
                        help="Only run parsing algorithm; assumes preprocessed "
                             "sentences")
    parser.add_argument("-g", "--only-gloss", action="store_true",
                        help="Only run glossing algorithm; assumes "
                             "morphologically parsed input")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print debugging messages")
    parser.add_argument("-n", "--non-interactive", action="store_false",
                        help="Disable yes_noation messages; all matches will "
                        "be automatically replaced; intended for debugging")
    parser.add_argument("-i", "--infix",
                        help="Set an alternative string for delimiting infixes")
    parser.add_argument("file",
                        help="File to parse; must be plain text, ideally with "
                        "one line corresponding to one sentence")
    return parser.parse_args()


def main():
    if args.verbose:
        log.setLevel(logging.DEBUG)

    fname = args.file
    sents = read_file(fname)
    log.debug('SENTENCES:\n  ' + '\n  '.join(sents))
    sents = [sent.split() for sent in sents]

    if not args.only_gloss:
        can_interrupt(parse_morphology, sents, fname + '.parsed',
            args.infix, interactive=args.non_interactive)
    if not args.only_parse:
        can_interrupt(parse_gloss, sents, fname + '.glossed',
            args.infix, interactive=args.non_interactive)


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    args = parse_args()
    main()
