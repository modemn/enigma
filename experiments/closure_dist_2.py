import sys
import random
import networkx as nx
import csv
import matplotlib.pyplot as plt
import numpy as np
from enigma import Enigma

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

LOREM = 'LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELITSEDDOEIUSMODTEMPORINCIDIDUNTUTLABOREETDOLOREMAGNAALIQUAUTENIMADMINIMVENIAMQUISNOSTRUDEXERCITATIONULLAMCOLABORISNISIUTALIQUIPEXEACOMMODOCONSEQUATDUISAUTEIRUREDOLORINREPREHENDERITINVOLUPTATEVELITESSECILLUMDOLOREEUFUGIATNULLAPARIATUREXCEPTEURSINTOCCAECATCUPIDATATNONPROIDENTSUNTINCULPAQUIOFFICIADESERUNTMOLLITANIMIDESTLABORUM'


def get_random_enigma(crib_length):
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
        reflector,
        steckers
    )

    with open('criblen_{}.csv'.format(crib_length), 'w', newline='') as file:
        wr = csv.writer(file)
        row = [
            enigma.l_rotor.name,
            enigma.m_rotor.name,
            enigma.r_rotor.name,
            enigma.l_rotor.current_letter_setting(),
            enigma.m_rotor.current_letter_setting(),
            enigma.r_rotor.current_letter_setting(),
            enigma.l_rotor.ring_setting,
            enigma.m_rotor.ring_setting,
            enigma.r_rotor.ring_setting,
            enigma.reflector.name,
            ', '.join(steckers)
        ]

        wr.writerow(row)

    return enigma


def get_closures(graph):
    closures = []
    g = nx.DiGraph(graph)

    res = list(nx.simple_cycles(g))

    for cl in res:
        if len(cl) > 2:
            if (set(''.join(cl)) not in [set(x) for x in closures]):
                closures.append(cl)

    return closures


max_crib_length = int(sys.argv[1])
num_iterations = int(sys.argv[2])
bar_offset = 0
bar_width = 0.1

for crib_length in range(5, max_crib_length+1, 5):
    enigma = get_random_enigma(crib_length)

    encrypted_lorem = enigma.encrypt(LOREM)

    closure_lengths = []
    for _ in range(num_iterations):
        idx = random.randint(0, len(LOREM))
        plain_crib = LOREM[idx:idx+crib_length]
        cipher_crib = encrypted_lorem[idx:idx+crib_length]

        menu = {}
        for i in range(len(plain_crib)):
            if (plain_crib[i] in menu.keys()):
                menu[plain_crib[i]].append(cipher_crib[i])
            else:
                menu[plain_crib[i]] = [cipher_crib[i]]

            if (cipher_crib[i] in menu.keys()):
                menu[cipher_crib[i]].append(plain_crib[i])
            else:
                menu[cipher_crib[i]] = [plain_crib[i]]

        closures = get_closures(menu)
        closure_lengths.append(len(closures))

        with open('criblen_{}.csv'.format(crib_length), 'a', newline='') as file:
            wr = csv.writer(file)
            row = [plain_crib, cipher_crib, len(closures)]
            wr.writerow(row)

    with open('criblen_{}.csv'.format(crib_length), 'a', newline='') as file:
        wr = csv.writer(file)
        wr.writerow(closure_lengths)

    closure_lengths = dict((x, closure_lengths.count(x))
                           for x in set(closure_lengths))

    x_data = np.array(list(closure_lengths.keys()))
    y_data = list(closure_lengths.values())
    y_data = [y/num_iterations for y in y_data]

    plt.bar(x_data + bar_offset, y_data, label='Crib length {}'.format(
        str(crib_length)), width=bar_width)

    bar_offset += bar_width

plt.legend()
plt.xlabel('Number of closures in the menu')
plt.ylabel('Normalized Rate of occurrance')
plt.xticks(np.arange(max(x_data)+1) + bar_width, np.arange(max(x_data)+1))
plt.show()
