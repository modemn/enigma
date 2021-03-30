from bombe_2 import Bombe

b = Bombe(
    'II',  # TOP / LEFT ROTOR
    'V',  # MIDDLE ROTOR
    'III',  # BOTTOM / RIGHT ROTOR
    'ZZZ',
    'B',  # REFLECTOR
    ['ZZK', 'ZZE', 'ZZF', 'ZZN', 'ZZM', 'ZZG',
        'ZZP', 'ZZB', 'ZZJ', 'ZZI', 'ZZL', 'ZZO'],  # SCRAMBLER SETTINGS
    ['UE', 'EG', 'GR', 'RA', 'AS', 'SV', 'VE', 'EN',
        'HZ', 'ZR', 'RG', 'GL'],  # CONNECTIONS
    'E',  # INPUT LETTER
    False,  # PRINTING
    True,  # OUTPUTTING TO A FILE
)

b.run()
