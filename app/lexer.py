from app.custom_types import Token, TokenType
from app.exceptions import LexicalError
from typing import List, TextIO
from sys import stderr, stdout
from io import StringIO


class Lexer:
    f: TextIO
    debug: bool

    tokens: List[Token]
    has_errors: bool

    def __init__(self, f: TextIO, debug: bool = False):
        self.f = f
        self.debug = debug

        self.tokens = []
        self.has_errors = False

    def tokenize(self):
        for line_number, line in enumerate(self.f):
            line_number += 1

            with StringIO(line) as l:
                while True:
                    c = l.read(1)

                    if not c:
                        break

                    try:
                        if c == '(':
                            token = Token(
                                TokenType.LEFT_PAREN,
                                c
                            )
                        elif c == ')':
                            token = Token(
                                TokenType.RIGHT_PAREN,
                                c
                            )
                        elif c == '{':
                            token = Token(
                                TokenType.LEFT_BRACE,
                                c
                            )
                        elif c == '}':
                            token = Token(
                                TokenType.RIGHT_BRACE,
                                c
                            )
                        elif c == ',':
                            token = Token(
                                TokenType.COMMA,
                                c
                            )
                        elif c == '.':
                            token = Token(
                                TokenType.DOT,
                                c
                            )
                        elif c == '-':
                            token = Token(
                                TokenType.MINUS,
                                c
                            )
                        elif c == '+':
                            token = Token(
                                TokenType.PLUS,
                                c
                            )
                        elif c == ';':
                            token = Token(
                                TokenType.SEMICOLON,
                                c
                            )
                        elif c == '/':
                            token = Token(
                                TokenType.SLASH,
                                c
                            )
                        elif c == '*':
                            token = Token(
                                TokenType.STAR,
                                c
                            )
                        else:
                            raise LexicalError(f'Unexpected character: {c}')

                        self.print(token)

                        self.tokens.append(token)
                    except LexicalError as e:
                        self.has_errors = True

                        self.print(f'[line {line_number}] Error: {e}', error=True)

        eof_token = Token(
            TokenType.EOF
        )

        self.print(eof_token)

        self.tokens.append(eof_token)

    def print(self, message: str, error: bool = False) -> None:
        if not self.debug:
            return

        print(message, file=stderr if error else stdout)
