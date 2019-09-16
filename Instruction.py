class Instruction:
    def __init__(self, current_state, new_state):
        self.current_state = current_state
        self.new_state = new_state


class ReadInstruction(Instruction):
    def __init__(self, current_state, new_state, read_char):
        self.read_char = read_char
        super().__init__(current_state, new_state)


class WriteInstruction(Instruction):
    def __init__(self, current_state, new_state, write_string):
        self.write_string = write_string
        super().__init__(current_state, new_state)


class InitialInstruction(Instruction):
    def __init__(self, current_state, new_state):
        super().__init__(current_state, new_state),
