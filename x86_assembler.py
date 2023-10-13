class Assembler:
    def __init__(self):
        self.symbol_table = {}

        self.registers = {}
        for i in range(6):
            register_name = f'R{i}'
            self.registers[register_name] = i

        self.opcodes = {
            'ADD': 0x00,
            'SUB': 0x01,
            'LD': 0x02,
            'ST': 0x03,
            'BNE': 0x04,
            'AND': 0x05,
            'OR': 0x06,
            'XOR': 0x07,
            'SHL': 0x08,
            'SHR': 0x09,
            'MUL': 0x0A,
            'DIV': 0x0B,
        }
    
    def translate_instruction(self, instruction):
        parts = instruction.split()
        if not parts:
            return None
        
        opcode = parts[0]
        print(f"opcode : {opcode}")
        if opcode not in self.opcodes:
            print("Unknown opcode")
            return None  # Unknown opcode

        opcode_value = self.opcodes[opcode]
        binary_instruction = (opcode_value << 12)

        if opcode == 'ADD' or opcode == 'SUB' or opcode == 'AND' or opcode == 'OR' or opcode == 'XOR' or opcode == 'SHL' or opcode == 'SHR' or opcode == 'MUL' or opcode == 'DIV':
            if len(parts) != 4:
                print("Incorrect number of operands")
                return None  # Incorrect number of operands
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if rd not in self.registers or rs1 not in self.registers or rs2 not in self.registers:
                print("Invalid register")
                return None  # Invalid register
            binary_instruction |= (self.registers[rd] << 8) | (self.registers[rs1] << 4) | self.registers[rs2]
        elif opcode == 'LD' or opcode == 'ST':
            if len(parts) != 3:
                print("Incorrect number of operands")
                return None  # Incorrect number of operands
            rd, mem_address = parts[1], parts[2]
            if rd not in self.registers:
                print("Invalid register")
                return None  # Invalid register
            if mem_address in self.symbol_table:
                mem_address = self.symbol_table[mem_address]
            binary_instruction |= (self.registers[rd] << 8) | mem_address
        elif opcode == 'BNE':
            if len(parts) != 4:
                print("Incorrect number of operands")
                return None  # Incorrect number of operands
            rs1, rs2, label = parts[1], parts[2], parts[3]
            if rs1 not in self.registers or rs2 not in self.registers:
                print("Invalid register")
                return None  # Invalid register
            if label not in self.symbol_table:
                print("Unknown label")
                return None  # Unknown label
            offset = self.symbol_table[label] - (self.symbol_table[instruction] + 1)
            binary_instruction |= (self.registers[rs1] << 8) | (self.registers[rs2] << 4) | offset

        return binary_instruction.to_bytes(2, byteorder='big')
    
    def extract_loops(self, assembly_code):
        loops = []
        lines = assembly_code.split('\n')
        inside_loop = False
        current_loop = []
        for line in lines:
            if 'LOOP_START' in line:
                if inside_loop:
                    print("Nested loops are not supported.")
                    return None
                inside_loop = True
                current_loop.append(line)
            elif 'LOOP_END' in line:
                if not inside_loop:
                    print("Unexpected LOOP_END found.")
                    return None
                current_loop.append(line)
                loops.append('\n'.join(current_loop))
                inside_loop = False
                current_loop = []
            elif inside_loop:
                current_loop.append(line)

        if inside_loop:
            print("Unterminated loop found.")
            return None

        return loops

    def assemble(self, assembly_code, output_file):
        binary_code = []
    
        for line in assembly_code.split('\n'):
            semicolon_pos = line.find(';')
            if semicolon_pos >= 0:
                line = line[:semicolon_pos]
            if line == None:
                continue
            binary_instruction = assembler.translate_instruction(line)
            if binary_instruction is not None:
                binary_code.append(binary_instruction)
        
        with open(output_file, 'wb') as f:
            for binary_instruction in binary_code:
                f.write(binary_instruction)
    
    def initialize_registers(self):
        for register in self.registers:
            self.registers[register] = 42

if __name__ == '__main__':
    # Example assembly code
    assembly_code = """
    ; Calculate the Sum of an Array
    LD R1, #0
    LD R2, R0
    LD R3, [R0]
    LD R4, #0

    LOOP_START:
    LOOP_END:

    LOOP_START:
    ADD R1, R1, R3
    ADD R4, R4, #1
    LD R3, [R4]
    SUB R2, R2, #1
    BNE R2, R0, LOOP_START

    ST [R0], R1
    LOOP_END:

    LD R5, #0
    """
    

    output_file = 'output.bin'
    
    assembler = Assembler()
    assembler.initialize_registers()
    assembler.symbol_table = {'LOOP': 3}

    loops = assembler.extract_loops(assembly_code)
    if loops is not None:
        #i = 0
        for i, loop in enumerate(loops):
            print(f'Loop {i + 1}:\n{loop}')
            #i += 1

    print(end='\n\n')

    assembler.assemble(assembly_code, output_file)
