from menu_generator import MenuGenerator
from bombe_2 import Bombe
from enigma import Enigma
import random
import sys
import networkx as nx

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

PLAINTEXT = 'INVORAUSSICHTDASSICHUBERKURZEMMITDERSCHWERSTENFORDERUNGANDIEMENSCHHEITHERANTRETENMUSSDIEJEANSIEGESTELLTWURDESCHEINTESMIRUNERLASSLICHZUSAGENWERICHBINIMGRUNDEDURFTEMANSWISSENDENNICHHABEMICHNICHTUNBEZEUGTGELASSENDASMISSVERHALTNISSABERZWISCHENDERGROSSEMEINERAUFGABEUNDDERKLEINHEITMEINERZEITGENOSSENISTDARINZUMAUSDRUCKGEKOMMENDASSMANMICHWEDERGEHORTNOCHAUCHNURGESEHNHATICHLEBEAUFMEINENEIGNENCREDITHINESISTVIELLEICHTBLOSSEINVORURTHEILDASSICHLEBEICHBRAUCHENURIRGENDEINENGEBILDETENZUSPRECHENDERIMSOMMERINSOBERENGADINKOMMTUMMICHZUUBERZEUGENDASSICHNICHTLEBEUNTERDIESENUMSTANDENGIEBTESEINEPFLICHTGEGENDIEIMGRUNDEMEINEGEWOHNHEITNOCHMEHRDERSTOLZMEINERINSTINKTEREVOLTIRTNAMLICHZUSAGENHORTMICHDENNICHBINDERUNDDERVERWECHSELTMICHVORALLEMNICHT'


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

    # with open('test{}.txt'.format(str(x+1)), 'w', newline='') as file:
    #     file.write(
    #         str(
    #             str(enigma.l_rotor.name) + ' ' +
    #             str(enigma.m_rotor.name) + ' ' +
    #             str(enigma.r_rotor.name) + '\n' +
    #             str(enigma.l_rotor.current_letter_setting()) + ' ' +
    #             str(enigma.m_rotor.current_letter_setting()) + ' ' +
    #             str(enigma.r_rotor.current_letter_setting()) + '\n' +
    #             str(enigma.l_rotor.ring_setting) + ' ' +
    #             str(enigma.m_rotor.ring_setting) + ' ' +
    #             str(enigma.r_rotor.ring_setting) + '\n' +
    #             str(enigma.reflector.name) + '\n' +
    #             ' '.join(steckers) + '\n'
    #         )
    #     )

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


def make_menu(plain_crib, cipher_crib):
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

    return menu


crib_len = sys.argv[1]


random_enigma = get_random_enigma()
ciphertext = random_enigma.encrypt(PLAINTEXT)

for i in range(len(PLAINTEXT)):
    plain_crib = PLAINTEXT[i:i+crib_len]
    cipher_crib = ciphertext[i:i+crib_len]
    menu = make_menu(plain_crib, cipher_crib)
    closures = get_closures(menu)

    if len(closures) == 1:
        mg = MenuGenerator(plain_crib, cipher_crib, 'ZZZ')
        settings, connections, input_letter, _ = mg.get_bombe_settings()

        bombe = Bombe(
            random_enigma.l_rotor.name,
            random_enigma.m_rotor.name,
            random_enigma.r_rotor.name,
            'ZZZ',
            random_enigma.reflector.name,
            settings,
            connections,
            input_letter
        )
