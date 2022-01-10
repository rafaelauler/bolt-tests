# bolt-tests

This is a testsuite containing large binaries for [BOLT](https://github.com/facebookincubator/BOLT).

## Git LFS
This repository uses [Git Large File Storage](https://github.com/git-lfs/git-lfs) to work around GitHub's file size limit which is 100Mb for plain Git repositories and 2GB with [LFS with GitHub Free](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage).

Please follow the official instructions to install git-lfs:
[Installation](https://github.com/git-lfs/git-lfs/wiki/Installation).

## Usage
### Prerequisites
- Install binary tests prerequisites (libtinfo.so.5):
```
sudo apt-get install libtinfo5
```
- Install perf tools:
```
sudo apt-get install linux-tools-`uname -r`
```
### LLVM CMake configuration
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
