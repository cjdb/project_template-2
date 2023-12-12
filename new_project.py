import os, shutil
from string import Template
from git import Repo, Submodule
from panic import panic

def new_project(project):
    """Creates a new C++ project."""

    if not project.root:
        project.root = './'

    path = f'{project.root}/{project.name}'
    generate_repo(path, project.git, project.package_manager)
    generate_editor(path, project.editor, project.name)

    if project.build_system == 'cmake':
        print('todo: init cmake')
    return

def generate_repo(path, git_choice, package_manager):
    if os.path.exists(path):
        panic(f"path '{path}' already exists")

    print(f'Creating repo at {path}')
    repo = Repo.init(path=path, mkdir=True)
    if git_choice.endswith('.git'):
        repo.create_remote(name='origin', url=f'{git_choice}')

    shutil.copy('templates/.gitignore', path)
    if package_manager == 'vcpkg':
        print('Downloading vcpkg')
        vcpkg = Submodule.add(repo, 'vcpkg', path=f'{path}/vcpkg', url='https://github.com/Microsoft/vcpkg.git')
        vcpkg.update(recursive=True, init=True, to_latest_revision=True)

    return

def generate_editor(path, editor, project_name):
    if editor == 'none':
        return

    if editor == 'vscode':
        generate_vscode(path, project_name)

def generate_vscode(path, project_name):
    vscode_dir = f'{path}/.vscode'
    cmake_kits_template = 'templates/.vscode/cmake-kits.json'
    os.mkdir(vscode_dir)
    with open(cmake_kits_template) as f:
        cmake_kits = Template(f.read())
    with open(f'{vscode_dir}/cmake-kits.json', 'w') as f:
        replace = {'project_name': project_name}
        f.write(cmake_kits.substitute(replace))
