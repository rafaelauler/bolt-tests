# bolt-tests

This is a testsuite containing large binaries for [BOLT](https://github.com/facebookincubator/BOLT).

## Usage

Install binary tests prerequisites (libtinfo.so.5):
```
sudo apt-get install libtinfo5
```

Configure LLVM with the `LLVM_EXTERNAL_PROJECTS` and
`LLVM_EXTERNAL_PROJECTS_SOURCE_DIR` cmake flags. Example:

```
$ git clone https://github.com/facebookincubator/BOLT llvm-bolt
$ git clone https://github.com/rafaelauler/bolt-tests bolt-tests
$ mkdir build
$ cd build
$ cmake -G Ninja ../llvm-bolt/llvm \
   -DLLVM_TARGETS_TO_BUILD="X86;AArch64" \
   -DLLVM_ENABLE_PROJECTS="clang;lld;bolt" \
   -DLLVM_EXTERNAL_PROJECTS="bolttests" \
   -DLLVM_EXTERNAL_BOLTTESTS_SOURCE_DIR=$(pwd)/../bolt-tests
$ ninja check-large-bolt
```

When this repo is configured as an external project, it will add itself as an extra target in LLVM named "check-large-bolt". Just build that target to run this testsuite.
