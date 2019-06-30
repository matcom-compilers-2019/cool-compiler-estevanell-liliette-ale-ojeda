import ply.lex as lex

TOKEN = lex.TOKEN


class Lexer(object):
    def __init__(self):
        self.lexer = None
        self.tokens = ()
        self.line_start = 0
        self.reserved = {}

    @property
    def _tokens(self):
        return (
            # Identifiers
            "ID", "TYPE",
            # Primitive Types
            "INTEGER", "STRING",  # "BOOLEAN"
            # Literals
            "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", "COMMA", "DOT", "SEMICOLON", "AT",
            # Operators
            "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQ", "LT", "LTEQ", "ASSIGN", "INT_COMP",
            # Special Operators
            "ARROW",
            # Boolean values
            "TRUE", "FALSE", "BOOLEAN", "SELF"
            # Keywords
            # "CASE", "CLASS", "ELSE", "ESAC", "FI", "IF", "IN", "INHERITS", "ISVOID", "LET",
            # "LOOP", "NEW", "NOT", "OF", "POOL", "THEN", "WHILE", "TRUE", "FALSE"
        )

    @property
    def _reserved(self):
        # TODO AQUI SOLO ESTAN LAS KEYWORDS!!!
        return {
            "case": "CASE",
            "class": "CLASS",
            "else": "ELSE",
            "esac": "ESAC",
            "fi": "FI",
            "if": "IF",
            "in": "IN",
            "inherits": "INHERITS",
            "isvoid": "ISVOID",
            "let": "LET",
            "loop": "LOOP",
            "new": "NEW",
            "not": "NOT",
            "of": "OF",
            "pool": "POOL",
            "then": "THEN",
            "while": "WHILE"
            # "true": "TRUE",
            # "false": "FALSE"
        }

    @property
    def states(self):
        return (
            ("STRING", "exclusive"),
            ("COMMENT", "exclusive")
        )

    # TOKEN KEYWORDS
    # t_CASE = r'(C|c)(A|a)(S|s)(E|e)'  # case
    # t_CLASS = r'(C|c)(L|l)(A|a)(S|s)(S|s)'  # class
    # t_ELSE = r'(E|e)|(L|l)(S|s)(E|e)'  # else
    # t_ESAC = r'(E|e)(S|s)(A|a)(C|c)'  # esac
    # t_FI = r'(F|f)(I|i)'  # fi
    # t_IF = r'(I|i)(F|f)'  # if
    # t_IN = r'(I|i)(N|n)'  # in
    # t_INHERITS = r'(I|i)(N|n)(H|h)(E|e)(R|r)(I|i)(T|t)(S|s)'  # inherits
    # t_ISVOID = r'(I|i)(S|s)(V|v)(O|o)(I|i)(D|d)'  # isvoid
    # t_LET = r'(L|l)(E|e)(T|t)'  # let
    # t_LOOP = r'(L|l)(O|o)(O|o)(P|p)'  # loop
    # t_NEW = r'(N|n)(E|e)(W|w)'  # new
    # t_NOT = r'(N|n)(O|o)(T|t)'  # not
    # t_OF = r'(O|o)(F|f)'  # of
    # t_POOL = r'(P|p)(O|o)(O|o)(L|l)'  # pool
    # t_THEN = r'(T|t)(H|h)(E|e)(N|n)'  # then
    # t_WHILE = r'(W|w)(H|h)(I|i)(L|l)(E|e)'  # while

    # TOKEN SYMBOLS
    t_LPAREN = r'\('                      # (
    t_RPAREN = r'\)'                      # )
    t_LBRACE = r'\{'                      # {
    t_RBRACE = r'\}'                      # }
    t_COLON = r'\:'                       # :
    t_COMMA = r'\,'                       # ,
    t_DOT = r'\.'                         # .
    t_SEMICOLON = r'\;'                   # ;
    t_AT = r'\@'                          # @
    t_MULTIPLY = r'\*'                    # *
    t_DIVIDE = r'\/'                      # /
    t_PLUS = r'\+'                        # +
    t_MINUS = r'\-'                       # -
    t_INT_COMP = r'~'                     # ~
    t_LT = r'\<'                          # <
    t_EQ = r'\='                          # =
    t_LTEQ = r'\<\='                      # <=
    t_ASSIGN = r'\<\-'                    # <-
    t_ARROW = r'\=\>'                     # =>

    # region INITIAL STATE rules.

    t_ignore_SINGLE_LINE_COMMENT = r'\-\-[^\n]*'

    digit = r'([0-9])'
    nondigit = r'([_A-Za-z])'
    identifier = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

    # @TOKEN(r'(true | false)')
    # def t_BOOLEAN(self, token):
    #     token.value = True if token.value == 'true' else False
    #     return token

    @TOKEN(r't(R|r)(U|u)(E|e)')
    def t_TRUE(self, token):
        token.value = 'TRUE'
        return token

    @TOKEN(r'f(A|a)(L|l)(S|s)(E|e)')
    def t_FALSE(self, token):
        token.value = 'FALSE'
        return token

    @TOKEN(r'\d+')
    def t_INTEGER(self, token):
        # token.lexpos = (token.lexpos - self.lexer.line_start)  # OJO
        token.value = int(token.value)
        return token

    @TOKEN(r'[A-Z][a-zA-Z_0-9]*')
    def t_TYPE(self, token):
        # token.lexpos = (token.lexpos - self.lexer.line_start)  # OJO
        # Check for reserved words
        token.type = self._reserved.get(token.value.lower(), 'TYPE')  # OJO
        return token

    @TOKEN(r'[a-z_][a-zA-Z_0-9]*')
    def t_ID(self, token):
        # token.lexpos = (token.lexpos - self.lexer.line_start)  # OJO
        # Check for reserved words
        token.type = self._reserved.get(token.value.lower(), 'ID')  # OJO
        return token

    @TOKEN(r'\n+')
    def t_newline(self, token):
        token.lexer.lineno += len(token.value)

    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # Ignore Whitespace Character Rule
    t_ignore = ' \t\r\f'
    # endregion

    # region STRING STATE rules.
    @TOKEN(r'\"')
    def t_start_string(self, token):
        token.lexer.push_state("STRING")
        token.lexer.string_backslashed = False
        token.lexer.stringbuf = ""

    @TOKEN(r'\n')
    def t_STRING_newline(self, token):
        token.lexer.lineno += 1
        if not token.lexer.string_backslashed:
            print("String newline not escaped")
            token.lexer.skip(1)
        else:
            token.lexer.string_backslashed = False

    @TOKEN(r'\"')
    def t_STRING_end(self, token):
        if not token.lexer.string_backslashed:
            token.lexer.pop_state()
            token.value = token.lexer.stringbuf
            token.type = "STRING"
            return token
        else:
            token.lexer.stringbuf += '"'
            token.lexer.string_backslashed = False

    @TOKEN(r'[^\n]')
    def t_STRING_anything(self, token):
        if token.lexer.string_backslashed:
            if token.value == 'b':
                token.lexer.stringbuf += '\b'
            elif token.value == 't':
                token.lexer.stringbuf += '\t'
            elif token.value == 'n':
                token.lexer.stringbuf += '\n'
            elif token.value == 'f':
                token.lexer.stringbuf += '\f'
            elif token.value == '\\':
                token.lexer.stringbuf += '\\'
            else:
                token.lexer.stringbuf += token.value
            token.lexer.string_backslashed = False
        else:
            if token.value != '\\':
                token.lexer.stringbuf += token.value
            else:
                token.lexer.string_backslashed = True

    t_STRING_ignore = ''

    def t_STRING_error(self, token):
        print("Illegal character! Line: {0}, character: {1}".format(
            token.lineno, token.value[0]))
        token.lexer.skip(1)
    # endregion

    # region COMMENT STATE rules.

    @TOKEN(r'\(\*')
    def t_start_comment(self, token):
        token.lexer.push_state("COMMENT")
        token.lexer.comment_count = 0

    @TOKEN(r"\(\*")
    def t_COMMENT_startanother(self, t):
        t.lexer.comment_count += 1

    @TOKEN(r"\*\)")
    def t_COMMENT_end(self, token):
        if token.lexer.comment_count == 0:
            token.lexer.pop_state()
        else:
            token.lexer.comment_count -= 1

    # @TOKEN("[\n]")
    # def t_COMMENT_newline(self, token):
    #     token.lexer.lineno += 1
    #     self.lexer.line_start = token.lexpos

    # COMMENT ignored characters
    t_COMMENT_ignore = ''

    # COMMENT error handler
    def t_COMMENT_error(self, token):
        token.lexer.skip(1)

    def t_error(self, token):
        """
        Error Handling and Reporting Rule.
        """
        print("Illegal character! Line: {0}, character: {1}".format(
            token.lineno, token.value[0]))
        token.lexer.skip(1)
    # endregion

    def reset(self):
        self.build()

    def build(self, **kwargs):
        self.reserved = self._reserved.keys()
        self.tokens = self._tokens + tuple(self._reserved.values())
        self.lexer = lex.lex(module=self, **kwargs)

    def __call__(self, data):
        self.reset()
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            yield tok

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

def create_lexer(**kwargs):
    a_lexer = CoolLeX()
    a_lexer.build(**kwargs)
    return a_lexer
