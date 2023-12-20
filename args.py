import argparse, sys, re, os
from panic import panic


def validate_args(args):
    if not args.command == 'new-project':
        return

    if sum(not c.isalnum() and c != '_' for c in os.path.basename(args.path)):
        panic(
            'project names may only contain alphanumeric characters and underscores'
        )

    pattern = re.compile(
        r"""^(git|(((https|git):\/\/)|git@)[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+[.]git)$"""
    )
    if not pattern.fullmatch(args.git):
        panic('`--git` valid options:\n'
              '    git\n'
              '    git@<remote>:<repository>.git\n'
              '    git://<remote>/<repository>.git\n'
              '    https://<remote>/repository>.git')
    return


def parse_args():
    parser = argparse.ArgumentParser(prog='generate-c++',
                                     description='Generates a C++ project.')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    new_project = subparsers.add_parser('new-project',
                                        help='Creates a new project.')
    new_project.add_argument(
        'path',
        help=
        'A path to the project directory.',
    )
    new_project.add_argument('--author',
                             required=True,
                             help='The entity who owns the copyright.')
    new_project.add_argument(
        '--git',
        default='git',
        help=
        "Version control system to use (default='git'). Also recognises Git remotes (e.g. 'git@', 'git://')."
    )
    new_project.add_argument('--build-system',
                             choices=['cmake'],
                             default='cmake',
                             help='Build system to use (default=cmake).')
    new_project.add_argument('--package-manager',
                             choices=['vcpkg'],
                             default='vcpkg',
                             help='Package manager to use (default=vcpkg).')
    new_project.add_argument('--editor',
                             choices=['none', 'vscode'],
                             default='vscode',
                             help='Editor to set up for.')
    new_project.add_argument(
        '-prefix',
        type=str,
        default='/usr',
        help='Path to compiler root directory. (default=\'/usr\')')
    new_project.add_argument(
        '-target',
        type=str,
        default='',
        help='The triple to target. Defaults to system default.')
    new_project.add_argument(
        '-std',
        choices=[11, 14, 17, 20, 23, 26],
        default=20,
        help='C++ standard to compile against (default=20).')
    new_project.add_argument('-fno-exceptions',
                           action='store_true',
                           help='Disables exceptions (default=false).')
    new_project.add_argument('-fno-rtti',
                           action='store_true',
                           help='Disables RTTI (default=false).')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    validate_args(args)
    return args
