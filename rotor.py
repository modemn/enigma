rotor_dict = {
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
    return list(rotor_dict.keys())


class Rotor:
    def __init__(self, model) -> None:
        self.name = rotor_dict[model]['name']
        self.output = rotor_dict[model]['output']
        self.notch = rotor_dict[model]['notch']

    def forward(self, input):
        index = ALPHABET.find(input)
        output = self.output[index]
        return output

    def backward(self, input):
        index = self.output.find(input)
        output = ALPHABET[index]
        return output
