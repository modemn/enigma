import sys
import random
import networkx as nx
import csv
import matplotlib.pyplot as plt
from pprint import pprint
from enigma import Enigma

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

LOREM = 'LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELITSEDDOEIUSMODTEMPORINCIDIDUNTUTLABOREETDOLOREMAGNAALIQUAUTENIMADMINIMVENIAMQUISNOSTRUDEXERCITATIONULLAMCOLABORISNISIUTALIQUIPEXEACOMMODOCONSEQUATDUISAUTEIRUREDOLORINREPREHENDERITINVOLUPTATEVELITESSECILLUMDOLOREEUFUGIATNULLAPARIATUREXCEPTEURSINTOCCAECATCUPIDATATNONPROIDENTSUNTINCULPAQUIOFFICIADESERUNTMOLLITANIMIDESTLABORUM'


def get_random_enigma(num_repeats, crib_length):
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

    with open('{}_{}.csv'.format(num_repeats, crib_length), 'w', newline='') as file:
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


def get_cribs(num_cribs, crib_len, encrypted_text):
    cribs = {}
    while len(cribs) != num_cribs:
        idx = random.randint(0, len(LOREM))
        if (idx+crib_len < len(LOREM)):
            crib = LOREM[idx:idx+crib_len]
            if (crib not in cribs.keys()):
                cribs[crib] = encrypted_text[idx:idx+crib_len]
        else:
            continue
    return cribs


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
num_repeats = int(sys.argv[2])

for crib_length in range(10, max_crib_length+1):
    enigma = get_random_enigma(num_repeats, crib_length)

    encrypted_lorem = enigma.encrypt(LOREM)

    # print(LOREM)
    # print()
    # print(encrypted_lorem)

    plain_and_cipher_cribs = get_cribs(
        num_repeats, crib_length, encrypted_lorem)
    # pprint(plain_and_cipher_cribs)

    closure_lengths = []

    for plain_crib in plain_and_cipher_cribs:
        cipher_crib = plain_and_cipher_cribs[plain_crib]
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

        # print(plain_crib)
        # print(cipher_crib)

        # menu = {
        #     'A': ['B', 'C', 'D'],
        #     'B': ['A', 'C'],
        #     'C': ['A', 'B'],
        #     'D': ['A', 'E'],
        #     'E': ['D', 'F', 'H'],
        #     'F': ['E', 'G'],
        #     'G': ['F', 'H'],
        #     'H': ['E', 'G']
        # }
        # pprint(menu)

        closures = get_closures(menu)
        closure_lengths.append(len(closures))

        pprint(closures)

        with open('{}_{}.csv'.format(num_repeats, crib_length), 'a', newline='') as file:
            wr = csv.writer(file)
            row = [plain_crib, cipher_crib, len(closures)]
            wr.writerow(row)

    with open('{}_{}.csv'.format(num_repeats, crib_length), 'a', newline='') as file:
        wr = csv.writer(file)
        wr.writerow(closure_lengths)

    closure_lengths = dict((x, closure_lengths.count(x))
                           for x in set(closure_lengths))

    x_data = list(closure_lengths.keys())
    y_data = list(closure_lengths.values())

    plt.plot(x_data, y_data, label='Crib length {}'.format(str(crib_length)))
    # plt.xticks(x_data, tuple(x_data))

plt.legend()
plt.show()
