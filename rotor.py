ROTOR_DICT = {
    'I': {
        'name': 'I',
        'output': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'notch': 'Q'
    },
    'II': {
        'name': 'II',
        'output': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'notch': 'E'
    },
    'III': {
        'name': 'III',
        'output': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'notch': 'V'
    },
    'IV': {
        'name': 'IV',
        'output': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'notch': 'J'
    },
    'V': {
        'name': 'V',
        'output': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'notch': 'Z'
    }
}

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_rotor_choices():
    return list(ROTOR_DICT.keys())


class Rotor:
    def __init__(self, model, printing, start_letter, ring_setting):
        self.name = ROTOR_DICT[model]['name']
        self.output = ROTOR_DICT[model]['output']
        self.notch = ROTOR_DICT[model]['notch']
        self.pos = 0
        self.printing = printing
        self.set_start(start_letter)
        self.set_ring_setting(ring_setting)

    def set_start(self, letter):
        self.pos = ALPHABET.find(letter)

    def set_ring_setting(self, offset):
        self.ring_setting = offset+1
        if (offset != 0):
            dot_pos = self.output.find('A')
            new_wiring = ''
            for char in self.output:
                new_wiring += ALPHABET[(ALPHABET.find(char)+offset) % 26]
            new_dot_pos = (dot_pos + offset) % 26

            while not new_wiring[new_dot_pos] == ALPHABET[offset]:
                new_wiring = new_wiring[-1:] + new_wiring[:-1]

            self.output = new_wiring

    def forward(self, input):
        output = (input+self.pos) % 26
        cipherletter = self.output[output]
        if(self.printing):
            print('->', cipherletter, '(forward through rotor {})'.format(self.name))
        output = (ALPHABET.find(cipherletter)-self.pos) % 26
        return output

    def backward(self, input):
        output = (input+self.pos) % 26
        output = self.output.find(ALPHABET[output])
        cipherletter = ALPHABET[output]
        if(self.printing):
            print('->', cipherletter,
                  '(backwards through rotor {})'.format(self.name))
        output = (output-self.pos) % 26
        return output

    def current_letter_setting(self):
        return ALPHABET[self.pos]

    def step(self):
        if(self.printing):
            print("Stepping rotor", self.name)
        turnover = (self.current_letter_setting() == self.notch)
        self.pos = (self.pos+1) % 26
        return turnover
