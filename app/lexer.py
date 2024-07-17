from app.custom_types import Token, TokenType
from app.exceptions import LexicalError
from string import whitespace, digits
from typing import List, BinaryIO
from sys import stderr, stdout
from io import SEEK_CUR

whitespace_bytes = whitespace.encode()
digits_bytes = digits.encode()


class Lexer:
    f: BinaryIO
    debug: bool

    tokens: List[Token]
    has_errors: bool

    def __init__(self, f: BinaryIO, debug: bool = False):
        self.f = f
        self.debug = debug

        self.tokens = []
        self.has_errors = False

    def read_until(self, stop: bytes) -> bytes:
        value = b''
        end = False

        while True:
            c = self.f.read(1)

            if not c:
                break

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

            if c in whitespace_bytes:
                if c == b'\n':
                    line_number += 1

                continue

            lexeme = c
            literal = None

            try:
                if c == b'(':
                    type_ = TokenType.LEFT_PAREN
                elif c == b')':
                    type_ = TokenType.RIGHT_PAREN
                elif c == b'{':
                    type_ = TokenType.LEFT_BRACE
                elif c == b'}':
                    type_ = TokenType.RIGHT_BRACE
                elif c == b',':
                    type_ = TokenType.COMMA
                elif c == b'.':
                    type_ = TokenType.DOT
                elif c == b'-':
                    type_ = TokenType.MINUS
                elif c == b'+':
                    type_ = TokenType.PLUS
                elif c == b';':
                    type_ = TokenType.SEMICOLON
                elif c == b'/':
                    next_c = self.f.read(1)

                    if next_c == b'/':
                        try:
                            self.read_until(b'\n')

                            line_number += 1

                            continue
                        except EOFError:
                            break

                    type_ = TokenType.SLASH

                    if next_c:
                        self.f.seek(-1, SEEK_CUR)
                elif c == b'*':
                    type_ = TokenType.STAR
                elif c == b'=':
                    next_c = self.f.read(1)

                    if next_c == b'=':
                        type_ = TokenType.EQUAL_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.EQUAL

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == b'!':
                    next_c = self.f.read(1)

                    if next_c == b'=':
                        type_ = TokenType.BANG_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.BANG

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == b'<':
                    next_c = self.f.read(1)

                    if next_c == b'=':
                        type_ = TokenType.LESS_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.LESS

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == b'>':
                    next_c = self.f.read(1)

                    if next_c == b'=':
                        type_ = TokenType.GREATER_EQUAL

                        lexeme += next_c
                    else:
                        type_ = TokenType.GREATER

                        if next_c:
                            self.f.seek(-1, SEEK_CUR)
                elif c == b'"':
                    type_ = TokenType.STRING

                    try:
                        literal = self.read_until(b'"')

                        lexeme += literal + b'"'

                        literal = literal.decode()
                    except EOFError:
                        raise LexicalError('Unterminated string.') from None
                elif c in digits_bytes:
                    type_ = TokenType.NUMBER

                    while True:
                        next_c = self.f.read(1)

                        if not next_c:
                            break

                        if next_c not in digits_bytes + b'.':
                            self.f.seek(-1, SEEK_CUR)

                            break

                        if next_c == b'.' and b'.' in lexeme:
                            break

                        lexeme += next_c

                    literal = float(lexeme)
                else:
                    raise LexicalError(f'Unexpected character: {c.decode()}')

                self.add_token(type_, lexeme.decode(), literal)
            except LexicalError as e:
                self.has_errors = True

                self.print(f'[line {line_number}] Error: {e}', error=True)

        self.add_token(TokenType.EOF)

    def add_token(self, *args, **kwargs) -> None:
        token = Token(*args, **kwargs)

        self.print(str(token))

        self.tokens.append(token)

    def print(self, message: str, error: bool = False) -> None:
        if not self.debug:
            return

        print(message, file=stderr if error else stdout)
