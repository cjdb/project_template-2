import argparse, sys, re, os
from utils import panic


def validate_git_remote(remote: str) -> bool:
    pattern = re.compile(
        r"""^(git|(((https|git):\/\/)|git@)[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+[.]git)$"""
    )
    if pattern.fullmatch(remote):
        return

    file = 'file://'
    if not (remote.startswith(file) and os.path.isdir(remote[len(file):])):
        panic('remote valid options:\n'
              '    git@<remote>:<repository>.git\n'
              '    git://<remote>/<repository>.git\n'
              '    https://<remote>/repository>.git\n'
              '    file:///path/to/remote')


def validate_args(args):
    if not args.command == 'new-project':
        return

    if sum(not c.isalnum() and c != '_' for c in os.path.basename(args.path)):
        panic(
            'project names may only contain alphanumeric characters and underscores'
        )

    if args.remote:
        validate_git_remote(args.remote)
    if args.package_manager_remote:
        validate_git_remote(args.package_manager_remote)
    return


def parse_args():
    parser = argparse.ArgumentParser(prog='generate-c++',
                                     description='Generates a C++ project.')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    new_project = subparsers.add_parser('new-project',
                                        help='Creates a new project.')
    new_project.add_argument(
        'path',
        help='A path to the project directory.',
    )
    new_project.add_argument('--author',
                             required=True,
                             help='The entity who owns the copyright.')
    new_project.add_argument(
        '--remote',
        default='',
        help=
        "Sets the default Git remote. Use 'file://' to indicate a file system-based remote."
    )
    new_project.add_argument('--package-manager',
                             choices=['none', 'vcpkg'],
                             default='vcpkg',
                             help='Package manager to use (default=vcpkg).')
    new_project.add_argument(
        '--package-manager-remote',
        default='',
        help=
        'Remote for package manager. Use `file://` to indicate the remote is a local repository.'
    )
    new_project.add_argument('--editor',
                             choices=['none', 'vscode'],
                             default='vscode',
                             help='Editor to set up for.')
    new_project.add_argument(
        '--toolchain-prefix',
        type=str,
        default='/usr',
        help='Path to compiler root directory. (default=\'/usr\')')
    new_project.add_argument(
        '-std',
        choices=[
            'c++11', 'c++14', 'c++17', 'c++20', 'c++23', 'c++26', 'gnu++11',
            'gnu++14', 'gnu++17', 'gnu++20', 'gnu++23', 'gnu++26'
        ],
        default='c++20',
        help='C++ standard to compile against (default=c++20).')
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
