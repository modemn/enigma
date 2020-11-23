from enigma import Enigma
from indicator import Indicator
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

        # Indicator scrambler that shows the possible ring settings when a stop occurs
        self.indicator = Indicator(['Z', 'Z', 'Z'])

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

            top_row += ' '+str(self.indicator.t_rotor.current_letter())
            middle_row += ' '+str(self.indicator.m_rotor.current_letter())
            bottom_row += ' '+str(self.indicator.b_rotor.current_letter())

            print(i, '----------------------------------')
            print('Scrambler settings:')
            print(top_row)
            print(middle_row)
            print(bottom_row)
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
                print('STOP!', len(consistent_letters),
                      'letter(s) did not change after scrambling')
                print()

                for cl in consistent_letters:
                    # Create dictionary with all the steckers given by the stop
                    for j in range(len(all_outputs)):
                        self.steckers[self.path[j % self.num_scramblers]
                                      ] = all_outputs[j][cl]

                    # Go through the steckers and check for contradictions
                    consistent_steckers = True
                    for j in self.steckers:
                        val = self.steckers[j]
                        if (val in self.steckers.keys()):
                            if (self.steckers[val] != j):
                                consistent_steckers = False

                    # If no contradictions are found, then print out the stop
                    # and continue search after the user inputs
                    if (consistent_steckers):
                        stop = True
                        print(ALPHABET[cl], 'stays consistent')
                        for o in all_outputs:
                            print(o)
                        print()
                        print('##################################')
                        print('Possible steckers:')
                        for stecker in self.steckers:
                            print(stecker, '<->', self.steckers[stecker])
                        print()
                        print('Possible ring settings:')
                        print(
                            self.indicator.b_rotor.current_letter(),
                            self.indicator.m_rotor.current_letter(),
                            self.indicator.t_rotor.current_letter()
                        )
                        print('##################################')
                        input()
                        print('Continuing search')
                        print()

                        for scrambler in self.scramblers:
                            scrambler.step_rotors(False)
                        self.indicator.step_rotors()
                        stop = False

                    # If not, then step all scramblers
                    else:
                        print('//////////////////////////////////////')
                        print('Contradiction found, continuing search')
                        print('//////////////////////////////////////')
                        print()
                        for scrambler in self.scramblers:
                            scrambler.step_rotors(False)
                        self.indicator.step_rotors()
                        stop = False

            # If not, then step all scramblers
            else:
                for scrambler in self.scramblers:
                    scrambler.step_rotors(False)
                self.indicator.step_rotors()

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
