from enigma import ALPHABET, Enigma
import random
from menu_generator import MenuGenerator

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

print()
print()
print('****************')
print('ENIGMA SIMULATOR')
print('****************')

print()
print()
print('Please enter the plaintext you want to encipher')
print('-----------------------------------------------')

plain = input().replace(' ', '').upper()

rotors = random.sample(['I', 'II', 'III', 'IV', 'V'], k=3)
starting_letters = random.choices(list(ALPHABET), k=3)
ring_settings = random.choices(list(str(k) for k in range(1, 27)), k=3)
reflector = random.sample(['A', 'B', 'C'], k=1)[0]
a_copy = list(ALPHABET)[:]
random.shuffle(a_copy)
steckers = [''.join(a_copy[i*2: (i+1)*2])
            for i in range(random.randint(5, 10))]

enigma = Enigma(
    False,
    False,
    True,
    rotors,
    starting_letters,
    ring_settings,
    'B',
    steckers
)

print()
print()
print('Enigma Starting Settings:')
print('*************************')
print('Rotors Selected:', enigma.l_rotor.name,
      enigma.m_rotor.name, enigma.r_rotor.name)
print('Rotor Setting:', enigma.l_rotor.current_letter_setting(),
      enigma.m_rotor.current_letter_setting(), enigma.r_rotor.current_letter_setting())
print('Rotor Ring Settings:', enigma.l_rotor.ring_setting,
      enigma.m_rotor.ring_setting, enigma.r_rotor.ring_setting)
print('Reflector Selected:', enigma.reflector.name)
print('Swapped Letters:', steckers)
print('*************************')

cipher = enigma.encrypt(plain)

print()
print('*************************')
print('Plaintext:', plain)
print('Ciphertext:', cipher)
print('*************************')
print()

mg = MenuGenerator(plain, cipher, 'ZZZ')
