Abbreviation parser for MoinMoin 1.9
====================================

This parser is based on [abbr.py][1] written by Oliver Siemoneit and
Johannes Berg for [MoinMoin][2] 1.6.

The parser is distributed under terms of GNU GPL license as the
original version.  See COPYING for details.

The main difference between original parser and this one is that the
latter uses a bit different syntax.  Here is the description of each
difference and justification for it:


Differences from abbr.py 1.0
----------------------------

### Different delimiter

This parser uses question marks:

    ?WAI?

instead of carets:

    ^WAI^

The reason for this change is that carets are also used for making
superscript text, so normally '^WAI^' expanded to HTML code
'<sup>WAI</sup>'.

On the other hand, question marks don't conflict with other of
MoinMoin markup elements.

And after all question marks are easier for typing than carets :-)


### Different syntax for page specification

This parser uses the following syntax for page specification:

    ?WAI|page=OtherPage?

instead of:

    ^WAI|OtherPage^

Because it unifies way of specifying of attributes and it looks
clearer.


### Use "lang" instead of "language"

This parser uses "lang"

    ?WAI|lang=en?

instead of "language":

    ?WAI|language=en?

Because it is shorter.


### Other notable changes

 - Order of attributes ("page" and "lang") doesn't matter.
 - Value of "lang" attribute for '<abbr>' is wrapped into quotes
   according to [recommendations of W3C][3].
   

Installation
------------

Please see [official instructions][4] for installation of parsers.


[1]: http://moinmo.in/ParserMarket/Abbreviation
[2]: http://moinmo.in/
[3]: http://www.w3.org/TR/REC-html40/intro/sgmltut.html#h-3.2.2
[4]: http://moinmo.in/ParserMarket/InstallingParsers
