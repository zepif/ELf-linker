import os
import struct
import argparse
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import Section
from parse import Parser

def create_elf(output_file, input_files):
    with open(output_file, 'wb') as elf_output:
        elf_output.write(b'\x7FELF')
        elf_output.write(struct.pack('B', 2))
        elf_output.write(struct.pack('B', 1))
        elf_output.write(struct.pack('B', 1))
        elf_output.write(b'\x00' * 9)

        sections = []

        for input_file in input_files:
            with open(input_file, 'rb') as obj_file:
                elf_file = ELFFile(obj_file)
                for section in elf_file.iter_sections():
                    data = section.data()
                    sections.append((section.name, data))

        sections.sort(key=lambda x: x[0])
        sh_offset = 0x34 + len(sections) * 0x28

        for section_name, section_data in sections:
            elf_output.write(b'\x00' * 4)
            elf_output.write(struct.pack('I', Section.sh_flags['SHF_ALLOC']))
            elf_output.write(struct.pack('I', sh_offset))
            elf_output.write(struct.pack('I', len(section_data)))
            elf_output.write(struct.pack('I', 0))
            elf_output.write(struct.pack('I', 0))
            elf_output.write(struct.pack('I', 0))
            elf_output.write(struct.pack('I', 0))
            sh_offset += len(section_data)

        for section_name, section_data in sections:
            elf_output.write(section_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Custom Linker')
    parser.add_argument('output_file', help='Output ELF file')
    parser.add_argument('input_files', nargs='+', help='Input object files')
    args = parser.parse_args()

    output_file = args.output_files
    input_files = args.input_files
    input_elf_files = []

    file_parser = Parser()

    for input_file in input_files:
        input_directory = os.path.dirname(input_file)
        file_parser.file_in_directory(input_directory)
        elf_file = file_parser.parse(input_file)
        if elf_file and parser.file_exists(input_directory):
            input_elf_files.append(elf_file)
        else:
            print(f"The file '{input_file}' does not exist.")
    
    create_elf(output_file, input_elf_files)
