import sys
import random
import networkx as nx
# import csv
import matplotlib.pyplot as plt
import numpy as np
from enigma import Enigma
from pprint import pprint

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

LOREMS = [
    ('Joe Biden Inauguration Speech', 'THISISAMERICASDAYTHISISDEMOCRACYSDAYADAYOFHISTORYANDHOPEOFRENEWALANDRESOLVETHROUGHACRUCIBLEFORTHEAGESAMERICAHASBEENTESTEDANEWANDAMERICAHASRISENTOTHECHALLENGETODAYWECELEBRATETHETRIUMPHNOTOFACANDIDATEBUTOFACAUSEACAUSEOFDEMOCRACYTHEPEOPLETHEWILLOFTHEPEOPLEHASBEENHEARDANDTHEWILLOFTHEPEOPLEHASBEENHEEDEDWEVELEARNEDAGAINTHATDEMOCRACYISPRECIOUSDEMOCRACYISFRAGILEANDATTHISHOURMYFRIENDSDEMOCRACYHASPREVAILEDSONOWONTHISHALLOWEDGROUNDWHEREJUSTAFEWDAYSAGOVIOLENCESOUGHTTOSHAKETHECAPITOLSVERYFOUNDATIONSWECOMETOGETHERASONENATIONUNDERGODINDIVISIBLETOCARRYOUTTHEPEACEFULTRANSFEROFPOWERASWEHAVEFORMORETHANTWOCENTURIESASWELOOKAHEADINOURUNIQUELYAMERICANWAYRESTLESSBOLDOPTIMISTICANDSETOURSIGHTSONANATIONWEKNOWWECANBEANDMUSTBEITHANKMYPREDECESSORSOFBOTHPARTIESFORTHEIRPRESENCEHEREITHANKTHEMFROMTHEBOTTOMOFMYHEARTANDIKNOWTHERESILIENCEOFOURCONSTITUTIONANDTHESTRENGTHTHESTRENGTHOFOURNATIONASDOESPRESIDENTCARTERWHOISPOKEWITHLASTNIGHTWHOCANNOTBEWITHUSTODAYBUTWHOWESALUTEFORHISLIFETIMEOFSERVICE'),
    ('Nietzsche Ecce Homo Preface 1', 'INVORAUSSICHTDASSICHUBERKURZEMMITDERSCHWERSTENFORDERUNGANDIEMENSCHHEITHERANTRETENMUSSDIEJEANSIEGESTELLTWURDESCHEINTESMIRUNERLASSLICHZUSAGENWERICHBINIMGRUNDEDURFTEMANSWISSENDENNICHHABEMICHNICHTUNBEZEUGTGELASSENDASMISSVERHALTNISSABERZWISCHENDERGROSSEMEINERAUFGABEUNDDERKLEINHEITMEINERZEITGENOSSENISTDARINZUMAUSDRUCKGEKOMMENDASSMANMICHWEDERGEHORTNOCHAUCHNURGESEHNHATICHLEBEAUFMEINENEIGNENCREDITHINESISTVIELLEICHTBLOSSEINVORURTHEILDASSICHLEBEICHBRAUCHENURIRGENDEINENGEBILDETENZUSPRECHENDERIMSOMMERINSOBERENGADINKOMMTUMMICHZUUBERZEUGENDASSICHNICHTLEBEUNTERDIESENUMSTANDENGIEBTESEINEPFLICHTGEGENDIEIMGRUNDEMEINEGEWOHNHEITNOCHMEHRDERSTOLZMEINERINSTINKTEREVOLTIRTNAMLICHZUSAGENHORTMICHDENNICHBINDERUNDDERVERWECHSELTMICHVORALLEMNICHT'),
    ('Real Enigma Message', 'TAETIGKEITSBERIQTVOMXSEQSXDREIXVIERNULLXSONDERANLAGEXZWOXSXITEXZWOXLGXKDOXROEMDREIXXNULLXSTRIQXNULLXSEITEXDREIXLGXKDOXROEMXDREIXNULLXSTRIQXZWOXLGXKDOXROEMXDREIBKRKRALLEXXFOLGENDESISTSOFORTBEKANNTZUGEBENXXICHHABEFOLGELNBEBEFEHLERHALTENXXJANSTERLEDESBISHERIGXNREICHSMARSCHALLSJGOERINGJSETZTDERFUEHRERSIEYHVRRGRZSSADMIRALYALSSEINENNACHFOLGEREINXSCHRIFTLSCHEVOLLMACHTUNTERWEGSXABSOFORTSOLLENSIESAEMTLICHEMASSNAHMENVERFUEGENYDIESICHAUSDERGEGENWAERTIGENLAGEERGEBENXGEZXREICHSLEITEIKKTULPEKKJBORMANNJXXOBXDXMMMDURNHFKSTXKOMXADMXUUUBOOIEXKP')
]


def get_random_enigma(i):
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

    with open('test{}.txt'.format(str(i+1)), 'w', newline='') as file:
        file.write(
            str(
                str(enigma.l_rotor.name) + ' ' +
                str(enigma.m_rotor.name) + ' ' +
                str(enigma.r_rotor.name) + '\n' +
                str(enigma.l_rotor.current_letter_setting()) + ' ' +
                str(enigma.m_rotor.current_letter_setting()) + ' ' +
                str(enigma.r_rotor.current_letter_setting()) + '\n' +
                str(enigma.l_rotor.ring_setting) + ' ' +
                str(enigma.m_rotor.ring_setting) + ' ' +
                str(enigma.r_rotor.ring_setting) + '\n' +
                str(enigma.reflector.name) + '\n' +
                ' '.join(steckers) + '\n'
            )
        )

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


data = {}

for text in LOREMS:
    data[text[0]] = []

for i in range(num_iterations):
    enigma = get_random_enigma(i)

    for l in LOREMS:
        LOREM = l[1]
        encrypted_lorem = enigma.encrypt(LOREM)
        y_data = []

        for crib_length in range(5, max_crib_length+1):
            closure_lengths = []
            # for _ in range(num_iterations):
            #     idx = random.randint(0, len(LOREM))
            # for idx in range(len(LOREM)):
            for idx in range(532):  # 532 is the length of the actual enigma message
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

            closure_lengths = dict((x, closure_lengths.count(x))
                                   for x in set(closure_lengths))

            y_data.append(sum(list(closure_lengths.values())[1:]))
            # y_data.append(closure_lengths[0])

        data[l[0]].append(y_data)

        # plt.plot(x_data, y_data, label=l[0])

# print(data)
x_data = np.arange(5, max_crib_length+1)

for d in data:
    l = np.array(data[d])
    y_data = np.average(l, axis=0)
    # print(y_data)
    plt.plot(x_data, y_data, label=d)


plt.legend()
plt.xlabel('Length of Crib')
# plt.ylabel('Rate of no closures occuring')
plt.ylabel('Rate of one or more closures occuring')
plt.show()
