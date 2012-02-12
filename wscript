#! /usr/bin/env python2

import os.path
import sys

build_tools = os.path.join('.', 'tools', 'waf')
sys.path.append(build_tools)

APPNAME = 'stechec2'
VERSION = '2012'

top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_cxx')
    opt.load('unittest_gtest')
    opt.load('boost')

    opt.add_option('--enable-debug', action = 'store_true', default = False,
                   help = 'build a debug version', dest = 'debug')
    opt.add_option('--enable-werror', action = 'store_true', default = False,
                   help = 'interpret warnings as errors', dest = 'werror')

def configure(conf):
    conf.load('compiler_cxx')
    conf.load('unittest_gtest')

    # Warning flags
    conf.check_cxx(cxxflags = '-Wall')
    conf.check_cxx(cxxflags = '-Wextra')
    conf.check_cxx(cxxflags = '-pedantic')

    conf.env.append_value('CXXFLAGS', ['-Wall', '-Wextra', '-pedantic',
                                       '-Wno-variadic-macros'])

    # Check for C++0x
    conf.check_cxx(cxxflags = '-std=c++0x')
    conf.check_cxx(cxxflags = '-std=c++0x', header_name = "cstdint")
    conf.check_cxx(cxxflags = '-std=c++0x', msg = 'Checking for std::shared_ptr',
                   fragment = '''
                   #include <memory>
                   int main() { std::shared_ptr<int> p; }
                   ''')
    conf.check_cxx(cxxflags = '-std=c++0x', msg = 'Checking for std::array',
                   fragment = '''
                   #include <array>
                   int main() { std::array<int, 4> a; }
                   ''')
    conf.env.append_value('CXXFLAGS', '-std=c++0x')

    # Debug / Release
    if conf.options.debug:
        conf.check_cxx(cxxflags = '-g')
        conf.check_cxx(cxxflags = '-ggdb3')
        conf.env.append_value('DEFINES', '__DEBUG__')
        conf.env.append_value('CXXFLAGS', ['-g', '-ggdb3'])
    else:
        conf.check_cxx(cxxflags = '-O2')
        conf.check_cxx(cxxflags = '-ffast-math')
        conf.env.append_value('CXXFLAGS', ['-O2', '-ffast-math'])

    # ZeroMQ
    conf.check_cfg(package = 'libzmq', uselib_store = 'ZeroMQ',
                   args = ['--cflags', '--libs'])

    # Other
    conf.env.append_value('INCLUDES', 'src/lib')

    # Boost
    conf.load('boost')
    conf.check_boost(lib = 'program_options')

    # Werror support - at the end to avoid false negatives in the checks
    if conf.options.werror:
        conf.check_cxx(cxxflags = '-Werror')
        conf.env.append_value('CXXFLAGS', '-Werror')

def build(bld):
    build_libs(bld)
    build_client(bld)
    build_server(bld)

def build_libs(bld):
    build_net(bld)
    build_rules(bld)
    build_utils(bld)

def build_net(bld):
    bld.stlib(
        source = """
            src/lib/net/socket.cc
            src/lib/net/server.cc
            src/lib/net/client.cc
            src/lib/net/message.cc
        """,
        defines = ['MODULE_COLOR=ANSI_COL_PURPLE', 'MODULE_NAME="network"'],
        target = 'net',
        use = ['ZeroMQ', 'utils']
    )

def build_utils(bld):
    bld.stlib(
        source = """
            src/lib/utils/dll.cc
            src/lib/utils/log.cc
            src/lib/utils/options.cc
        """,
        defines = ['MODULE_COLOR=ANSI_COL_GREEN', 'MODULE_NAME="utils"'],
        target = 'utils'
    )

    for test in ['buffer', 'options']:
        bld.program(
            features = 'gtest',
            source = 'src/lib/utils/tests/test-%s.cc' % test,
            target = 'utils-test-%s' % test,
            use = ['utils', 'BOOST']
        )

def build_rules(bld):
    bld.stlib(
        source = """
            src/lib/rules/action.cc
            src/lib/rules/state.cc
        """,
        defines = ['MODULE_COLOR=ANSI_COL_BLUE', 'MODULE_NAME="rules"'],
        target = 'rules'
    )

    for test in ['action', 'state']:
        bld.program(
            features = 'gtest',
            source = 'src/lib/rules/tests/test-%s.cc' % test,
            target = 'rules-test-%s' % test,
            use = ['rules']
        )

def build_client(bld):
    bld.program(
        source = """
            src/client/main.cc
            src/client/options.cc
            src/client/client.cc
        """,
        target = 'stechec2-client',
        defines = ['MODULE_COLOR=ANSI_COL_YELLOW', 'MODULE_NAME="client"',
            'MODULE_VERSION="%s"' % VERSION],
        use = ['utils', 'net', 'BOOST']
    )

def build_server(bld):
    bld.program(
        source = """
            src/server/main.cc
            src/server/options.cc
            src/server/server.cc
        """,
        target = 'stechec2-server',
        defines = ['MODULE_COLOR=ANSI_COL_RED', 'MODULE_NAME="server"',
            'MODULE_VERSION="%s"' % VERSION],
        use = ['utils', 'net', 'BOOST']
    )
