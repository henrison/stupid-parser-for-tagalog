"""
Regular expressions go here
"""
import re
import itertools
# Morpheme-parsing regexps

_start = [
    (re.compile(r"^(napaka|pinaka)(?=\w{3})"),
        r"\1-"),
    # ni allomorph of <in>, with/without RED, with/without i-
    (re.compile(r"^ni([ly][aeiou])\1"),
        r"<in>-RED-\1"),
    (re.compile(r"^ni([ly][aeiou]\w)"),
        r"<in>-\1"),
    (re.compile(r"^ini([lyh]?[aeiou])\1"),
        r"i-<in>-RED-\1"),
    (re.compile(r"^ini([lyh]?[aeiou]\w)"),
        r"i-<in>-\1"),
    # Reduplication + Infixation
    (re.compile(r"(\w?)(um|in)([aeiou])\1\3"),
        r"<\2>-RED-\1\3"),
    # Infixation
    (re.compile(r"(\bi?)([^aeiou-]?)(?<!-)(um|in)(?=[aeiou]\w)"),
        r"\1<\3>-\2"),
]
_maN = [
    # MaN/PaN/NaN + RED
    (re.compile(r"\b([mpn]a)(ng|n|m)(\w{2})\3"),
        r"\1N-RED-\3"),
    (re.compile(r"\b([mpn]a)(ng)-([aeiou])\3"),
        r"\1N-RED-\3"),
    # MaN/PaN/NaN
    (re.compile(r"\b([mpn]a)(ng|n|m)([^aeiou])"),
        r"\1N-\3"),
]
_mag = [
    # Mag/Pag + RED
    (re.compile(r"\b([mpn]ag)(\w{2})\2"),
        r"\1-RED-\2"),
    (re.compile(r"\b([mpn]ag)-([aeiou])\2"),
        r"\1-RED-\2"),
    # Mag/Pag (Vowel-initial stems don't need changing)
    (re.compile(r"\b([mpn]ag)([^aeiou-])"),
        r"\1-\2"),
]
_ma = [
    # M-initial with RED
    # (re.compile(r"^(maka|naka)ka(?=\w{3})"),
    (re.compile(r"^([pmn])ak([ai])k\2(?=\w{3})"),
        r"\1ak\2-RED-"),
    (re.compile(r"^(maka|naka)([^aeiou]?[aeiou])\2"),
        r"\1-RED-\2"),
    (re.compile(r"^([pmn]a)([^aeiou]?[aeiou])\2"),
        r"\1-RED-\2"),
    # M-initial Prefixes
    (re.compile(r"^([pmn])ak([ai])(?=\w{3})"),
        r"\1ak\2-"),
    (re.compile(r"^([pmn]a)(?=\w{3})"),
        r"\1-"),
]
_end = [
    # i- morpheme
    (re.compile(r"(^|-)i(?=[^-]{4})"),
        r"\1i-"),
    # Recent Perfective
    (re.compile(r"^ka(\w{2})\1(?=\w)"),
        r"kaRED-\1"),
    (re.compile(r"^kaka(?=\w{3})"),
        r"kaRED-"),
    # Reduplication only
    (re.compile(r"\b([^aeiou]?[aeiou])\1"),
        r"RED-\1"),
    # ka- comitative
    (re.compile(r"(^|-)ka(?=[a-z]{3})"),
        r"\1ka-"),
]

morphology = itertools.chain(
    _start,
    _mag,
    _maN,
    _ma,
    _mag,
    _maN,
    _end
)
null_pv = [
    (re.compile(r"^(<in>|na|ma)-([\w-]+)(?<!-[ai]n)(=|$)"), r"\1-\2-(in)\3")]
suffix = (re.compile(r'([^-]{3,})([ia]n)(=|$)'), r'{}-\2\3')

# Glosses (IN PROGRESS)
"""
( |=)na( )
$1Lk$2

# PV Forms
na-([^(\s]+)-\(in\)
Nvol.Inch-$1-Pv
<in>-([^(\s]+)-\(in\)
<Inch>-$1-Pv

\bako(=|\s)
1sg.Nom$1
\b(ka|ikaw)(=|\s)
2sg.Nom$1
\bsiya(=|\s)
3sg.Nom$1
\bkami(=|\s)
1pl.Excl.Nom$1
\btayo(=|\s)
1pl.Incl.Nom$1
\bkayo(=|\s)
2pl.Nom$1
\bsila(=|\s)
3pl.Nom$1

\bko(=|\s)
1sg.Gen$1
\bmo(=|\s)
2sg.Gen$1
\bniya(=|\s)
3sg.Gen$1
\bnamin(=|\s)
1pl.Excl.Gen$1
\bnatin(=|\s)
1pl.Incl.Gen$1
\bnin?yo(=|\s)
2pl.Gen$1
\bnila(=|\s)
3pl.Gen$1

\bakin(=|\s)
1sg.Obl$1
\bi?yo(=|\s)
2sg.Obl$1
\bkani?ya(=|\s)
3sg.Obl$1
\bamin(=|\s)
1pl.Excl.Obl$1
\batin(=|\s)
1pl.Incl.Obl$1
\binyo(=|\s)
2pl.Obl$1
\bkanila(=|\s)
3pl.Obl$1
"""
