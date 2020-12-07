"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        self.reg = {}
        self.reg = [0] * 8
        self.reg[7] = 0xF4

        self.pc = 0


        # self.registers = [0] * 8
        # self.registers[7] = 0xF4
        self.halted = False

    def ram_read(self, memory_address_register):
        """Accepts an address and returns the value stored there"""

        return self.ram[memory_address_register]

    def ram_write(self, memory_data_register, memory_address_register):
        """Accepts a value to write and the address to write to it"""

        self.ram[memory_address_register] = memory_data_register


    def load(self):
        """Load a program into memory."""

        address = 0
        program = []

        print('Instructions')
        with open(sys.argv[1], 'r') as file:
            for line in file:
                if line[0].isdigit():
                    str_val = line[0:8]
                    print(line[0:8])
                    int_val = int(line[0:8], 2)
                    program.append(int_val)
        print('------------')

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        ir = self.pc
        running = True

        while running:
            instruction = self.ram_read(ir)
            operand_a = self.ram_read(ir + 1)
            operand_b = self.ram_read(ir + 2)

            if instruction == 0b10000010:  # LDI
                self.reg[operand_a] = operand_b
                ir += 3

            elif instruction == 0b01000111:  # PRN
                print(self.reg[operand_a])
                ir += 2

            elif instruction == 0b00000001:  # HLT
                running = False
                ir += 1

            elif instruction == 0b10100010:  # MUL
                product = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = product
                ir += 3

            else:
                print(f'Unknown instructions: {instruction}')
