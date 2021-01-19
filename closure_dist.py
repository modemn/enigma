import sys
import random
from pprint import pprint
from enigma import Enigma

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

LOREM = 'LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELITSEDDOEIUSMODTEMPORINCIDIDUNTUTLABOREETDOLOREMAGNAALIQUAUTENIMADMINIMVENIAMQUISNOSTRUDEXERCITATIONULLAMCOLABORISNISIUTALIQUIPEXEACOMMODOCONSEQUATDUISAUTEIRUREDOLORINREPREHENDERITINVOLUPTATEVELITESSECILLUMDOLOREEUFUGIATNULLAPARIATUREXCEPTEURSINTOCCAECATCUPIDATATNONPROIDENTSUNTINCULPAQUIOFFICIADESERUNTMOLLITANIMIDESTLABORUM'


def get_random_enigma():
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


def find_closures_util(graph, v, visited, parent):
    visited[v] = True

    for neighbour in graph[v]:
        if visited[neighbour] == False:
            res = find_closures_util(graph, neighbour, visited, v)
            if res != '!':
                if (len(set(res)) != len(res)):
                    return res
                else:
                    return v+res
        elif neighbour != parent:
            return v+neighbour
    return '!'


def find_closures(graph):
    visited = {}
    # visited = dict.fromkeys(visited, False)
    for i in graph.keys():
        visited[i] = False
    closures = []

    for i in graph:
        res = find_closures_util(graph, i, visited, -1)
        if res != '!':
            if set(res) not in [set(cl) for cl in closures]:
                closures.append(res)
        for i in graph.keys():
            visited[i] = False

    return closures

# crib_length = int(sys.argv[1])
# num_repeats = int(sys.argv[2])


crib_length = 10
num_repeats = 50

enigma = get_random_enigma()

encrypted_lorem = enigma.encrypt(LOREM)

# print(LOREM)
# print()
# print(encrypted_lorem)

plain_and_cipher_cribs = get_cribs(50, crib_length, encrypted_lorem)
# pprint(plain_and_cipher_cribs)

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

    menu = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C'],
        'C': ['A', 'B'],
        'D': ['A', 'E'],
        'E': ['D', 'F', 'H'],
        'F': ['E', 'G'],
        'G': ['F', 'H'],
        'H': ['E', 'G']
    }
    pprint(menu)

    closures = find_closures(menu)
    print(closures)

    # input()
