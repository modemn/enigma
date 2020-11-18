from enigma import Enigma


class Bombe():
    def __init__(self, t_rotor, m_rotor, b_rotor, reflector, scrambler_settings, connections, input):
        # Scramblers
        # Types top to bottom
        # Reflector type
        # Menu Settings
        # Scrambler starting letters
        # Which letters the ends connect to on the diagonal board
        # Input letter
        # Indicator scrambler, this could be an enigma

        # Initialize all 12 scramblers with the settings
        self.scramblers = []
        for i in range(12):
            self.scramblers.append(
                Enigma(False, False, False, [str(b_rotor), str(m_rotor), str(
                    t_rotor)], list(scrambler_settings[i]), ['1', '1', '1'], reflector, [])
            )

            print(self.scramblers[i].toString())

    def run(self):
        output = self.input
        for scrambler in self.scramblers:
            output =


b = Bombe(
    'II',
    'V',
    'III',
    'B',
    ['ZZK', 'ZZE', 'ZZF', 'ZZN', 'ZZM', 'ZZG',
        'ZZP', 'ZZB', 'ZZJ', 'ZZI', 'ZZL', 'ZZO'],
    ['UE', 'EG', 'GR', 'RA', 'AS', 'SV', 'VE', 'EN', 'HZ', 'ZR', 'RG', 'GL'],
    'G'
)
