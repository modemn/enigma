ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Plugboard():
    def __init__(self):
        self.output = ALPHABET

    def set_swap(self, letter_1, letter_2):
        index_1 = ALPHABET.find(letter_1)
        index_2 = ALPHABET.find(letter_2)
        output_list = list(self.output)
        output_list[index_1], output_list[index_2] = output_list[index_2], output_list[index_1]
        self.output = "".join(output_list)
        print(self.output)

    def swap(self, input):
        index = ALPHABET.find(input)
        cipherletter = self.output[index]
        print('->', cipherletter, '(Through pluboard)')
        output = ALPHABET.find(cipherletter)
        return output