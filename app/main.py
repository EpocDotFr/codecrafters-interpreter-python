from app.lexer import Lexer
import argparse


def main() -> None:
    arg_parser = argparse.ArgumentParser()

    command_arg_parser = arg_parser.add_subparsers(dest='command', required=True)

    tokenize_arg_parser = command_arg_parser.add_parser('tokenize')
    tokenize_arg_parser.add_argument('filename')

    args = arg_parser.parse_args()

    if args.command == 'tokenize':
        with open(args.filename, 'rb') as f:
            lexer = Lexer(f, True)
            lexer.tokenize()

        if lexer.has_errors:
            exit(65)


if __name__ == '__main__':
    main()
