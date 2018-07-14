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


def parse_morphology(sents, non_interactive=False):
    split_sents = [sent.split() for sent in sents]
    try:
        for expr, repl in res.morphology:
            log.debug('Current REGEXP: {!r} --> {!r}'.format(expr.pattern, repl))
            try_expr(expr, repl, split_sents, non_interactive=non_interactive)
        handle_suffixes(split_sents, non_interactive=non_interactive)
    except KeyboardInterrupt:
        if not confirm("\n\nKeyboardInterrupt caught. Output intermediate "
                       "results to a file (y/N)?", default=False):
            exit()
    return split_sents


def try_expr(expr, repl, sents, non_interactive=False):
    skip_words = []
    repl_words = []
    for sent in sents:
        sent_msg = '\nCurrent Sentence: {}\n'.format(' '.join(sent))
        for j, word in enumerate(sent):
            if word not in skip_words and expr.search(word):
                new_word = expr.sub(repl, word)
                if not (non_interactive or word in repl_words):
                    # This word hasn't been set to be ignored or replaced yet
                    replace, remember = replace_loop(sent_msg, word, new_word)
                    sent_msg = ''
                    if remember:
                        (repl_words if replace else skip_words).append(word)
                    if not replace:
                        continue
                log.info('Replacing: {} --> {}'.format(word, new_word))
                sent[j] = new_word
        log.debug("Result: " + ' '.join(sent))


def replace_loop(curr_sent_msg, word, new_word):
    print '{}Match found: {} --> {}'.format(curr_sent_msg, word, new_word)
    replace = confirm("Replace (Y/n)?")
    remember = confirm("Remember this choice (Y/n)? [U]ndo?", extra='u')
    while remember is None:
        replace = not replace
        print "Replacement changed to: {}".format("YES" if replace else "NO")
        remember = confirm("Remember this choice (Y/n)? [U]ndo?", extra='u')
    return replace, remember


def handle_suffixes(split_sents, non_interactive=False):
    words = {}
    for sent in split_sents:
        for j, word in enumerate(sent):
            if '@' in word:
                if word in words:
                    pass
                elif non_interactive:
                    words[word] = word.replace('@', '')
                else:
                    modify, new_word = modify_loop(word)
                    words[word] = new_word if modify else word.replace('@','')
                sent[j] = words[word]


def modify_loop(word):
    print "\nFound word with suffix:", word
    while True:
        modify = confirm("Modify root (y/N)?", default=False)
        if modify:
            break
        if confirm("Are you sure (Y/n)?"):
            return modify, None
    while True:
        repl = res.suffix[1].format(raw_input("Enter new root: ").lower())
        new_word = res.suffix[0].sub(repl, word)
        if confirm("Confirm change: {} --> {} (Y/n)? ".format(word, new_word)):
            return modify, new_word


def confirm(msg, default=True, extra=None):
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


def main():
    parser = argparse.ArgumentParser(description="Semi-automatically perform morphological parsing of Tagalog sentences")
    # parser.add_argument("-p", "--parse", action="store_true",
    #                     help="Run parsing algorithm; assumes preprocessed "
    #                          "sentences, runs before glossing algorithm")
    # parser.add_argument("-g", "--gloss", action="store_true",
    #                     help="Run glossing algorithm; assumes morphologically "
    #                          "parsed input, or runs after parser")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print debugging messages")
    parser.add_argument("-n", "--non-interactive", action="store_true",
                        help="Disable confirmation messages; all matches will "
                        "be automatically replaced; intended for debugging")
    parser.add_argument("file",
                        help="File to parse; must be plain text, ideally with "
                        "one line corresponding to one sentence")

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    fname = args.file
    sents = read_file(fname)
    log.debug('SENTENCES:\n  ' + '\n  '.join(sents))

    sents = parse_morphology(sents, non_interactive=args.non_interactive)
    write_file(fname + '.parsed', sents)

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    main()
