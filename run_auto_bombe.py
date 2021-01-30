import sys
import csv
from pprint import pprint
from bombe_2 import Bombe
from menu_generator import MenuGenerator

top_rotor = sys.argv[1]
middle_rotor = sys.argv[2]
bottom_rotor = sys.argv[3]

assert top_rotor in ['I', 'II', 'III', 'IV',
                     'V'], "That rotor does not exist or currently isnt available as an option, please pick from {'I', 'II', 'III', 'IV', 'V'}"
assert middle_rotor in ['I', 'II', 'III', 'IV',
                        'V'], "That rotor does not exist or currently isnt available as an option, please pick from {'I', 'II', 'III', 'IV', 'V'}"
assert bottom_rotor in ['I', 'II', 'III', 'IV',
                        'V'], "That rotor does not exist or currently isnt available as an option, please pick from {'I', 'II', 'III', 'IV', 'V'}"

reflector = sys.argv[4].upper()

assert reflector in [
    'A', 'B', 'C'], "That reflector does not exist or currently isnt available as an option, please pick from {'A', 'B', C}"

plain_crib = sys.argv[5].replace(' ', '').upper()
cipher_crib = sys.argv[6].replace(' ', '').upper()

assert len(plain_crib) == len(
    cipher_crib), 'The cipher and plain cribs should be of the same length'

starting_letters = sys.argv[7].upper()

assert len(starting_letters) == 3, 'There should be 3 starting letters!'

mg = MenuGenerator(plain_crib, cipher_crib, starting_letters)
settings, connections, input_letter, num_closures = mg.get_bombe_settings()

with open('bombe_output.csv', 'w', newline='') as file:
    wr = csv.writer(file)
    wr.writerow([
        top_rotor,
        middle_rotor,
        bottom_rotor,
        reflector,
        plain_crib,
        cipher_crib,
        starting_letters,
        input_letter
    ])
    wr.writerow([])
    wr.writerows(list(zip(settings, connections)))
    wr.writerow([])
    wr.writerow([f'Number of closures in the settings: {num_closures}'])
    wr.writerow([])


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
    input_letter
)

print('RUNNING...')
b.auto_run()
