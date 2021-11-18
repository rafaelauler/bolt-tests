# BOLT large testsuite

# These tests run BOLT using large binaries captured from an opensource
# environment

find_package(Python3 COMPONENTS Interpreter)

set(BOLTTESTS_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(BOLTTESTS_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR})

set(BOLTTESTS_DEPS
  clang
  count
  FileCheck
  lld
  llvm-bolt
  llvm-boltdiff
  llvm-config
  llvm-dwarfdump
  llvm-mc
  llvm-nm
  llvm-objdump
  llvm-readobj
  llvm-readelf
  llvm-strip
  merge-fdata
  not
  perf2bolt
  yaml2obj
  )

if (NOT DEFINED Python3_EXECUTABLE)
  message(FATAL_ERROR "Cannot run bolt-tests without python 3")
endif()

configure_lit_site_cfg(
  ${CMAKE_CURRENT_SOURCE_DIR}/lit.site.cfg.py.in
  ${CMAKE_CURRENT_BINARY_DIR}/lit.site.cfg.py
  MAIN_CONFIG
  ${CMAKE_CURRENT_SOURCE_DIR}/lit.cfg.py
  )

# This may easily OOM the machine, so we limit jobs to 4
add_lit_testsuite(check-large-bolt "Running bolt large bins testsuite"
  ${CMAKE_CURRENT_BINARY_DIR}
  DEPENDS ${BOLTTESTS_DEPS}
  ARGS "-j4"
  )

add_lit_testsuites(BOLTTESTS ${CMAKE_CURRENT_SOURCE_DIR}
  DEPENDS ${BOLTTESTS_DEPS}
  )

set_target_properties(check-large-bolt PROPERTIES FOLDER "bolt large bins testsuite")
