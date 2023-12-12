import sys

def panic(message):
    print(f'{sys.argv[0]}: {message}', file=sys.stderr)
    sys.exit(1)
