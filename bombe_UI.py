from timer import Timer
from bombe_2 import Bombe
import PySimpleGUI as sg
from menu_generator_1 import MenuGenerator
import run_continuous

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
    window['continuous_error'].update(visible=values['continuous'])

    if event == sg.WIN_CLOSED or event == 'Exit':
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
        reflector = values['reflector'].upper()
        plain_crib = values['plaincrib'].upper()
        cipher_crib = values['ciphercrib'].upper()

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
            window['output'].update('')
        else:
            window['no_closure_error'].update(visible=False)
            window['settings'].update(settings)
            window['connections'].update(connections)
            window['Start Bombe'].update(disabled=False)
            window['output'].update('')

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
                True,
                False
            )

            print('RUNNING...')
            print()
            b.auto_run(plain_crib, cipher_crib)

window.close()
