from timer import Timer
from bombe_2_for_UI import Bombe
import PySimpleGUI as sg
from menu_generator_1 import MenuGenerator

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

rotors = [
    sg.T('Top Rotor:', k='trotor_text'),
    sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'II',
        size=(4, 1),
        key='t_rotor',
    ),
    sg.T('Middle Rotor:', k='mrotor_text'),
    sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'V',
        size=(4, 1),
        key='m_rotor',
    ),
    sg.T('Bottom Rotor:', k='brotor_text'),
    sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'III',
        size=(4, 1),
        key='b_rotor',
    ),
]

reflector = [
    sg.T('Reflector:'),
    sg.Combo(
        ['A', 'B', 'C'],
        'B',
        size=(4, 1),
        key='reflector',
    )
]

input_column = [
    [
        sg.T('Plain Crib:'),
        sg.In(key='plaincrib', default_text='WETTERVORHERSAGE')
    ],
    [
        sg.T('Cipher Crib:'),
        sg.In(key='ciphercrib', default_text='SNMKGGSTZZUGARLV')
    ],
    [
        sg.T("Starting Letters:"),
        sg.Combo(
            list(ALPHABET),
            'Z',
            size=(4, 1),
            key='sletter1',
        ),
        sg.Combo(
            list(ALPHABET),
            'Z',
            size=(4, 1),
            key='sletter2',
        ),
        sg.Combo(
            list(ALPHABET),
            'Z',
            size=(4, 1),
            key='sletter3',
        ),
    ],
    [
        sg.CB('Continuous Mode', default=False,
              key='continuous', enable_events=True)
    ],
    [sg.Col([reflector], k='reflector_row')],
    [sg.Col([rotors], k='rotors_row')],
]

setting_output_column = [
    [sg.Button('Create Menu')],
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
    [sg.Output(size=(70, 50), k='output')]
]

layout = [
    [sg.Column(input_column)],
    [sg.HorizontalSeparator()],
    [sg.Column(setting_output_column)],
    [sg.HorizontalSeparator()],
    [sg.Column(bombe_output_column)],
]

# Create the window
window = sg.Window("Bombe", layout, size=(500, 500))

while True:  # Event Loop
    event, values = window.read()

    window['rotors_row'].update(visible=not values['continuous'])
    window['reflector_row'].update(visible=not values['continuous'])

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Create Menu':
        top_rotor = values['t_rotor']
        middle_rotor = values['m_rotor']
        bottom_rotor = values['b_rotor']
        starting_letters = str(
            values['sletter1']+values['sletter2']+values['sletter3'])
        reflector = values['reflector']
        plain_crib = values['plaincrib']
        cipher_crib = values['ciphercrib']

        mg = MenuGenerator(
            plain_crib,
            cipher_crib,
            starting_letters
        )

        settings, connections, input_letter, _ = mg.get_bombe_settings()

        window['settings'].update(settings)
        window['connections'].update(connections)
        window['Start Bombe'].update(disabled=False)
        window['output'].update('')

        if (not values['continuous']):
            print('******************BOMBE******************')
            print('Running the Bombe with the following settings:')
            print('Rotors:', top_rotor, middle_rotor, bottom_rotor)
            print('Reflector:', reflector)
            print('Starting Letters:', starting_letters)
            print('Input Letter:', input_letter)
            print('*****************************************')
            print()

    elif event == 'Start Bombe':
        if values['continuous']:
            print('CONTINUOUS MODE MAY TAKE SOME TIME')
            print('180 possible settings to go through')
            print()
            ROTORS = ['I', 'II', 'III', 'IV', 'V']
            REFLECTORS = ['A', 'B', 'C']
            rotor_combos = [(x, y, z)
                            for x in ROTORS for y in ROTORS for z in ROTORS if x != y if y != z if x != z]

            timer = Timer()
            timer.start()
            i = 0
            for top_rotor, middle_rotor, bottom_rotor in rotor_combos:
                for reflector in REFLECTORS:
                    i += 1
                    print(f'Settings {i}/180')
                    print('******************BOMBE******************')
                    print('Running the Bombe with the following settings:')
                    print('Rotors:', top_rotor, middle_rotor, bottom_rotor)
                    print('Reflector:', reflector)
                    print('Starting Letters:', starting_letters)
                    print('Input Letter:', input_letter)
                    print('*****************************************')
                    print()

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
                    b.auto_run(plain_crib, cipher_crib)

            print('Total time through all rotors:', timer.stop())
        else:
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
            print()
            output = b.auto_run(plain_crib, cipher_crib)
            print()
            for line in output:
                print(line)

window.close()
