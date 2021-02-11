import sys
from bombe_2 import Bombe
from menu_generator_1 import MenuGenerator
from pprint import pprint
from timer import Timer

ROTORS = ['I', 'II', 'III', 'IV', 'V']
REFLECTORS = ['A', 'B', 'C']

plain_crib = sys.argv[1].replace(' ', '').upper()
cipher_crib = sys.argv[2].replace(' ', '').upper()

assert len(plain_crib) == len(
    cipher_crib), 'The cipher and plain cribs should be of the same length'

starting_letters = sys.argv[3].upper()

assert len(starting_letters) == 3, 'There should be 3 starting letters!'

printing = bool(sys.argv[4])

mg = MenuGenerator(plain_crib, cipher_crib, starting_letters)
settings, connections, input_letter, num_closures = mg.get_bombe_settings()


rotor_combos = [(x, y, z)
                for x in ROTORS for y in ROTORS for z in ROTORS if x != y if y != z if x != z]

timer = Timer()
timer.start()

for top_rotor, middle_rotor, bottom_rotor in rotor_combos:
    for reflector in REFLECTORS:
        print('******************BOMBE******************')
        print('Running the Bombe with the following settings:')
        print('Rotors:', top_rotor, middle_rotor, bottom_rotor)
        print('Starting Letters:', starting_letters)
        pprint(list(zip(settings, connections)))
        print('Input Letter:', input_letter)
        print('*****************************************')
        print()
        print("Press return to start the Bombe")
        input()

        b = Bombe(
            top_rotor,
            middle_rotor,
            bottom_rotor,
            starting_letters,
            reflector,
            settings,
            connections,
            input_letter,
            True
        )

        print('RUNNING...')
        b.auto_run(plain_crib, cipher_crib)

print(timer.stop())
