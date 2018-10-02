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
    (re.compile(r"(^|-)i(?=[^-]{2})"),
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
_standalone_re = r"^{}$"
_with_linker_re = r"^{}\b"
_prefix_re = r"\b{}"
_suffix_re = r"{}\b"

_glosses = [
    (re.compile(r"\bna$"), None, r"Lk"),
    (r"na", _standalone_re, r"already"),
    (r"pa", _standalone_re, r"still"),
    # Pronouns
    (r"ako", _with_linker_re, r"1sg.Nom"),
    (r"(ka|ikaw)", _with_linker_re, r"2sg.Nom"),
    (r"siya", _with_linker_re, r"3sg.Nom"),
    (r"kami", _with_linker_re, r"1pl.Excl.Nom"),
    (r"tayo", _with_linker_re, r"1pl.Incl.Nom"),
    (r"kayo", _with_linker_re, r"2pl.Nom"),
    (r"sila", _with_linker_re, r"3pl.Nom"),
    (r"ko", _with_linker_re, r"1sg.Gen"),
    (r"mo", _with_linker_re, r"2sg.Gen"),
    (r"niya", _with_linker_re, r"3sg.Gen"),
    (r"namin", _with_linker_re, r"1pl.Excl.Gen"),
    (r"natin", _with_linker_re, r"1pl.Incl.Gen"),
    (r"nin?yo", _with_linker_re, r"2pl.Gen"),
    (r"nila", _with_linker_re, r"3pl.Gen"),
    (r"akin", _with_linker_re, r"1sg.Obl"),
    (r"i?yo", _with_linker_re, r"2sg.Obl"),
    (r"kani?ya", _with_linker_re, r"3sg.Obl"),
    (r"amin", _with_linker_re, r"1pl.Excl.Obl"),
    (r"atin", _with_linker_re, r"1pl.Incl.Obl"),
    (r"inyo", _with_linker_re, r"2pl.Obl"),
    (r"kanila", _with_linker_re, r"3pl.Obl"),
    (r"kita", _with_linker_re, r"1sg.Gen>2sg.Nom"),
    # Demonstratives
    (r"ito", _with_linker_re, r"Prox"),
    (r"i?yan", _with_linker_re, r"Med"),
    (r"i?y[ou]n", _with_linker_re, r"Dist"),
    (r"nito", _with_linker_re, r"Gen.Prox"),
    (r"ni?yan", _with_linker_re, r"Gen.Med"),
    (r"n(iyo|oo|u)n", _with_linker_re, r"Gen.Dist"),
    (r"dito", _with_linker_re, r"Obl.Prox"),
    (r"di?yan", _with_linker_re, r"Obl.Med"),
    (r"d(oo|u)n", _with_linker_re, r"Obl.Dist"),
    (r"ang", _standalone_re, r"Nom"),
    (r"ng", _standalone_re, r"Gen"),
    (r"sa", _standalone_re, r"Obl"),
    (r"si", _standalone_re, r"Nom.Pr"),
    (r"ni", _standalone_re, r"Gen.Pr"),
    (r"kay", _standalone_re, r"Obl.Pr"),
    (r"sina", _standalone_re, r"Nom.Pr.Pl"),
    (r"nina", _standalone_re, r"Gen.Pr.Pl"),
    (r"ki[nl]a", _standalone_re, r"Obl.Pr.Pl"),
    (r"mga", _standalone_re, r"Pl"),
    (r"kung", _standalone_re, r"if"),
    # PV Forms
    (re.compile(r"na-([^(\s]+)-\(in\)"), None, r"Nvol.Inch-\1-Pv"),
    (re.compile(r"ma-([^(\s]+)-\(in\)"), None, r"Nvol-\1-Pv"),
    (re.compile(r"<in>-([^(\s]+)-\(in\)"), None, r"<Inch>-\1-Pv"),
    # Other Voices
    (r"i-", _prefix_re, r"Cv-"),
    (r"ma[gN]-", _prefix_re, r"Av-"),
    (r"na[gN]-", _prefix_re, r"Av.Inch-"),
    (re.compile(r"<in>-"), None, r"<Inch>-"),
    (re.compile(r"<um>-"), None, r"<Av.Inch>-"),
    (r"RED-", _prefix_re, r"Ncompl-"),
    (r"-an", _suffix_re, r"-Lv"),
]

glosses = []
for expr, template, repl in _glosses:
    try:
        regexp = re.compile(template.format(expr))
    except AttributeError:
        regexp = expr
    glosses.append((regexp, repl))
