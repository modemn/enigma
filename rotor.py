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
    def __init__(self, model):
        self.name = ROTOR_DICT[model]['name']
        self.output = ROTOR_DICT[model]['output']
        self.notch = ROTOR_DICT[model]['notch']
        self.pos = 0

    def set_start(self, letter):
        self.pos = ALPHABET.find(letter)

    def forward(self, input):
        output = (input+self.pos) % 26
        cipherletter = self.output[output]
        print('->', cipherletter, '(forward through rotor {})'.format(self.name))
        output = (ALPHABET.find(cipherletter)-self.pos) % 26
        return output

    def backward(self, input):
        output = (input+self.pos) % 26
        output = self.output.find(ALPHABET[output])
        cipherletter = ALPHABET[output]
        print('->', cipherletter, '(backwards through rotor {})'.format(self.name))
        output = (output-self.pos) % 26
        return output

    def current_letter_setting(self):
        return ALPHABET[self.pos]

    def step(self):
        turnover = (self.current_letter_setting() == self.notch)
        self.pos = (self.pos+1) % 26
        return turnover
