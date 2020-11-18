from enigma import ALPHABET, Enigma

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

            # print(self.scramblers[i].to_string())

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
        # i = 17575
        stop = False
        while ((i < 17576) and (not stop)):
            output = self.input
            input_pos = ALPHABET.find(self.input)
            print(output)
            for scrambler in self.scramblers:
                output = scrambler.encrypt(output)
                print(output)

            # Check if the input letter is unchanged
            if (output.find(self.input) == input_pos):
                print('Stop occurred!')
                top_row = ''
                middle_row = ''
                bottom_row = ''

                for scrambler in self.scramblers:
                    top_row += str(scrambler.r_rotor.current_letter_setting())
                    middle_row += str(scrambler.m_rotor.current_letter_setting())
                    bottom_row += str(scrambler.l_rotor.current_letter_setting())

                print(top_row)
                print(middle_row)
                print(bottom_row)
                stop = True
                input()
                for scrambler in self.scramblers:
                    scrambler.step_rotors(False)
                stop = False
            # If not, then all scramblers (including the indicator scrambler)
            # should step one letter
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


b = Bombe(
    'II',
    'V',
    'III',
    'B',
    ['ZZE', 'ZZF', 'ZZN', 'ZZM', 'ZZG',
        'ZZP'],
    ['UE', 'EG', 'GR', 'RA', 'AS', 'SV', 'VE', 'EN', 'HZ', 'ZR', 'RG', 'GL'],
    'A'
).run()
