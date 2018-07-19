#!/usr/bin/python
"""
Main script file
"""
import re
import regexps as res
import argparse
import logging
logging.basicConfig()

def read_file(fname, infix_paren):
    print "Opening file:", fname
    sents = []
    with open(fname, "r") as f:
        punct = re.compile(r"[.,:;?!]")
        infix = re.compile(r"(?<!<){0}(um|in){0}(?!>)".format(infix_paren))
        for line in f:
            line = line.strip()
            line = punct.sub("", line)
            line = infix.sub(r"<\1>", line)
            if not line:
                continue
            line = line[0].lower() + line[1:]
            sents.append(line)
    if not sents:
        print "No sentences found. Exiting..."
        quit()
    return sents


def write_file(fname, sents, infix_paren):
    re_infix = re.compile(r"[<>]")
    print "Writing to file:", fname
    with open(fname, "w") as f:
        for sent in sents:
            joined = ' '.join(sent)
            if infix_paren:
                joined = re_infix.sub(infix_paren, joined)
            f.write(joined + '\n')


def parse_morphology(sents, interactive=True):
    try_exprs(res.morphology, sents, interactive=interactive)
    try_linker(sents, interactive=interactive)
    try_suffixes(sents, interactive=interactive)
    try_exprs(res.null_pv, sents, interactive=interactive)


def parse_gloss(sents, interactive=True):
    try_exprs(res.glosses, sents, interactive=interactive)


def try_exprs(exprs, sents, interactive=True):
    for expr, repl in exprs:
        log.debug('Current REGEXP: {!r} --> {!r}'.format(expr.pattern, repl))
        try_expr(expr, repl, sents, interactive=interactive)


def try_expr(expr, repl, sents, interactive=True):
    skip_words = []
    repl_words = []
    for sent in sents:
        sent_msg = '\nCurrent Sentence: {}\n'.format(' '.join(sent))
        for j, word in enumerate(sent):
            if word not in skip_words and expr.search(word):
                new_word = expr.sub(repl, word)
                if word not in repl_words:
                    replace, remember = conf_replace(
                        sent_msg, word, new_word, interactive=interactive)
                    sent_msg = ''
                    if remember:
                        (repl_words if replace else skip_words).append(word)
                    if not replace:
                        continue
                log.info('Replacing: {} --> {}'.format(word, new_word))
                sent[j] = new_word
        log.debug("Result: " + ' '.join(sent))


def try_linker(sents, interactive=True):
    saved = {}
    for sent in sents:
        for i, word in enumerate(sent):
            if word.endswith('ng') and len(word) > 3:
                try:
                    sent[i] = saved[word]
                except:
                    new_word, remember = conf_linker(                       word, interactive=interactive)
                    if remember:
                        saved[word] = new_word
                    sent[i] = new_word


def try_suffixes(sents, interactive=True):
    saved = {}
    skip_words = []
    re_suffix, template = res.suffix
    for sent in sents:
        for j, word in enumerate(sent):
            if word in skip_words:
                continue
            match = re_suffix.search(word)
            if not match:
                continue
            root = match.group(1)
            try:
                repl = template.format(saved[root])
                sent[j] = re_suffix.sub(repl, word)
            except KeyError:
                new_root, remember = conf_suffix(
                    word, root, interactive=interactive)
                if new_root:
                    repl = template.format(new_root)
                    sent[j] = re_suffix.sub(repl, word)
                if remember:
                    if new_root:
                        saved[root] = new_root
                    else:
                        skip_words.append(word)


def conf_replace(curr_sent_msg, word, new_word, interactive=True):
    if not interactive:
        return True, True
    print '{}Match found: {} --> {}'.format(curr_sent_msg, word, new_word)
    replace = yes_no_loop("Replace (Y/n)?")
    remember = yes_no_loop("Remember this choice (Y/n)? [U]ndo?", extra='u')
    while remember is None:
        replace = not replace
        print "Replacement changed to: {}".format("YES" if replace else "NO")
        remember = yes_no_loop("Remember this choice (Y/n)? [U]ndo?", extra='u')
    return replace, remember


def conf_linker(word, interactive=True):
    if not interactive:
        return word[:-2] + '=na'

    while True:
        if not yes_no_loop("\nParse linker for: {} (Y/n)?".format(word)):
            new_word = word
        elif yes_no_loop("Stem ends in 'n' (y/N)?", default=False):
            new_word = word[:-1] + '=na'
        else:
            new_word = word[:-2] + '=na'

        remember = yes_no_loop(
            "Remember: {} --> {} (Y/n)? [U]ndo?".format(word, new_word),
            extra='u')
        if remember is None:
            continue
        return new_word, remember


def conf_suffix(word, root, interactive=True):
    if not interactive:
        return root, True

    while True:
        if not yes_no_loop(
            "\nParse suffix for: {} with root {} (Y/n)?".format(word, root)):
            new_root = None
        else:
            new_root = raw_input(
                "Enter replacement for all instances of " + root +
                ", or enter nothing to keep as is: ").lower()
            if not new_root:
                new_root = root

        if new_root:
            repl = res.suffix[1].format(new_root)
            msg = "Remember change: {} --> {} (Y/n)? [U]ndo?".format(
                word, res.suffix[0].sub(repl, word))
        else:
            msg = "Remember no change (Y/n)? [U]ndo?"
        remember = yes_no_loop(msg, extra='u')
        if remember is None:
            continue
        return new_root, remember


def yes_no_loop(msg, default=True, extra=None):
    response = 'no response'
    while response:
        if response == 'n':
            return False
        elif response == 'y':
            return True
        elif extra and response in extra:
            return None
        else:
            response = raw_input(msg + ' ').lower()
    else:
        return default


def can_interrupt(f, sents, fname, infix, interactive=True):
    try:
        f(sents, interactive=interactive)
    except KeyboardInterrupt:
        if yes_no_loop("\n\nKeyboardInterrupt caught. Output intermediate "
                       "results to a file (y/N)?", default=False):
           write_file(fname, sents, infix)
        exit()
    write_file(fname, sents, infix)


def parse_args():
    parser = argparse.ArgumentParser(description="Semi-automatically perform morphological parsing of Tagalog sentences")
    # parser.add_argument("-p", "--parse", action="store_true",
    #                     help="Run parsing algorithm; assumes preprocessed "
    #                          "sentences, runs before glossing algorithm")
    # parser.add_argument("-g", "--gloss", action="store_true",
    #                     help="Run glossing algorithm; assumes morphologically "
    #                          "parsed input, or runs after parser")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print debugging messages")
    parser.add_argument("-n", "--non-interactive", action="store_false",
                        help="Disable confirmation messages; all matches will "
                        "be automatically replaced; intended for debugging")
    parser.add_argument("-i", "--infix",
                        help="Set an alternative string for delimiting infixes"
                        ", applies to input file and output file")
    parser.add_argument("file",
                        help="File to parse; must be plain text, ideally with "
                        "one line corresponding to one sentence")
    return parser.parse_args()


def main():
    if args.verbose:
        log.setLevel(logging.DEBUG)

    log.debug("ARGS: " + str(args))
    fname = args.file
    sents = read_file(fname, args.infix)
    log.debug('SENTENCES:\n  ' + '\n  '.join(sents))
    sents = [sent.split() for sent in sents]

    can_interrupt(parse_morphology, sents, fname + '.parsed',
        args.infix, interactive=args.non_interactive)


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    args = parse_args()
    main()
