import sys

SYMBOL_TABLE = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576
}

# Checks the line for comments and removes them.
def remove_comments(line):
    comment = line.find('//')
    if comment != -1:
        return line[:comment].strip()
    else:
        return line.strip()

def isAInstruction(instruction):
    if instruction[0] == '@':
        return True
    else:
        return False

def isLabel(instruction):
    if instruction[0] == '(' and instruction[-1] == ')':
        return True
    else:
        return False

# Should return 7 bits: a c1 c2 c3 c4 c5 c6
def comp(instr):
    lookup_table = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        '!D': '001101',
        '!A': '110001',
        '-D': '001111',
        '-A': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101',
        'M': '110000',
        '!M': '110001',
        '-M': '110011',
        'M+1': '110111',
        'M-1': '110010',
        'D+M': '000010',
        'D-M': '010011',
        'M-D': '000111',
        'D&M': '000000',
        'D|M': '010101',
    }
    if instr.find('M') == -1:
        # No M
        return '0' + lookup_table[instr]
    else:
        # Yes M
        return '1' + lookup_table[instr]

def dest(instr):
    lookup_table = {
        'null': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }
    return lookup_table[instr]

def jmp(instr):
    lookup_table = {
        'null': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }
    return lookup_table[instr]

# Address of free register for storing variables
free_mem_addr = 16

def translate_A_instruction(instruction):
    global free_mem_addr

    # If non symbol instruction
    if instruction[1:].isnumeric():
        address = int(instruction[1:])
    # If symbol instruction
    else:
        var_name = instruction[1:]

        # Handles address variables
        if var_name not in SYMBOL_TABLE:
            SYMBOL_TABLE.update({var_name: free_mem_addr})
            free_mem_addr += 1

        address = SYMBOL_TABLE[var_name]

    return '0' + bin(address)[2:].zfill(15)

def translate_C_instruction(instruction):
    dest_index = instruction.find('=')
    jmp_index = instruction.find(';')
    isDest = True if dest_index != -1 else False
    isJmp = True if jmp_index != -1 else False
    Dest = instruction[:dest_index] if isDest else 'null'
    Jmp = instruction[jmp_index + 1:] if isJmp else 'null'
    if isDest:
        if isJmp:
            Comp = instruction[dest_index + 1: jmp_index]
        else:
            Comp = instruction[dest_index + 1:]
    else:
        if isJmp:
            Comp = instruction[:jmp_index]
        else:
            Comp = instruction

    return '111' + comp(Comp) + dest(Dest) + jmp(Jmp)


def translator(instruction_set):
    translated = []
    for instruction in instruction_set:
        if isAInstruction(instruction):
            translated.append(translate_A_instruction(instruction))
        else:
            translated.append(translate_C_instruction(instruction))
    return translated

def labelParse(instruction, line):
    label = instruction[1:-1]
    SYMBOL_TABLE.update({label: line})

def Parser(asm_code):
    instructions = []
    counter = 0
    for i in asm_code:
        cleaned_line = remove_comments(i)
        if len(cleaned_line) != 0:
            if isLabel(cleaned_line):
                labelParse(cleaned_line, counter)
            else:
                instructions.append(cleaned_line)
                counter += 1

    return instructions

def main():
    # Checking if the user provided the file name.
    if len(sys.argv) != 2:
        print('Usage: python3 assembler.py [file_path]')
        return

    # Trying to read file. Returns error to user if unable to read file.
    try:
        asm_file = open(sys.argv[1], 'r')
    except:
        print('Invalid file name.')
        return

    if sys.argv[1].split('/')[-1].find('.asm') == -1:
        print('Invalid File. Assembler only supports .asm assembly files.')
        return

    asm_code = [i.strip() for i in asm_file.read().split('\n')]

    parsed_instructions = Parser(asm_code)
    translated_instructions = translator(parsed_instructions)

    with open(sys.argv[1][:-4] + '.hack', 'w') as f:
        f.write('\n'.join(translated_instructions))


if __name__ == '__main__':
    main()