reflector_dict = {
    'A': {'name': 'A',
          'output': 'EJMZALYXVBWFCRQUONTSPIKHGD'},
    'B': {'name': 'B',
          'output': 'YRUHQSLDPXNGOKMIEBFZCWVJAT'},
    'C': {'name': 'C',
          'output': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
}

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_reflector_choices():
    return list(reflector_dict.keys())


class Reflector:
    def __init__(self, model, printing):
        self.name = reflector_dict[model]['name']
        self.output = reflector_dict[model]['output']
        self.printing = printing

    def reflect(self, input):
        cipherletter = self.output[input]
        if (self.printing):
            print('->', cipherletter, '(reflector {})'.format(self.name))
        output = ALPHABET.find(cipherletter)
        return output
