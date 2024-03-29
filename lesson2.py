
import re

class GDL02_main:
    def __init__(self, vlst):
        self.vlst = vlst

class GDL02_stmt:
    def __init__(self, s, v):
        self.s = s
        self.v = v

class GDL02_stmt_value:
    def __init__(self, v):
        self.v = v

class GDL02_values_or:
    def __init__(self, slst):
        self.slst = slst

class GDL02_string_or:
    def __init__(self, slst):
        self.slst = slst

class GDL02_series:
    def __init__(self, vlst):
        self.vlst = vlst

class GDL02_jiap:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

class GDL02_litname:
    def __init__(self, s):
        self.s = s

class GDL02_litstring:
    def __init__(self, s):
        self.s = s

class GDL02_value1:
    def __init__(self, v):
        self.v = v

class GDL02_enclosed:
    def __init__(self, v):
        self.v = v

class GDL02_itemd:
    def __init__(self, v):
        self.v = v

class GDL02_value:
    def __init__(self, v):
        self.v = v

class Parser00:
    def __init__(self, txt):
        self.txt = txt
        self.pos = 0
    def handle_NAME(self):
        partn = '[A-Za-z_][A-Za-z0-9_]*'
        partn_compiled = re.compile(partn)
        m = partn_compiled.match(self.txt, self.pos)
        if m:
            content = m.group()
            self.pos = m.end()
            return content
        return None
    def handle_NUMBER(self):
        partn = r'0|[1-9]\d*'
        partn_compiled = re.compile(partn)
        m = partn_compiled.match(self.txt, self.pos)
        if m:
            content = m.group()
            self.pos = m.end()
            return content
        return None
    def handle_STRING(self):
        partn = r"'[^'\\]*(?:\\.[^'\\]*)*'"
        partn_compiled = re.compile(partn)
        m = partn_compiled.match(self.txt, self.pos)
        if m:
            content = m.group()
            self.pos = m.end()
            return content
        return None
    def handle_NEWLINE(self):
        partn = r"\n[\n \t]*"
        partn_compiled = re.compile(partn)
        m = partn_compiled.match(self.txt, self.pos)
        if m:
            content = m.group()
            self.pos = m.end()
            return content
        return None
    def handle_str(self, s):
        if self.txt[self.pos:].startswith(s):
            self.pos += len(s)
            return s
    def restorepos(self, pos):
        self.pos = pos
    def skipspace(self):
        while self.pos < len(self.txt) and self.txt[self.pos] in ' \t':
            self.pos += 1

class GDL02_Parser(Parser00):
    def handle_main(self):
        vlst = []
        savpos = self.pos
        while True:
            v = self.handle_stmt()
            if not v:
                break
            self.skipspace()
            if not self.handle_NEWLINE():
                break
            vlst.append(v)
            savpos = self.pos
            self.skipspace()
        self.restorepos(savpos)
        if not vlst:
            return None
        return GDL02_main(vlst)

    def handle_stmt(self):
        savpos = self.pos
        s = self.handle_NAME()
        if not s:
            return None
        self.skipspace()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspace()
        v = self.handle_stmt_value()
        if not v:
            return self.restorepos(savpos)
        return GDL02_stmt(s, v)

    def handle_stmt_value(self):
        v = self.handle_values_or()
        if not v:
            v = self.handle_string_or()
        if not v:
            v = self.handle_jiap()
        if not v:
            v = self.handle_series()
        if not v:
            return None
        return GDL02_stmt_value(v)

    def handle_values_or(self):
        savpos = self.pos
        slst = []
        s = self.handle_NAME()
        if not s:
            return None
        slst.append(s)
        while True:
            self.skipspace()
            if not self.handle_str('|'):
                break
            self.skipspace()
            s = self.handle_NAME()
            if not s:
                break
            slst.append(s)
            savpos = self.pos
        self.restorepos(savpos)
        if len(slst) < 2:
            return None
        return GDL02_values_or(slst)

    def handle_string_or(self):
        savpos = self.pos
        slst = []
        s = self.handle_STRING()
        if not s:
            return None
        slst.append(s)
        while True:
            self.skipspace()
            if not self.handle_str('|'):
                break
            self.skipspace()
            s = self.handle_STRING()
            if not s:
                break
            slst.append(s)
            savpos = self.pos
        self.restorepos(savpos)
        if len(slst) < 2:
            return None
        return GDL02_string_or(slst)

    def handle_series(self):
        savpos = self.pos
        vlst = []
        while True:
            v = self.handle_value()
            if not v:
                break
            vlst.append(v)
            savpos = self.pos
            self.skipspace()
        self.restorepos(savpos)
        if not vlst:
            return None
        return GDL02_series(vlst)

    def handle_jiap(self):
        savpos = self.pos
        s1 = self.handle_NAME()
        if not s1:
            return None
        self.skipspace()
        if not self.handle_str('^+'):
            return self.restorepos(savpos)
        self.skipspace()
        s2 = self.handle_STRING()
        if not s2:
            return restorepos(savpos)
        return GDL02_jiap(s1, s2)

    def handle_litname(self):
        s = self.handle_NAME()
        if not s:
            return None
        return GDL02_litname(s)

    def handle_litstring(self):
        s = self.handle_STRING()
        if not s:
            return None
        return GDL02_litstring(s)

    def handle_value1(self):
        v = self.handle_litname()
        if not v:
            v = self.handle_litstring()
        if not v:
            v = self.handle_enclosed()
        if not v:
            return None
        return GDL02_value1(v)

    def handle_enclosed(self):
        savpos = self.pos
        if not self.handle_str('('):
            return None
        self.skipspace()
        v = self.handle_stmt_value()
        if not v:
            return self.restorepos(savpos)
        self.skipspace()
        if not self.handle_str(')'):
            return self.restorepos(savpos)
        return GDL02_enclosed(v)

    def handle_value(self):
        v = self.handle_itemd()
        if not v:
            v = self.handle_value1()
        if not v:
            return None
        return GDL02_value(v)

    def handle_itemd(self):
        savpos = self.pos
        v = self.handle_value1()
        if not v:
            return None
        self.skipspace()
        if not self.handle_str('*'):
            return self.restorepos(savpos)
        return GDL02_itemd(v)

syntax = '''main = (stmt NEWLINE)*
    stmt = NAME '=' stmt_value
    stmt_value = values_or | string_or | jiap | series
        values_or = NAME ^+ '|'
        string_or = STRING ^+ '|'
        series = value*
        jiap = NAME '^+' STRING

    litname = NAME
    litstring = STRING
    value1 = litname | litstring | enclosed
        enclosed = '(' stmt_value ')'
    value = itemd | value1
        itemd = value1 '*'
'''


import unittest
class Test(unittest.TestCase):
    def testhandle_NAME(self):
        the = Parser00("'hello world' is ok")
        word1 = the.handle_STRING()
        self.assertEqual(the.pos, 13)
        self.assertEqual(word1, "'hello world'")
    def testParse(self):
        the = GDL02_Parser(syntax)
        mod = the.handle_main()
        self.assertEqual(mod.vlst[-1].s, 'itemd')
    def testParse2(self):
        syntax = '''main = stmt*
            stmt = declare_with_value | declare | assign | funccall
            datatype = 'int' | 'long'
            declare = datatype NAME
            declare_with_value = datatype NAME '=' value
            value0 = NUMBER | NAME
            binvalue = value0 ('+' | '-') value0
            value = binvalue | value0
            assign = NAME '=' value
            funccall = NAME '(' value ')'
        '''
        the = GDL02_Parser(syntax)
        mod = the.handle_main()
        self.assertEqual(mod.vlst[-1].s, 'funccall')

