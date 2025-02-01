#! /usr/bin/env nix
#! nix shell github:tomberek/-#python3With.pyelftools --command python3

import sys
import subprocess
import re
import os
from elftools.elf.elffile import ELFFile
from elftools.elf.constants import SHN_INDICES

def get_dependencies(binary_path):
    """
    Runs `ldd` on the given binary and extracts the resolved shared library paths.

    Returns:
        A set of absolute paths to all dependent shared libraries.
    """

    try:
        output = subprocess.check_output(["ldd", binary_path],
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running ldd on {binary_path}: {e.output}")
        sys.exit(1)

    libs = set()

    # Regex to match lines like:
    #    libfoo.so => /usr/lib/libfoo.so (0x00007f7d3abc5000)
    #    libc.so.6 => /lib64/libc.so.6 (0x00007f7d3a481000)
    pattern = re.compile(r"\S+ => (\S+) \(")

    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            lib_path = match.group(1)
            # Skip "not found" or lines that do not map to an actual file
            if lib_path != "not found" and os.path.exists(lib_path):
                libs.add(os.path.realpath(lib_path))

    return libs

def count_exported_symbols(elf_path):
    """
    Counts exported (i.e., not SHN_UNDEF) dynamic symbols in the given ELF object.

    Returns:
        The number of exported dynamic symbols.
    """
    exported_count = 0

    with open(elf_path, 'rb') as f:
        elf = ELFFile(f)

        # Look for the .dynsym section
        dynsym = elf.get_section_by_name('.dynsym')
        if not dynsym:
            return 0

        for symbol in dynsym.iter_symbols():
            # Check if symbol is in an actual section (i.e. not undefined)
            shndx = symbol['st_shndx']
            if shndx != SHN_INDICES.SHN_UNDEF:
                exported_count += 1

    return exported_count

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-elf>")
        sys.exit(1)

    elf_binary = sys.argv[1]

    if not os.path.exists(elf_binary):
        print(f"File {elf_binary} does not exist.")
        sys.exit(1)

    # Get the set of transitive dependencies
    dependencies = get_dependencies(elf_binary)
    # add the main binary itself
    dependencies.add(elf_binary)

    total_exported = 0
    for lib in dependencies:
        lib_exported = count_exported_symbols(lib)
        print(f"Exported symbols in {lib}: {lib_exported}")
        total_exported += lib_exported

    print(f"Total exported symbols in the dependency graph of {elf_binary}: {total_exported}")

if __name__ == "__main__":
    main()
