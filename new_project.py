import os, shutil, datetime, re, platform
from string import Template
from git import Repo, Submodule
from panic import panic


def new_project(project):
    """Creates a new C++ project."""

    name = os.path.basename(project.path)

    repo = generate_repo(project.path, project.git, project.package_manager)
    generate_editor(path=project.path,
                    editor=project.editor,
                    project_name=name)
    generate_clang_dotfiles(project_name=name, path=project.path)
    generate_documentation(project_name=name,
                           author=project.author,
                           remote=project.git,
                           path=project.path)

    if project.build_system == 'cmake':
        generate_cmake(project_name=name,
                       path=project.path,
                       cxx_standard=project.std,
                       toolchain_prefix=project.prefix,
                       vcpkg_enabled=project.package_manager == 'vcpkg')
    return


def generate_repo(path: str, git_choice: str, package_manager: str) -> Repo:
    if os.path.exists(path):
        panic(f"path '{path}' already exists")

    print(f'Creating repo at {path}')
    repo = Repo.init(path=path, mkdir=True)
    if git_choice.endswith('.git'):
        repo.create_remote(name='origin', url=f'{git_choice}')

    shutil.copy('templates/.gitignore', path)
    if package_manager == 'vcpkg':
        print('Downloading vcpkg')
        vcpkg = Submodule.add(repo,
                              'vcpkg',
                              path=f'{path}/vcpkg',
                              url='https://github.com/Microsoft/vcpkg.git')
        vcpkg.update(recursive=True, init=True, to_latest_revision=True)

    return repo


def generate_editor(path, editor, project_name):
    if editor == 'none':
        return

    if editor == 'vscode':
        generate_vscode(path, project_name)


def substitute_templates(replace, template, prefix, rename=None):
    with open(f'templates/{template}') as f:
        data = Template(f.read())

    suffix = template if not rename else os.path.join(
        os.path.dirname(template), rename)
    with open(f'{prefix}/{suffix}', 'w') as f:
        f.write(re.sub('^\s+$', '', data.substitute(replace)))


def generate_vscode(path, project_name):
    print('Copying VS Code files')
    vscode_dir = f'{path}/.vscode'
    os.mkdir(vscode_dir)

    vscode_templates = 'templates/.vscode'
    shutil.copy(f'{vscode_templates}/launch.json', vscode_dir)
    shutil.copy(f'{vscode_templates}/settings.json', vscode_dir)

    cmake_kits_json = 'cmake-kits.json'
    substitute_templates(
        template=f'.vscode/{cmake_kits_json}',
        prefix=path,
        replace={'project_name': project_name},
    )


def generate_clang_dotfiles(project_name, path):
    print('Copying clang-tools dotfiles')
    shutil.copy('templates/.clang-format', path)
    shutil.copy('templates/.clangd', path)

    dot_clang_tidy = '.clang-tidy'
    substitute_templates(
        template=f'{dot_clang_tidy}',
        prefix=path,
        replace={'project_name': project_name},
    )


def get_remote(remote: str) -> str:
    if not remote:
        return ''
    if 'github.com' in remote:
        text = '[GitHub]'
    elif 'gitlab.com' in remote:
        text = '[GitLab]'
    else:
        return 'our Git repo'

    if (remote.startswith('https://') or remote.startswith('http://')):
        return remote

    remote = re.sub(':', '/', remote)
    remote = re.sub('^(git(@|:\/\/))', 'https://', remote)
    remote = re.sub('.git$', '', remote)
    return f'{text}({remote})'


def generate_documentation(project_name: str, author: str, remote: str,
                           path: str):
    print('Generating documentation')
    shutil.copy('templates/README.md', path)
    substitute_templates(
        template='LICENCE',
        prefix=path,
        replace={
            'project_name': project_name,
            'copyright_holder': author,
            'year': datetime.date.today().year,
        },
    )

    substitute_templates(
        template='CODE_OF_CONDUCT.md',
        prefix=path,
        replace={
            'project_name': project_name,
            'remote': get_remote(remote)
        },
    )

    os.makedirs(f'{path}/docs/project/teams')
    shutil.copy('templates/docs/project/teams/conduct_teams.md',
                f'{path}/docs/project/teams')
    substitute_templates(
        template='docs/project/teams/leads.md',
        prefix=f'{path}',
        replace={
            'project_name': project_name,
        },
    )


def generate_cmake(project_name: str, path: str, cxx_standard,
                   toolchain_prefix, vcpkg_enabled: bool):
    substitute_templates(
        template='CMakeLists.txt',
        prefix=path,
        replace={
            'project_name': project_name,
            'cxx_standard': cxx_standard
        },
    )

    root = 'config/cmake'
    os.makedirs(f'{path}/{root}/toolchains')

    substitute_templates(
        template=f'{root}/add_targets.cmake',
        prefix=path,
        replace={'project_name': project_name},
    )
    substitute_templates(
        template=f'{root}/FindClangTidy.cmake',
        prefix=path,
        replace={'project_name': project_name},
    )
    substitute_templates(
        template=f'{root}/FindStdModules.cmake',
        prefix=path,
        replace={'project_name': project_name},
    )
    substitute_templates(
        template=f'{root}/packages.cmake',
        prefix=path,
        replace={'project_name': project_name},
    )

    target = 'x86_64'
    triple = 'x86_64-unknown-linux-gnu'
    substitute_templates(rename=f'{triple}-gcc.cmake',
                         template=f'{root}/toolchains/toolchain_base.cmake',
                         prefix=path,
                         replace={
                             'system_name': platform.system(),
                             'target': target,
                             'triple': triple,
                             'prefix': toolchain_prefix,
                             'cc': 'gcc',
                             'cxx': 'g++',
                             'ar': 'ar',
                             'rc': 'rc',
                             'ranlib': 'ranlib',
                             'linker': '-fuse-ld=lld',
                             'libcxx': '',
                             'hardening': '',
                             'libunwind': '',
                             'compiler_rt': '',
                         })
    substitute_templates(rename=f'{triple}-clang-gnu-runtime.cmake',
                         template=f'{root}/toolchains/toolchain_base.cmake',
                         prefix=path,
                         replace={
                             'system_name': platform.system(),
                             'target': target,
                             'triple': triple,
                             'prefix': toolchain_prefix,
                             'cc': 'clang',
                             'cxx': 'clang++',
                             'ar': 'ar',
                             'rc': 'rc',
                             'ranlib': 'ranlib',
                             'linker': '-fuse-ld=lld',
                             'libcxx': '-stdlib=libstdc++',
                             'hardening': '',
                             'libunwind': '',
                             'compiler_rt': '',
                         })
    substitute_templates(
        rename=f'{triple}-clang-llvm-runtime.cmake',
        template=f'{root}/toolchains/toolchain_base.cmake',
        prefix=path,
        replace={
            'system_name': platform.system(),
            'target': target,
            'triple': triple,
            'prefix': toolchain_prefix,
            'cc': 'clang',
            'cxx': 'clang++',
            'ar': 'ar',
            'rc': 'rc',
            'ranlib': 'ranlib',
            'linker': '-fuse-ld=lld',
            'libcxx': '-stdlib=libc++',
            'hardening':
            '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST',
            'libunwind': '-unwindlib=libunwind',
            'compiler_rt': '-rtlib=compiler-rt',
        })

    if vcpkg_enabled:
        vcpkg_root = 'config/vcpkg/cmake/toolchains'
        os.makedirs(f'{path}/{vcpkg_root}')
        substitute_templates(rename=f'{triple}-gcc.cmake',
                             template=f'{vcpkg_root}/toolchain_base.cmake',
                             prefix=path,
                             replace={
                                 'system_name': platform.system(),
                                 'triplet_name': f'{triple}_gcc',
                                 'triple': triple,
                                 'target': target,
                                 'prefix': toolchain_prefix,
                                 'cc': 'gcc',
                                 'cxx': 'g++',
                                 'ar': 'ar',
                                 'rc': 'rc',
                                 'ranlib': 'ranlib',
                                 'linker': '',
                                 'libcxx': '',
                                 'hardening': '',
                                 'libunwind': '',
                                 'compiler_rt': '',
                                 'lto': '-flto'
                             })
        substitute_templates(rename=f'{triple}-clang-gnu-runtime.cmake',
                             template=f'{vcpkg_root}/toolchain_base.cmake',
                             prefix=path,
                             replace={
                                 'system_name': platform.system(),
                                 'triplet_name': f'{triple}_clang_gnu_runtime',
                                 'triple': triple,
                                 'target': target,
                                 'prefix': toolchain_prefix,
                                 'cc': 'clang',
                                 'cxx': 'clang++',
                                 'ar': 'ar',
                                 'rc': 'rc',
                                 'ranlib': 'ranlib',
                                 'linker': '-fuse-ld=lld',
                                 'libcxx': '-std=libstdc++',
                                 'hardening': '',
                                 'libunwind': '',
                                 'compiler_rt': '',
                                 'lto': '-flto=thin'
                             })
        substitute_templates(
            rename=f'{triple}-clang-llvm-runtime.cmake',
            template=f'{vcpkg_root}/toolchain_base.cmake',
            prefix=path,
            replace={
                'system_name': platform.system(),
                'triplet_name': f'{triple}_clang_llvm_runtime',
                'target': target,
                'triple': triple,
                'prefix': toolchain_prefix,
                'cc': 'clang',
                'cxx': 'clang++',
                'ar': 'llvm-ar',
                'rc': 'llvm-rc',
                'ranlib': 'llvm-ranlib',
                'linker': '-fuse-ld=lld',
                'libcxx': '-std=libc++',
                'hardening':
                '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST',
                'libunwind': '-unwindlib=libunwind',
                'compiler_rt': '-rtlib=compiler-rt',
                'lto': '-flto=thin'
            })
