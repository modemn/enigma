import sys
from enigma import Enigma
import ast

filename = sys.argv[1:][0]

with open(filename, 'r') as reader:
    lines = reader.readlines()
    opts = []
    for line in lines:
        opts.append(line[line.find(':')+1:-1])

stepping_enabled = ast.literal_eval(opts[0])
rotors = ast.literal_eval(opts[1])
rotor_settings = ast.literal_eval(opts[2])
ring_settings = ast.literal_eval(opts[3])
reflector = opts[4]
plugboard = ast.literal_eval(opts[5])
plaintext = opts[6]

enigma = Enigma(
    False,
    False,
    stepping_enabled,
    rotors,
    rotor_settings,
    ring_settings,
    reflector,
    plugboard
)

ciphertext = enigma.encrypt(plaintext)
print(plaintext, '->', ciphertext)
print()
