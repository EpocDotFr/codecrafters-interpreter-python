from io import StringIO


class Lexer:
    f: StringIO

    def __init__(self, f: StringIO):
        self.f = f

    def tokenize(self):
        pass

    def __str__(self) -> str:
        return 'EOF  null'
