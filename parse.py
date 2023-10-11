import os
import sys
import pefile
from macholib import MachO

class Parser:
    def __init__(self):
        pass

    def parse(self, file_path):
        if file_path.endswith('.o') and sys.platform.startswith('win'):
            pe = pefile.PE(file_path)
            print("COFF Header:")
            print(f"Machine: {pe.FILE_HEADER.Machine}")
            print(f"Number of Sections: {pe.FILE_HEADER.NumberOfSections}")

            print("Section Headers:")
            for section in pe.sections:
                print(f"Section Name: {section.Name.decode('utf-8').strip(chr(0))}")
                print(f"Virtual Size: {section.Misc_VirtualSize}")
                print(f"Raw Size: {section.SizeOfRawData}")

            print("Symbols:")
            for symbol in pe.SHGetSymbols():
                print(f"Symbol: {symbol.name} (Value: {symbol.value}")

            print("Relocations:")
            for section in pe.sections:
                for relocation in section.relocations:
                    print(f"Section: {section.Name.decode('utf-8').strip(chr(0))}")
                    print(f"Relocation Offset: {relocation.rva}")

        if file_path.endswith('.o') and sys.platform.startswith('darwin'):
            macho = MachO.MachO(file_path)
            for header in macho.headers:
                print(f"Header: {header}")
                for load_command in header.commands:
                    print(f"Load Command: {load_command.get_cmd_name()}")
                    if load_command.get_cmd_name() == "LC_SYMTAB":
                        symtab = macho.get_dyld_info()[header.ncmds - 1]
                        for sym in symtab.nlist:
                            print(f"Symbol: {sym}")
        
        if file_path.endswith('.obj'):
            pe = pefile.PE(file_path)
            print("COFF Header:")
            print(f"Machine: {pe.FILE_HEADER.Machine}")
            print(f"Number of Sections: {pe.FILE_HEADER.NumberOfSections}")

            print("Section Headers:")
            for section in pe.sections:
                print(f"Section Name: {section.Name.decode('utf-8').strip(chr(0))}")
                print(f"Virtual Size: {section.Misc_VirtualSize}")
                print(f"Raw Size: {section.SizeOfRawData}")

            print("Symbols:")
            for symbol in pe.SHGetSymbols():
                print(f"Symbol: {symbol.name} (Value: {symbol.value})")

            print("Relocations:")
            for section in pe.sections:
                for relocation in section.relocations:
                    print(f"Section: {section.Name.decode('utf-8').strip(chr(0))}")
                    print(f"Relocation Offset: {relocation.rva}")

        print(f"Unsupported format: {file_path}")
        return None

    def file_in_directory(self, directory):
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if entry.is_file():
                        print(f"File: {entry.name}")
                    elif entry.is_dir():
                        print(f"Directory: {entry.name}")
        except FileNotFoundError:
            print(f"Directory '{directory}' not found.")
        except PermissionError:
            print(f"Permission denied for '{directory}'.")
    
    def file_exists(self, file_path):
        return os.path.exists(file_path)

if __name__ == '__main__':
    pass
