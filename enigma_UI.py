from enigma import ALPHABET, Enigma
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import RELIEF_GROOVE, TEXT_LOCATION_CENTER
from rotor import ROTOR_DICT
from reflector import REFLECTOR_DICT

ROTORS = list(ROTOR_DICT.keys())
REFLECTORS = list(REFLECTOR_DICT.keys())

rotor_history = []
prev_input_length = 1
og_letters = ['A', 'A', 'A']

input_column = [
    [sg.Text(text='Input:')],
    [sg.Multiline(size=(50, 10), key='enigma_input', enable_events=True)]
]

rotor_l = [
    [sg.Combo(
        ROTORS,
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
        ),
        sg.T('A', k='l_ring_letter')
    ]
]


rotor_m = [
    [sg.Combo(
        ROTORS,
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
        ),
        sg.T('A', k='m_ring_letter')
    ]
]

rotor_r = [
    [sg.Combo(
        ROTORS,
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
        ),
        sg.T('A', k='r_ring_letter')
    ]
]

reflector = [
    [
        sg.Combo(
            REFLECTORS,
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
    [
        sg.Checkbox('Monitor', k='monitor', enable_events=True, default=False),
        sg.Check('Live Encrypt', k='live_encrypt',
                 enable_events=True, default=True),
        sg.B('Reset Enigma')
    ],
    [sg.Column([[sg.B('Encrypt'), sg.Check('Output to file',
                                           k='file_output')]], visible=False, k='encrypt_row')]
]


monitor_column = [
    [sg.T('Monitor:')],
    [sg.Output(size=(50, 35), k='monitor_output')]
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
    window['encrypt_row'].update(visible=not values['live_encrypt'])
    window['monitor_output'].update(
        '' if len(values['enigma_input']) == 1 else None)
    window['enigma_output'].update(
        '' if len(values['enigma_input']) == 1 else None)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
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
            else:
                window[event+'_letter'].update(
                    '' if len(values[event]) == 0 else ALPHABET[int(values[event])-1])
    elif event == 'enigma_input':
        if values['live_encrypt']:
            if (len(values['enigma_input']) < prev_input_length):
                prev_input_length = len(values['enigma_input'])
                window['l_start'].update(rotor_history[-1][0])
                window['m_start'].update(rotor_history[-1][1])
                window['r_start'].update(rotor_history[-1][2])
                rotor_history.pop(-1)
                cipher_text = values['enigma_output'][:-2]
                window['enigma_output'].update(cipher_text)
            elif (len(values['enigma_input']) > 1) and (values['enigma_input'][-2] in ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')):
                rotor_history += [[
                    values['l_start'].upper(),
                    values['m_start'].upper(),
                    values['r_start'].upper(),
                ]]
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

                cipher_letter = e.encrypt(values['enigma_input'][-2].upper())
                cipher_text = values['enigma_output'][:-1]+cipher_letter
                window['enigma_output'].update('')
                window['enigma_output'].update(cipher_text)
                window['l_start'].update(e.l_rotor.current_letter_setting())
                window['m_start'].update(e.m_rotor.current_letter_setting())
                window['r_start'].update(e.r_rotor.current_letter_setting())
                prev_input_length = len(values['enigma_input'])
            else:
                window['enigma_input'].update(values['enigma_input'][:-2])
        else:
            window['l_start'].update(
                og_letters[0] if (len(values['enigma_input']) == 1) and (len(rotor_history) == 0) else None)
            window['m_start'].update(
                og_letters[1] if (len(values['enigma_input']) == 1) and (len(rotor_history) == 0) else None)
            window['r_start'].update(
                og_letters[2] if (len(values['enigma_input']) == 1) and (len(rotor_history) == 0) else None)
    elif event == 'Encrypt':
        window['monitor_output'].update('')
        if (len(values['enigma_input']) == 1):
            window['monitor_output'].update('')
        elif (len(values['enigma_input']) > 1) and (values['enigma_input'][-2] in ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')):
            og_letters = [
                values['l_start'].upper(),
                values['m_start'].upper(),
                values['r_start'].upper(),
            ]
            e = Enigma(
                values['file_output'],
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
            window['l_start'].update(e.l_rotor.current_letter_setting())
            window['m_start'].update(e.m_rotor.current_letter_setting())
            window['r_start'].update(e.r_rotor.current_letter_setting())
        else:
            window['enigma_input'].update(values['enigma_input'][:-2])
    elif event == 'Reset Enigma':
        window['enigma_input'].update('')
        window['reflector'].update('B')
        window['l_rotor'].update('I')
        window['m_rotor'].update('II')
        window['r_rotor'].update('III')
        window['l_start'].update('A')
        window['m_start'].update('A')
        window['r_start'].update('A')
        window['l_ring'].update('1')
        window['m_ring'].update('1')
        window['r_ring'].update('1')
        window['steckers'].update('')
        window['enigma_output'].update('')
        window['monitor_output'].update('')

window.close()
