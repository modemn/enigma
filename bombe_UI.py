from bombe_2 import Bombe
from enigma import Enigma
import PySimpleGUI as sg
from menu_generator_1 import MenuGenerator
from PySimpleGUI.PySimpleGUI import RELIEF_GROOVE, TEXT_LOCATION_CENTER
import run_continuous

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def make_bombe():
    stops = []
    rotors = [
        sg.T('Top Rotor:', k='trotor_text'),
        sg.Combo(
            ['I', 'II', 'III', 'IV', 'V'],
            'II',
            size=(4, 1),
            key='t_rotor',
            readonly=True
        ),
        sg.T('Middle Rotor:', k='mrotor_text'),
        sg.Combo(
            ['I', 'II', 'III', 'IV', 'V'],
            'V',
            size=(4, 1),
            key='m_rotor',
            readonly=True
        ),
        sg.T('Bottom Rotor:', k='brotor_text'),
        sg.Combo(
            ['I', 'II', 'III', 'IV', 'V'],
            'III',
            size=(4, 1),
            key='b_rotor',
            readonly=True
        ),
    ]

    reflector = [
        sg.T('Reflector:'),
        sg.Combo(
            ['A', 'B', 'C'],
            'B',
            size=(4, 1),
            key='bombe_reflector',
            readonly=True
        )
    ]

    input_column = [
        [
            sg.T('Cipher text:'),
            sg.Multiline(key='ciphertext',
                         default_text='SNMKGGSTZZUGARLV', size=(45, 5))
        ],
        [
            sg.T('Plain Crib:'),
            sg.In(key='plaincrib', default_text='WETTERVORHERSAGE')
        ],
        [
            sg.T('Crib Index:'),
            sg.In(key='cribindex', default_text='0',
                  enable_events=True, size=(5, 1)),
            sg.T('Crib Length:'),
            sg.In(key='criblen', default_text='16',
                  enable_events=True, size=(5, 1))
        ],
        [
            sg.T("Starting Letters:"),
            sg.Combo(
                list(ALPHABET),
                'Z',
                size=(4, 1),
                key='sletter1',
                readonly=True
            ),
            sg.Combo(
                list(ALPHABET),
                'Z',
                size=(4, 1),
                key='sletter2',
                readonly=True
            ),
            sg.Combo(
                list(ALPHABET),
                'Z',
                size=(4, 1),
                key='sletter3',
                readonly=True
            ),
        ],
        [
            sg.CB('Continuous Mode', default=False,
                  key='continuous', enable_events=True),
            sg.T('Warning! Continuous Mode may take a considerable amount of time',
                 visible=False, k='continuous_error', background_color='red')
        ],
        [sg.Col([reflector], k='reflector_row')],
        [sg.Col([rotors], k='rotors_row')],
    ]

    setting_output_column = [
        [
            sg.Button('Create Menu'),
            sg.T('That plain/cipher crib combo has no closures, please try another',
                 k='no_closure_error', background_color='red', visible=False)
        ],
        [
            sg.T("Scrambler Settings:"),
            sg.Multiline(k='settings', disabled=True)
        ],
        [
            sg.T("Scrambler Connections:"),
            sg.Multiline(k='connections', disabled=True)
        ]
    ]

    bombe_output_column = [
        [sg.B('Start Bombe', disabled=True)],
        [sg.T('Stops:')],
        [
            sg.Listbox(values=stops, size=(20, 10),
                       k='stoplist', enable_events=True),
            sg.Multiline(size=(50, 10), k='bombe_output', disabled=True)
        ],
        [sg.B('View on Enigma', visible=False)]
    ]

    layout = [
        [sg.Column(input_column)],
        [sg.HorizontalSeparator()],
        [sg.Column(setting_output_column)],
        [sg.HorizontalSeparator()],
        [sg.Column(bombe_output_column)],
    ]

    return sg.Window("Bombe", layout, finalize=True)


def make_enigma(stop_info):
    stop_info = stop_info.splitlines()
    rotors = stop_info[0][8:].split()
    enigma_reflector = stop_info[1][11:]
    ring_settings = stop_info[2][24:].split()
    enigma_starting_letters = stop_info[3][18:].split()
    steckers = stop_info[4][19:].split()
    input_text = stop_info[6][:-22]

    input_column = [
        [sg.Text(text='Input:')],
        [sg.Multiline(size=(50, 10), key='enigma_input',
                      default_text=input_text)]
    ]

    rotor_l = [
        [sg.Combo(
            ['I', 'II', 'III', 'IV', 'V'],
            rotors[0],
            tooltip='Rotor Name',
            size=(6, 1),
            key='l_rotor'
        )],
        [sg.Input(
            enigma_starting_letters[0],
            tooltip='Starting Letter',
            justification=TEXT_LOCATION_CENTER,
            size=(8, 1),
            key='l_start'
        )],
        [
            sg.Input(
                ring_settings[0],
                tooltip='Ring Setting',
                justification=TEXT_LOCATION_CENTER,
                size=(3, 1),
                key='l_ring'
            )
        ]
    ]

    rotor_m = [
        [sg.Combo(
            ['I', 'II', 'III', 'IV', 'V'],
            rotors[1],
            tooltip='Rotor Name',
            size=(6, 1),
            key='m_rotor',
        )],
        [sg.Input(
            enigma_starting_letters[1],
            tooltip='Starting Letter',
            justification=TEXT_LOCATION_CENTER,
            size=(8, 1),
            key='m_start'
        )],
        [
            sg.Input(
                ring_settings[1],
                tooltip='Ring Setting',
                justification=TEXT_LOCATION_CENTER,
                size=(3, 1),
                key='m_ring'
            )
        ]
    ]

    rotor_r = [
        [sg.Combo(
            ['I', 'II', 'III', 'IV', 'V'],
            rotors[2],
            tooltip='Rotor Name',
            size=(6, 1),
            key='r_rotor',
        )],
        [sg.Input(
            enigma_starting_letters[2],
            tooltip='Starting Letter',
            justification=TEXT_LOCATION_CENTER,
            size=(8, 1),
            key='r_start'
        )],
        [
            sg.Input(
                ring_settings[2],
                tooltip='Ring Setting',
                justification=TEXT_LOCATION_CENTER,
                size=(3, 1),
                key='r_ring'
            )
        ]
    ]

    reflector = [
        [
            sg.Combo(
                ['A', 'B', 'C'],
                enigma_reflector,
                tooltip='Reflector',
                size=(6, 1),
                key='reflector',
                pad=((5, 5), (24, 24))
            )
        ]
    ]

    plugboard = [
        [sg.In(k='steckers', default_text=" ".join(steckers))]
    ]

    rotor_column = [
        [
            sg.Frame('Reflector', reflector, relief=RELIEF_GROOVE),
            sg.Frame('Left Rotor', rotor_l, relief=RELIEF_GROOVE),
            sg.Frame('Middle Rotor', rotor_m, relief=RELIEF_GROOVE),
            sg.Frame('Right Rotor', rotor_r, relief=RELIEF_GROOVE)
        ],
        [sg.Frame('Steckers', plugboard, relief=RELIEF_GROOVE)],
        [sg.Checkbox('Monitor', k='monitor', enable_events=True)],
        [sg.Button('Encrypt')]
    ]

    monitor_column = [
        [sg.T('Monitor:')],
        [sg.Output(size=(50, 35))]
    ]

    output_column = [
        [sg.Text('Output:')],
        [sg.Multiline(size=(50, 10), key='enigma_output', disabled=True)]
    ]

    left_column = [
        [sg.Column(input_column)],
        [sg.Column(rotor_column)],
        [sg.Column(output_column)]
    ]

    layout = [
        [sg.Column(left_column), sg.Column(
            monitor_column, visible=False, k='mc')]
    ]

    return sg.Window("Enigma Machine", layout, finalize=True)


bombe_window, enigma_window = make_bombe(), None

while True:  # Event Loop
    window, event, values = sg.read_all_windows()

    if window == bombe_window:
        window['rotors_row'].update(visible=not values['continuous'])
        window['reflector_row'].update(visible=not values['continuous'])
        window['continuous_error'].update(visible=values['continuous'])
    if window == enigma_window:
        window['mc'].update(visible=values['monitor'])

    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == enigma_window:       # if closing win 2, mark as closed
            enigma_window = None
        elif window == bombe_window:     # if closing win 1, exit program
            break
    elif event == 'Create Menu':
        top_rotor = values['t_rotor'].upper()
        middle_rotor = values['m_rotor'].upper()
        bottom_rotor = values['b_rotor'].upper()
        starting_letters = str(
            values['sletter1'].upper() +
            values['sletter2'].upper() +
            values['sletter3'].upper()
        )
        reflector = values['bombe_reflector'].upper()
        plain_crib = values['plaincrib'].upper()
        cipher_crib = values['ciphertext'][int(values['cribindex']):int(
            values['cribindex'])+int(values['criblen'])].upper()

        mg = MenuGenerator(
            plain_crib,
            cipher_crib,
            starting_letters
        )

        settings, connections, input_letter, _ = mg.get_bombe_settings()
        if (len(settings) == 0):
            window['no_closure_error'].update(visible=True)
            window['settings'].update('')
            window['connections'].update('')
            window['Start Bombe'].update(disabled=True)
            window['bombe_output'].update('')
        else:
            window['no_closure_error'].update(visible=False)
            window['settings'].update(settings)
            window['connections'].update(connections)
            window['Start Bombe'].update(disabled=False)
            window['bombe_output'].update('')
    elif event == 'Start Bombe':
        if values['continuous']:
            print('foo')
            # ROTORS = ['I', 'II', 'III', 'IV', 'V']
            # REFLECTORS = ['A', 'B', 'C']

            # timer = Timer()
            # timer.start()

            # run_continuous.run(
            #     ROTORS,
            #     REFLECTORS,
            #     starting_letters,
            #     input_letter,
            #     settings,
            #     connections,
            #     plain_crib,
            #     cipher_crib
            # )

            # print('Total time through all rotors:', timer.stop())
        else:
            b = Bombe(
                top_rotor,
                middle_rotor,
                bottom_rotor,
                starting_letters,
                reflector,
                settings,
                connections,
                input_letter,
                False,
                False
            )
            stops = b.auto_run(plain_crib, cipher_crib)
            stoplist = []
            for i in range(len(stops)):
                stoplist += [f'Stop {i+1}']
            window['stoplist'].update(values=stoplist)
    elif event == 'cribindex' and values['cribindex'][-1] not in ('0123456789'):
        window['cribindex'].update(values['cribindex'][:-1])
    elif event == 'criblen' and values['criblen'][-1] not in ('0123456789'):
        window['criblen'].update(values['criblen'][:-1])
    elif event == 'stoplist' and values['stoplist']:
        window['bombe_output'].update(stops[int(values['stoplist'][0][-1])-1])
        window['View on Enigma'].update(visible=True)
    elif event == 'View on Enigma' and not enigma_window:
        enigma_window = make_enigma(stops[int(values['stoplist'][0][-1])-1])
    elif event in ['l_start', 'm_start', 'r_start']:
        if len(values[event]) > 0:
            if values[event][-1] not in ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                window[event].update(values[event][:-1])
            elif len(values[event]) > 1:
                window[event].update(values[event][:-1])
            elif values[event][-1] in ('abcdefghijklmnopqrstuvwxyz'):
                window[event].update(
                    values[event][:-1]+values[event][-1].upper())
    elif event in ['l_ring', 'm_ring', 'r_ring']:
        if len(values[event]) > 0:
            if values[event] not in [str(x) for x in range(1, 27)]:
                window[event].update(values[event][:-1])
    elif event == 'Encrypt':
        e = Enigma(
            False,
            values['monitor'],
            True,
            [
                values['l_rotor'],
                values['m_rotor'],
                values['r_rotor'],
            ],
            [
                values['l_start'].upper(),
                values['m_start'].upper(),
                values['r_start'].upper(),
            ],
            [
                str(values['l_ring']),
                str(values['m_ring']),
                str(values['r_ring']),
            ],
            str(values['reflector']),
            values['steckers'].upper().split()
        )

        cipher_text = e.encrypt(values['enigma_input'][:-1].upper())
        window['enigma_output'].update('')
        window['enigma_output'].update(cipher_text)

window.close()
