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
        self.printing_enabled = printing
        self.pos = ALPHABET.find(start_letter)

        # Creating the new output alphabet given the ring settings
        self.ring_setting = ring_setting+1
        if (ring_setting != 0):
            dot_pos = self.output.find('A')
            new_wiring = ''
            for char in self.output:
                new_wiring += ALPHABET[(ALPHABET.find(char)+ring_setting) % 26]
            new_dot_pos = (dot_pos + ring_setting) % 26

            while not new_wiring[new_dot_pos] == ALPHABET[ring_setting]:
                new_wiring = new_wiring[-1:] + new_wiring[:-1]

            self.output = new_wiring

    def forward(self, input):
        output = (input+self.pos) % 26
        cipherletter = self.output[output]
        if(self.printing_enabled):
            print('->', cipherletter, '(forward through rotor {})'.format(self.name))
        output = (ALPHABET.find(cipherletter)-self.pos) % 26
        return output

    def backward(self, input):
        output = (input+self.pos) % 26
        output = self.output.find(ALPHABET[output])
        cipherletter = ALPHABET[output]
        if(self.printing_enabled):
            print('->', cipherletter,
                  '(backwards through rotor {})'.format(self.name))
        output = (output-self.pos) % 26
        return output

    def current_letter_setting(self):
        return ALPHABET[self.pos]

    def step(self):
        if(self.printing_enabled):
            print("Stepping rotor", self.name)
        self.pos = (self.pos+1) % 26
