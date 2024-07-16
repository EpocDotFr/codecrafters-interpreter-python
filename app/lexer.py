from app.custom_types import Token, TokenType
from typing import List, TextIO


class Lexer:
    f: TextIO
    tokens: List[Token]

    def __init__(self, f: TextIO):
        self.f = f
        self.tokens = []

    def tokenize(self):
        while True:
            c = self.f.read(1)

            if not c:
                break

            if c == '(':
                self.tokens.append(Token(
                    TokenType.LEFT_PAREN,
                    c
                ))
            elif c == ')':
                self.tokens.append(Token(
                    TokenType.RIGHT_PAREN,
                    c
                ))

        self.tokens.append(Token(
            TokenType.EOF
        ))

    def __str__(self) -> str:
        return '\n'.join([
            str(t) for t in self.tokens
        ])
