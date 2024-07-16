class LexicalError(Exception):
    line: int

    def __init__(self, line: int, *args, **kwargs):
        self.line = line

        super().__init__(*args, *kwargs)
