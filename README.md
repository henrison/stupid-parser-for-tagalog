# stupid-parser-for-tagalog
A very basic morphological parser intended as an assistive tool for semi-automatically parsing large amounts of Tagolog sentential data

# Version history
**This script has been written only with the specific usage scenario intended by the original author in mind. You may find that using the script is not very intuitive or that the output is not correct. Comments and suggestions are welcome, but I cannot promise that I will be able to address them quickly.**

## 0.1
- Implemented basic morphological parsing for most of the easy cases
- Basic command prompt interface
- Does not yet handle nasal substitution in the general case (e.g.: `mangingisda` --> `maN-RED-isda`, `mamili` --> `maN-bili` or `maN-pili`)
- May not handle other cases as well

# How to use
**This script does _not_ perform automatic parsing of Tagalog morphology.**

This script is intended for users already familiar with Tagalog morphology.
It is a tool for semi-automating the potentially repetitive task of parsing medium-to-large sized collections of texts/sentences
The script requires that the user review/confirm all potential parses.

Requires Python 2.7.
Usage: `python parser.py <filename>`
