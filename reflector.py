reflector_dict = {
    'B': {'name': 'UKW-B',
          'output': 'YRUHQSLDPXNGOKMIEBFZCWVJAT'},
    'C': {'name': 'UKW-C',
          'output': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
}

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_reflector_choices():
    return list(reflector_dict.keys())


class Reflector:
    def __init__(self, model):
        self.name = reflector_dict[model]['name']
        self.output = reflector_dict[model]['output']

    def reflect(self, input):
        cipherletter = self.output[input]
        print('->', cipherletter, '(reflector {})'.format(self.name))
        output = ALPHABET.find(cipherletter)
        return output
