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
            html = '<abbr title="%(exp)s" lang="%(lang)s">%(word)s</abbr>' % {
                'exp': wikiutil.escape(exp),
                'lang': lang,
                'word': wikiutil.escape(key) }
            return self.request.formatter.rawHTML(html)
        except:
            return self.request.formatter.escapedText(key)

    def get_value(self, attr, tokens):
        res = ''
        for t in tokens:
            if t.startswith(attr + '='):
                res = t.split('=', 1)[1]
                break
        return res

    def _abbr_repl(self, word, groups):
        # Get rid of markup elements
        word = word[1:-1].strip()

        abbr = ''
        expl = ''
        lang = ''
        tokens = word.split('|')
        abbr = tokens[0]

        # Check if explanation is already given
        tmp = abbr.split(':')
        if len(tmp) == 2:
            abbr = tmp[0]
            expl = tmp[1]

        # Check if "lang" attribute is set
        lang = self.get_value("lang", tokens)
 
        # Explanation is directly given?
        if expl:
            return self.format_abbr(lang, abbr, expl)

        page = self.get_value("page", tokens)
        if not page:
            # Locate definition in the standard dictionary
            page = u"AbbrDict"

        dictionary = self.request.dicts.get(page, {})
        expl = dictionary.get(abbr, {})
        if not expl:
            return self.request.formatter.escapedText(expl)
        else:
            return self.format_abbr(lang, abbr, expl)

