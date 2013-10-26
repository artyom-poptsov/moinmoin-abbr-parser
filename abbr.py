# -*- coding: utf-8 -*-
"""
    MoinMoin - Abbreviation Parser

    This extension of the standard Moin wiki parser is mainly written for
    AccessibleMoin since it is one criteria for accessible sites, that abbrevations
    or acronyms should be marked with the <abbr title=.. lang=..> markup.

    Since the <acronym> tag won't be probably part of future (X)HTML standards and
    since Moin patches the missing <abbr> support of Internet Explorer, only <abbr>
    is used in AccessibleMoin to mark acronyms and abbreviations.

    Syntax:
        ^WAI^
        Marks the word WAI as an abbreviation and tries to retrieve the explanation from
        the standard abbreviation definitions page "AbbrDict" or the page specified
        with "#pragma abbreviation-definitions PageName" in the header of the page.

        ^WAI|OtherPage^
        Marks the word WAI as an abbreviation and tries to retrieve the explanation from
        the specified page "OtherPage". You can use this to overwrite the default settings
        like "AbbrDict" or "#pragma abbreviation-definitions PageName"        

        ^WAI:Web Accessibility Initiative^
        Marks the word WAI as an abbreviation and uses the given explanation.

        ^WAI|language=de^
        ^WAI|OtherPage|language=de^
        ^WAI:Web Accessibility Initiative|language=de^
        Marks the word WAI as an foreign language abbreviation (compared to the language
        default of the wiki and the page)

    Please note:
    * The explanation pages for abbreviations must be in WikiDict format, like
      " WAI:: Web Accessibility Initiative" (don't forget the space at the beginning!)
    * If the abbreviation is in an other language than the default page language, please
      mark this with "|language=LanguageShortcut"
    * Don't forget the caching mechanism of Moin: To get a page updated with a changed
      abbreviation explanation (e.g. from AbbrDict) you have to delete the cache of the page
      or reedit the page again.
    * For correct display of abbreviations also in IE please put this line in your screen.css
      "abbr[title] {border-bottom: 1px dotted; cursor: help}"

    Abbreviation Parser heavily based on AcronymParser by Johannes Berg

    MoinMoin - Abbreviation Parser
    @copyright: 2007 by Oliver Siemoneit
    @copyright: 2013 by Artyom Poptsov <poptsov.artyom@gmail.com>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.parser import text_moin_wiki as wiki
from MoinMoin.datastruct.backends.wiki_dicts import WikiDict
from MoinMoin import wikiutil
import re

class Parser(wiki.Parser):
    scan_rules = wiki.Parser.scan_rules
    scan_rules += ur'|(?P<abbr>\?[^\?]*\?)'
    scan_re = re.compile(scan_rules, re.UNICODE|re.VERBOSE)

    def __init__(self, raw, request, **kw):
        wiki.Parser.__init__(self, raw, request, **kw)
        self.formatter = request.formatter
        self.request = request
        self.args = kw.get('format_args', '')

    def format_abbr(self, lang, key, exp):
        try:
            html = '<abbr title="%(exp)s" %(lang)s>%(word)s</abbr>' % {
                'exp': wikiutil.escape(exp),
                'lang': lang,
                'word': wikiutil.escape(key) }
            return self.request.formatter.rawHTML(html)
        except:
            return self.request.formatter.escapedText(key)

    def dicts(self, request):
        from MoinMoin.datastruct import WikiDicts
        return WikiDicts(request)

    def _abbr_repl(self, word, groups):
        # Get rid of markup elements
        word = word[1:-1].strip()

        key = word
        exp = ''
        tmp = word.split('|')

        lang = ''

        if len(tmp) >= 2:
            key = tmp[0]
            exp = tmp[1]

        # Check if "lang" attribute is set
        if (len(tmp) == 3) and (tmp[2].startswith('lang=')):
            lang = 'lang="%s"' % tmp[2].split("=", 1)[1]
 
        # Explanation is directly given?
        if exp:
            return self.format_abbr(lang, key, exp)

        # Locate definition in the standard dictionary
        d = self.request.dicts.get(u"AbbrDict", {})
        exp = d.get(key, {})
        if not exp:
            return self.request.formatter.escapedText(key)
        else:
            return self.format_abbr(lang, key, exp)

