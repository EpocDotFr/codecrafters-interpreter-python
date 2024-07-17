from app.custom_types import Token, TokenType
from typing import List, Optional, Union
from app.exceptions import LexicalError
from io import BytesIO, SEEK_CUR
from sys import stderr, stdout
from string import whitespace


class Lexer:
    f: BytesIO
    debug: bool

    tokens: List[Token]
    has_errors: bool

    def __init__(self, f: BytesIO, debug: bool = False):
        self.f = f
        self.debug = debug

        self.tokens = []
        self.has_errors = False

    def read_until(self, stop: str) -> str:
        value = ''
        end = False

        while True:
            c = self.f.read(1)

            if not c:
                break

            c = c.decode()

            if c == stop:
                end = True

                break

            value += c

        if not end:
            raise EOFError()

        return value

    def tokenize(self) -> None:
        line_number = 1

        while True:
            c = self.f.read(1)

            if not c:
                break

            c = c.decode()

            if c in whitespace:
                if c == '\n':
                    line_number += 1

                continue

            lexeme = c
            literal = None

            try:
                if c == '(':
                    type_ = TokenType.LEFT_PAREN
                elif c == ')':
                    type_ = TokenType.RIGHT_PAREN
                elif c == '{':
                    type_ = TokenType.LEFT_BRACE
                elif c == '}':
                    type_ = TokenType.RIGHT_BRACE
                elif c == ',':
                    type_ = TokenType.COMMA
                elif c == '.':
                    type_ = TokenType.DOT
                elif c == '-':
                    type_ = TokenType.MINUS
                elif c == '+':
                    type_ = TokenType.PLUS
                elif c == ';':
                    type_ = TokenType.SEMICOLON
                elif c == '/':
                    next_c = self.f.read(1)

                    if next_c:
                        next_c = next_c.decode()

                    if next_c == '/':
                        self.read_until('\n')

                        continue

                    type_ = TokenType.SLASH

                    if next_c:
                        self.f.seek(-1, SEEK_CUR)
                elif c == '*':
                    type_ = TokenType.STAR
                elif c == '=':
                    next_c = self.f.read(1)

                    if next_c:
                        next_c = next_c.decode()

                    if next_c == '=':
                        type_ = TokenType.EQUAL_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.EQUAL

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == '!':
                    next_c = self.f.read(1)

                    if next_c:
                        next_c = next_c.decode()

                    if next_c == '=':
                        type_ = TokenType.BANG_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.BANG

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == '<':
                    next_c = self.f.read(1)

                    if next_c:
                        next_c = next_c.decode()

                    if next_c == '=':
                        type_ = TokenType.LESS_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.LESS

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == '>':
                    next_c = self.f.read(1)

                    if next_c:
                        next_c = next_c.decode()

                    if next_c == '=':
                        type_ = TokenType.GREATER_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.GREATER

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == '"':
                    type_ = TokenType.STRING

                    try:
                        literal = self.read_until('"')

                        lexeme += literal + '"'
                    except EOFError:
                        raise LexicalError('Unterminated string.') from None
                else:
                    raise LexicalError(f'Unexpected character: {c}')

                self.add_token(type_, lexeme, literal)
            except LexicalError as e:
                self.has_errors = True

                self.print(f'[line {line_number}] Error: {e}', error=True)

        self.add_token(TokenType.EOF)

    def add_token(self, type_: TokenType, lexeme: str = '', literal: Optional[Union[str, int, float, bool]] = None) -> None:
        token = Token(
            type_,
            lexeme,
            literal
        )

        self.print(token)

        self.tokens.append(token)

    def print(self, message: str, error: bool = False) -> None:
        if not self.debug:
            return

        print(message, file=stderr if error else stdout)
