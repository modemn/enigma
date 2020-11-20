from enigma import ALPHABET, Enigma
from pprint import pprint

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Bombe():
    def __init__(self, t_rotor, m_rotor, b_rotor, reflector, scrambler_settings, connections, input):

        self.connections = connections

        self.input = input

        # Initialize as many scramblers as settings are provided
        self.scramblers = []
        for i in range(len(scrambler_settings)):
            self.scramblers.append(
                Enigma(
                    False,
                    False,
                    False,
                    [str(b_rotor), str(m_rotor), str(t_rotor)],
                    list(scrambler_settings[i])[::-1],
                    ['1', '1', '1'],
                    reflector,
                    []
                )
            )
        self.num_scramblers = len(self.scramblers)

        self.steckers = {}
        for connection in connections:
            self.steckers[connection[0]] = ''

        self.path = list(self.steckers.keys())

        # print(self.scramblers[i].to_string())

        # TODO: Make an indicator component for displaying the possible ring settings
        # Indicator scrambler that shows the possible ring settings when a stop occurs
        # self.indicator = Enigma(
        #     False,
        #     False,
        #     False,
        #     [str(b_rotor), str(m_rotor), str(t_rotor)],
        #     ['Z', 'Z', 'Z'],
        #     ['1', '1', '1'],
        #     reflector,
        #     []
        # )

    # Run through the scrmablers in order and print output at each stage
    def run(self):
        i = 0
        # i = 17575 # <- For testing
        stop = False
        while ((i < 17576) and (not stop)):
            # output = self.input
            # input_pos = ALPHABET.find(self.input)

            output = ALPHABET
            all_outputs = [ALPHABET]
            for scrambler in self.scramblers:
                output = scrambler.encrypt(output)
                all_outputs.append(output)

            top_row = ''
            middle_row = ''
            bottom_row = ''

            for scrambler in self.scramblers:
                top_row += str(scrambler.r_rotor.current_letter_setting())
                middle_row += str(scrambler.m_rotor.current_letter_setting())
                bottom_row += str(scrambler.l_rotor.current_letter_setting())

            print()
            print('Scrambler settings:')
            print(top_row)
            print(middle_row)
            print(bottom_row)
            # TODO: print the current ring settings as well
            print()

            # consistent_letters = []
            # for letter in self.steckers:
            #     idx = ALPHABET.find(letter)
            #     if (ALPHABET[idx] == output[idx]):
            #         consistent_letters.append(idx)

            # Check if there are any letters that don't change after going
            # through all the scramblers
            consistent_letters = []
            for j in range(26):
                if(ALPHABET[j] == output[j]):
                    consistent_letters.append(j)

            # Check if the input letter is unchanged
            # if (output.find(self.input) == input_pos):

            # If consistent letters were found then a stop has occurred
            if(len(consistent_letters)):
                print('STOP!')
                print()

                # TODO: go through all the consistent letters, not just the first one found

                # Create dictionary with all the steckers given by the stop
                for j in range(len(all_outputs)):
                    self.steckers[self.path[j % self.num_scramblers]
                                  ] = all_outputs[j][consistent_letters[0]]

                # Go through the steckers and check for contradictions
                consistent_steckers = True
                for j in self.steckers:
                    val = self.steckers[j]
                    if (val in self.steckers.keys()):
                        if (self.steckers[val] != j):
                            consistent_steckers = False

                # If no contradictions are found, then print out the stop
                if (consistent_steckers):
                    stop = True
                    print(ALPHABET[consistent_letters[0]])
                    for o in all_outputs:
                        print(o)
                    print()
                    print('Possible steckers:')
                    for stecker in self.steckers:
                        print(stecker, '<->', self.steckers[stecker])
                    # TODO: print the possible ring settings from the indicator component
                    input()

                # If not, then step all scramblers
                # else:
                print('Contradiction found, continuing search')
                print('Step rotors')
                for scrambler in self.scramblers:
                    scrambler.step_rotors(False)
                stop = False

            # If not, then all step all scramblers
            else:
                print('Step rotors')

                top_row = ''
                middle_row = ''
                bottom_row = ''

                for scrambler in self.scramblers:
                    top_row += str(scrambler.r_rotor.current_letter_setting())
                    middle_row += str(scrambler.m_rotor.current_letter_setting())
                    bottom_row += str(scrambler.l_rotor.current_letter_setting())
                    scrambler.step_rotors(False)

                print(top_row)
                print(middle_row)
                print(bottom_row)

                # self.indicator.step_rotors()
                # print(self.indicator.r_rotor.current_letter_setting(
                # ), self.indicator.m_rotor.current_letter_setting(), self.indicator.l_rotor.current_letter_setting())

            i += 1


Bombe(
    'II',
    'V',
    'III',
    'B',
    ['ZZE', 'ZZF', 'ZZN', 'ZZM', 'ZZG',
        'ZZP'],
    ['EG', 'GR', 'RA', 'AS', 'SV', 'VE'],
    'A'
).run()
