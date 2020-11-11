ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Plugboard():
    def __init__(self, printing, letter_swaps):
        self.output = ALPHABET
        self.printing = printing
        if (len(letter_swaps) != 0):
            for letter_swap in letter_swaps:
                self.set_swap(letter_swap[0], letter_swap[1])

    def set_swap(self, letter_1, letter_2):
        index_1 = ALPHABET.find(letter_1)
        index_2 = ALPHABET.find(letter_2)
        output_list = list(self.output)
        output_list[index_1], output_list[index_2] = output_list[index_2], output_list[index_1]
        self.output = "".join(output_list)

    def swap(self, input):
        index = ALPHABET.find(input)
        cipherletter = self.output[index]
        if (self.printing):
            print('->', cipherletter, '(Through pluboard)')
        output = ALPHABET.find(cipherletter)
        return output
