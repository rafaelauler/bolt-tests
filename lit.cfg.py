# -*- Python -*-

import os
import platform
import re
import subprocess
import sys
import tempfile

import lit.formats
import lit.util

from lit.llvm import llvm_config
from lit.llvm.subst import ToolSubst
from lit.llvm.subst import FindTool

# Configuration file for the 'lit' test runner.

# name: The name of this test suite.
config.name = 'bolt-tests'

# testFormat: The test format to use to interpret tests.
#
# For now we require '&&' between commands, until they get globally killed and
# the test runner updated.
config.test_format = lit.formats.ShTest(not llvm_config.use_lit_shell)

# suffixes: A list of file extensions to treat as test files.
config.suffixes = ['.c', '.cppm', '.m', '.mm', '.cu',
                   '.ll', '.cl', '.s', '.S', '.modulemap', '.test', '.rs']

# excludes: A list of directories to exclude from the testsuite. The 'Inputs'
# subdirectories contain auxiliary inputs for various tests in their parent
# directories.
config.excludes = ['Inputs']

# test_source_root: The root path where tests are located.
config.test_source_root = os.path.join(config.bolt_tests_src_root, "test")

# test_exec_root: The root path where tests should be run.
config.test_exec_root = config.bolt_tests_obj_root

llvm_config.use_default_substitutions()

tool_dirs = [config.llvm_tools_dir,
             config.test_source_root]

tools = [
    ToolSubst('llvm-bolt', unresolved='fatal'),
    ToolSubst('llvm-dwarfdump', unresolved='fatal'),
    ToolSubst('llvm-nm', unresolved='fatal'),
    ToolSubst('llvm-objdump', unresolved='fatal'),
    ToolSubst('llvm-strip', unresolved='fatal'),
    ToolSubst('llvm-readelf', unresolved='fatal'),
    ToolSubst('perf2bolt', unresolved='fatal'),
]
llvm_config.add_tool_substitutions(tools, tool_dirs)

# Propagate path to symbolizer for ASan/MSan.
llvm_config.with_system_environment(
    ['ASAN_SYMBOLIZER_PATH', 'MSAN_SYMBOLIZER_PATH'])

config.substitutions.append(('%PATH%', config.environment['PATH']))

def calculate_arch_features(arch_string):
    features = []
    for arch in arch_string.split():
        features.append(arch.lower() + '-registered-target')
    return features

config.targets = frozenset(config.targets_to_build.split())

llvm_config.feature_config(
    [('--assertion-mode', {'ON': 'asserts'}),
     ('--cxxflags', {r'-D_GLIBCXX_DEBUG\b': 'libstdcxx-safe-mode'}),
        ('--targets-built', calculate_arch_features)
     ])

# Check if we should allow outputs to console.
run_console_tests = int(lit_config.params.get('enable_console', '0'))
if run_console_tests != 0:
    config.available_features.add('console')
