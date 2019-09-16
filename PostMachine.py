import Instruction as Ins

MAX_EXECUTIONS = 500
HALTED_STATE = 1
LOCKED_STATE = 2
LOOP_STATE = 3


class PostMachine:
    def __init__(self, program, tape):
        self.current_state = 's'
        self.current_execution = 0
        self.tape = tape
        self.instruction = []
        for instruction in program:
            self.instruction.append(inst_typedef(instruction))

    def get_next_instruction(self):
        for i in self.instruction:
            if i is not None and i.current_state == self.current_state:
                if isinstance(i, Ins.ReadInstruction):
                    if i.read_char == self.tape[0]:
                        return i
                else:
                    return i
        return None

    def process_machine(self):
        halted = False
        locked = False
        in_loop = False
        end_code = 0

        while not halted and not locked and not in_loop:
            next_instruction = self.get_next_instruction()
            self.current_execution += 1
            locked = next_instruction is None
            if locked:
                end_code = LOCKED_STATE
                break

            if isinstance(next_instruction, Ins.ReadInstruction):
                consumed = self.tape[0]
                self.tape = self.tape[1:]
                self.print_process(next_instruction, consumed, None)
                self.current_state = next_instruction.new_state
            elif isinstance(next_instruction, Ins.WriteInstruction):
                added = next_instruction.write_string
                self.tape = self.tape+added
                self.print_process(next_instruction, None, added)
                self.current_state = next_instruction.new_state
            elif isinstance(next_instruction, Ins.InitialInstruction):
                self.print_process(next_instruction, None, None)
                self.current_state = next_instruction.new_state
            halted = self.current_state == 'h'
            if halted:
                end_code = HALTED_STATE
            in_loop = self.current_execution >= MAX_EXECUTIONS
            if in_loop:
                end_code = LOOP_STATE
        self.print_end(end_code)

    def print_process(self, next_ins, consumed, added):
        print_message = '\'{}\' -> \'{}\' | Current tape: \'{}\''.format(self.current_state,
                                                                         next_ins.new_state,
                                                                         ''.join(self.tape))
        print('Actual state: '+print_message, end='')
        if consumed is not None:
            print('\t| (Consumed '+consumed+')', end='')
        if added is not None:
            print('\t| (Added '+added+')', end='')
        print('\n')

    @staticmethod
    def print_end(end_code):
        if end_code == HALTED_STATE:
            print('\nProcess ended with success! \t CODE 1 - HALT\n')
        elif end_code == LOCKED_STATE:
            print('\nProcess ended with error! \t CODE 2 - LOCKED\n')
        else:
            print('\nProcess ended with error! \t CODE 3 - LOOP\n')


def inst_typedef(instruction):
    if instruction[0] == '*':
        return None
    elif instruction[0] == 's':
        return Ins.InitialInstruction(instruction[0], instruction[4])
    elif instruction[2] == ' ':
        return Ins.WriteInstruction(instruction[0], instruction[4], instruction[6:-1])
    else:
        return Ins.ReadInstruction(instruction[0], instruction[4], instruction[2])


def main():
    file_name = input('Enter the file name: ')
    file = open(file_name, "r")
    file_entry = file.readlines()
    tape = input('Enter the initial tape: ')
    machine = PostMachine(file_entry, tape)
    machine.process_machine()


if __name__ == '__main__':
    main()
