import sys


def panic(message):
    print(f'{sys.argv[0]}: {message}', file=sys.stderr)
    sys.exit(1)


def log(message):
    # TODO: add verbosity setting
    print(message)
