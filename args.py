import argparse, sys, re
from panic import panic


def validate_args(args):
    if not args.command == 'new-project':
        return

    if sum(not c.isalnum() and c != '_' for c in args.name):
        panic(
            'project names may only contain alphanumeric characters and underscores'
        )

    if args.compiler == 'gcc':
        if args.target:
            panic('`-target` cannot be configured when using GCC.')
        if args.stdlib:
            panic('`-stdlib` cannot be configured when using GCC.')
        if args.rtlib:
            panic('`-rtlib` cannot be configured when using GCC.')
        if args.unwindlib:
            panic('`-unwindlib` cannot be configured when using GCC.')

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
        '--name',
        required=True,
        help=
        'A name for the project. Must follow the rules for C++ identifiers.',
    )
    new_project.add_argument('--root',
                             required=True,
                             help='Path to project root.')
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
    new_project_subparser = new_project.add_subparsers(
        help='Select a toolchain', required=True)
    toolchain = new_project_subparser.add_parser(
        'toolchain', help='Adds a toolchain to the project.')
    toolchain.add_argument('compiler',
                           choices=['clang', 'gcc'],
                           help='Compiler to use.')
    toolchain.add_argument(
        '-prefix',
        type=str,
        default='',
        help='Path to compiler root directory. (E.g. \'/usr/\')')
    toolchain.add_argument(
        '-target',
        type=str,
        default='',
        help='The triple to target (Clang only, default=clang default)')
    toolchain.add_argument(
        '-std',
        choices=[11, 14, 17, 20, 23, 26],
        default=23,
        help='C++ standard to compile against (default=23).')
    toolchain.add_argument('-stdlib',
                           choices=['libc++', 'libstdc++'],
                           help='C++ standard library to use (Clang only).')
    toolchain.add_argument(
        '-rtlib',
        choices=['', 'compiler-rt', 'libgcc'],
        default='',
        help='Compiler runtime library to use (Clang only).')
    toolchain.add_argument('-unwindlib',
                           choices=['', 'libunwind', 'libgcc'],
                           default='',
                           help='Unwind library to use (Clang only).')
    toolchain.add_argument('-fno-exceptions',
                           action='store_true',
                           help='Disables exceptions (default=false).')
    toolchain.add_argument('-fno-rtti',
                           action='store_true',
                           help='Disables RTTI (default=false).')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    validate_args(args)
    return args
