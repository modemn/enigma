from enigma import Enigma
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import RELIEF_GROOVE, TEXT_LOCATION_CENTER

input_column = [
    [sg.Text(text='Input:')],
    [sg.Multiline(size=(50, 10), key='enigma_input')]
]

rotor_l = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'I',
        tooltip='Rotor Name',
        size=(6, 1),
        key='l_rotor',
        readonly=True
    )],
    [sg.Input(
        'A',
        tooltip='Starting Letter',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1),
        key='l_start',
        enable_events=True
    )],
    [
        sg.Input(
            '1',
            tooltip='Ring Setting',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1),
            key='l_ring',
            enable_events=True
        )
    ]
]


rotor_m = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'II',
        tooltip='Rotor Name',
        size=(6, 1),
        key='m_rotor',
        readonly=True
    )],
    [sg.Input(
        'A',
        tooltip='Starting Letter',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1),
        key='m_start',
        enable_events=True
    )],
    [
        sg.Input(
            '1',
            tooltip='Ring Setting',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1),
            key='m_ring',
            enable_events=True
        )
    ]
]

rotor_r = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'III',
        tooltip='Rotor Name',
        size=(6, 1),
        key='r_rotor',
        readonly=True
    )],
    [sg.Input(
        'A',
        tooltip='Starting Letter',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1),
        key='r_start',
        enable_events=True
    )],
    [
        sg.Input(
            '1',
            tooltip='Ring Setting',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1),
            key='r_ring',
            enable_events=True
        )
    ]
]

reflector = [
    [
        sg.Combo(
            ['A', 'B', 'C'],
            'B',
            tooltip='Reflector',
            size=(6, 1),
            key='reflector',
            pad=((5, 5), (24, 24)),
            readonly=True
        )
    ]
]

plugboard = [
    [sg.In(k='steckers')]
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

# Create the window
window = sg.Window("Enigma Machine", layout)


while True:  # Event Loop
    event, values = window.read()
    window['mc'].update(visible=values['monitor'])

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
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
        # change the "output" element to be the value of "input" element
        window['enigma_output'].update('')
        window['enigma_output'].update(cipher_text)
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

window.close()
