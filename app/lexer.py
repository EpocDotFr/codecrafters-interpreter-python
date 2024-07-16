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
            elif c == '{':
                self.tokens.append(Token(
                    TokenType.LEFT_BRACE,
                    c
                ))
            elif c == '}':
                self.tokens.append(Token(
                    TokenType.RIGHT_BRACE,
                    c
                ))
            elif c == ',':
                self.tokens.append(Token(
                    TokenType.COMMA,
                    c
                ))
            elif c == '.':
                self.tokens.append(Token(
                    TokenType.DOT,
                    c
                ))
            elif c == '-':
                self.tokens.append(Token(
                    TokenType.MINUS,
                    c
                ))
            elif c == '+':
                self.tokens.append(Token(
                    TokenType.PLUS,
                    c
                ))
            elif c == ';':
                self.tokens.append(Token(
                    TokenType.SEMICOLON,
                    c
                ))

            elif c == '/':
                self.tokens.append(Token(
                    TokenType.SLASH,
                    c
                ))
            elif c == '*':
                self.tokens.append(Token(
                    TokenType.STAR,
                    c
                ))

        self.tokens.append(Token(
            TokenType.EOF
        ))

    def __str__(self) -> str:
        return '\n'.join([
            str(t) for t in self.tokens
        ])
