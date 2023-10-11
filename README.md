# ELf-linker
 
This linker could be used for parsing and linking object files. It can be used to create an ELF binary from multiple input object files.

## Features

- Parses COFF and Mach-O object files.
- Creates an ELF binary from input object files.
- Lists files and directories in a specified directory.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ELf-linker.git
   cd ELf-linker
   pip install -r requirements.txt
   ```
2. Install the requird packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Parsing and Listing Files

To parse object files and list files and directories in a directory, use the following command:

```bash
python linker.py /path/to/output.elf /path/to/input_files/ /path/to/input_files/
```

Replace /path/to/output.elf with the desired output ELF file path and /path/to/input_files/ with the directory containing your input object files.

## License

This project is licensed under the MIT License.