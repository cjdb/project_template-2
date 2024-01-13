# Copyright (c) LLVM Foundation
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
import lit.formats
import lit.util
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from lit.llvm import llvm_config
from lit.llvm.subst import ToolSubst, FindTool

config.name = 'project_template'
config.test_format = lit.formats.ShTest(not llvm_config.use_lit_shell)
config.suffixes = ['.test']
config.excludes = []
config.test_source_root = os.path.dirname(__file__)
config.test_exec_root = os.path.join(config.clang_obj_root, 'test')
homedir = tempfile.TemporaryDirectory()
config.environment['HOME'] = homedir.name

llvm_config.use_default_substitutions()
llvm_config.use_clang()

config.substitutions.append(('%PATH%', config.environment['PATH']))

config.substitutions.append((
    '%new-project',
    f'{Path(__file__).resolve().parent.resolve().parent}/generate.py 2>&1 new-project %t/project'
))
config.substitutions.append((
    '%cmake',
    'cmake -S%t/project -B%t/project/build -GNinja 2>&1 -DVCPKG_MAX_CONCURRENCY=2'
))
config.substitutions.append(('%ninja', 'ninja -C%t/project/build -v -j1 2>&1'))
config.substitutions.append(
    ('%ctest', 'ctest --test-dir %t/project/build --output-on-failure 2>&1'))

tool_dirs = []
tools = []
