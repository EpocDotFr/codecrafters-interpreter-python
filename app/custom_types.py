from typing import Optional, Union
from dataclasses import dataclass
import enum


class TokenType(enum.StrEnum):
    # Single-character tokens
    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()
    LEFT_BRACE = enum.auto()
    RIGHT_BRACE = enum.auto()
    COMMA = enum.auto()
    DOT = enum.auto()
    MINUS = enum.auto()
    PLUS = enum.auto()
    SEMICOLON = enum.auto()
    SLASH = enum.auto()
    STAR = enum.auto()

    # One or two character tokens
    BANG = enum.auto()
    BANG_EQUAL = enum.auto()
    EQUAL = enum.auto()
    EQUAL_EQUAL = enum.auto()
    GREATER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LESS = enum.auto()
    LESS_EQUAL = enum.auto()

    # Literals
    IDENTIFIER = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()

    # Keywords
    AND = enum.auto()
    CLASS = enum.auto()
    ELSE = enum.auto()
    FALSE = enum.auto()
    FUN = enum.auto()
    FOR = enum.auto()
    IF = enum.auto()
    NIL = enum.auto()
    OR = enum.auto()
    PRINT = enum.auto()
    RETURN = enum.auto()
    SUPER = enum.auto()
    THIS = enum.auto()
    TRUE = enum.auto()
    VAR = enum.auto()
    WHILE = enum.auto()

    EOF = enum.auto()


@dataclass
class Token:
    type_: TokenType
    lexeme: str = ''
    literal: Optional[Union[str, int, float, bool]] = None

    def __str__(self) -> str:
        return '{} {} {}'.format(
            self.type_.name,
            self.lexeme,
            'null' if self.literal is None else self.literal
        )
