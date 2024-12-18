import copy
from typing import List


def parse_register(register_line: str):
    return int(
        register_line.strip()
        .replace("Register ", "")
        .replace("A: ", "")
        .replace("B: ", "")
        .replace("C: ", "")
    )


def parse_program(program_line: str):
    return list(map(int, program_line.strip().replace("Program: ", "").split(",")))


def read_input(filename="input.txt"):
    with open(filename, "r") as file:
        register_a = parse_register(file.readline())
        register_b = parse_register(file.readline())
        register_c = parse_register(file.readline())
        file.readline()
        program = parse_program(file.readline())

    return Computer(register_a, register_b, register_c, program)


def logger(func):
    def wrapper(*args, **kwargs):
        print(f"\n\n-----------------------------------\n")
        result = func(*args, **kwargs)
        print(f"")
        return result

    return wrapper


class Computer:
    def copy(self):
        return Computer(
            self.register_a,
            self.register_b,
            self.register_c,
            copy.deepcopy(self.program),
        )

    def __init__(self, register_a, register_b, register_c, program):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.program = program
        self.instruction_pointer = 0
        self.output = []
        self.__jump_3_same_repetition = None

    def __str__(self):
        return f"Computer(Program - {self.__program_str}, Pointer - {self.instruction_pointer}, A - {self.register_a}, B - {self.register_b}, C - {self.register_c}) -> Output {self.__program_output}"

    @property
    def __program_str(self):
        return ",".join(map(str, self.program))

    @property
    def __program_output(self):
        return ",".join(map(str, self.output))

    def __3bit(self, value):
        tmp = value & 0b111
        # print(f"__3bit({value}) = {tmp}")
        return tmp

    #############################################
    # opcode            - instruction
    # literal operands  - value
    # combo operands    - get_combo_operand(value)
    ##############################################

    def get_combo_operand(self, value):
        if 3 >= value >= 0:
            return value
        elif 4 == value:
            return self.register_a
        elif 5 == value:
            return self.register_b
        elif 6 == value:
            return self.register_c
        else:
            raise ValueError(f"Invalid combo operand {value}")

    def dv(self, operands) -> int:
        numerator = self.register_a
        denominator = pow(2, self.get_combo_operand(operands))
        result = numerator // denominator
        return result

    def rdv(self, value):
        # returns operand // 2^value
        return pow(1 / 2, value) // self.register_a

    def adv(self, operands):
        numerator = self.register_a
        denominator = pow(2, self.get_combo_operand(operands))
        result = numerator // denominator
        # print(f"adv({operands}) = {numerator} // {denominator} = {result}")
        self.register_a = result

    def bxl(self, operands):
        result = self.register_b ^ operands
        # print(f"bxl({operands}) = {self.register_b}")
        self.register_b = result

    def bst(self, operands):
        result = self.get_combo_operand(operands) % 8
        result = self.__3bit(result)
        # print(
        #     f"bst({operands}) = {self.register_b} & {self.get_combo_operand(operands)} = {result}"
        # )
        self.register_b = result

    def jnz(self, operands):
        if self.register_a == 0:
            return
        self.instruction_pointer = operands
        # print(f"jnz({operands}) = {self.instruction_pointer}")

    def bxc(self, operands):
        result = self.register_b ^ self.register_c
        # print(f"bxc({operands}) = {self.register_b} & {self.register_c} = {result}")
        self.register_b = result

    def out(self, operands):
        result = self.get_combo_operand(operands) % 8
        self.output.append(result)
        # print(f"out({operands}) = {result}")

    def bdv(self, operands):
        numerator = self.register_a
        denominator = pow(2, self.get_combo_operand(operands))
        result = numerator // denominator
        # print(f"bdv({operands}) = {numerator} // {denominator} = {result}")
        self.register_b = result

    def cdv(self, operands):
        numerator = self.register_a
        denominator = pow(2, self.get_combo_operand(operands))
        result = numerator // denominator
        # print(f"cdv({operands}) = {numerator} // {denominator} = {result}")
        self.register_c = result

    def read_instruction(self):
        return (
            self.program[self.instruction_pointer],
            self.program[self.instruction_pointer + 1],
        )

    def handle_jump_3_same_repetition(self, operands):
        if (
            self.__jump_3_same_repetition is not None
            and self.__jump_3_same_repetition[0] == self.instruction_pointer
            and self.__jump_3_same_repetition[1] == operands
        ):
            if self.__jump_3_same_repetition[2] >= 3:
                return False
            self.__jump_3_same_repetition[2] += 1
        else:
            self.__jump_3_same_repetition = [self.instruction_pointer, operands, 1]
        return True

    # @logger
    def run_instruction(self) -> bool:
        if self.instruction_pointer >= len(self.program) - 1:
            return False
        opcode, operands = self.read_instruction()
        # print(f"Running instruction {opcode} with operands {operands}")
        skip_jump = False

        if opcode == 0:
            self.adv(operands)
        elif opcode == 1:
            self.bxl(operands)
        elif opcode == 2:
            self.bst(operands)
        elif opcode == 3:
            self.jnz(operands)
            return self.handle_jump_3_same_repetition(operands)
        elif opcode == 4:
            self.bxc(operands)
        elif opcode == 5:
            self.out(operands)
        elif opcode == 6:
            self.bdv(operands)
        elif opcode == 7:
            self.cdv(operands)
        else:
            raise ValueError(f"Invalid opcode {opcode}")

        if not skip_jump:
            self.instruction_pointer += 2
            self.__jump_3_same_repetition = None

        return True


def calc_distance(program: List, output: List) -> str:
    tmp_program = list(reversed(program.copy()))
    tmp_output = list(reversed(output.copy()))

    assert len(tmp_program) == len(tmp_output)

    distance = ""
    for p, o in zip(tmp_program, tmp_output):
        distance += str(int(p - o))

    print(f"Distance {distance}")

    return distance




if __name__ == "__main__":
    computer = read_input()
    # candidate = 100000000000000000030404040405

    candidates = [0]
    for i in range(len(computer.program)):
        
        next_candidates = []
        for candidate in candidates:
            for j in range(8):
                tmp_computer = computer.copy()
                new_candidate = (candidate << 3) + j  # found how to smart divide by power of 2
                tmp_computer.register_a = new_candidate
                while tmp_computer.run_instruction():
                    pass
                print(f"Trying candidate {new_candidate} with output {tmp_computer.output}")
                if tmp_computer.output[-i - 1 :] == tmp_computer.program[-i - 1 :]:
                    next_candidates.append(new_candidate)

        candidates = next_candidates
    
    print(f"Found {candidates} candidates")

