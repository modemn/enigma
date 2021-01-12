from enigma import Enigma
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Checkbox, Fr, Frame, RELIEF_GROOVE, TEXT_LOCATION_CENTER

input_column = [
    [sg.Text(text='Input:')],
    [sg.Multiline(size=(45, 10), key='-IN-')]
]

rotor_l = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'I',
        tooltip='Rotor Name',
        size=(6, 1),
        key='-LROTOR-'
    )],
    [sg.Input(
        'A',
        tooltip='Starting Letter',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1),
        key='-LSTART-'
    )],
    [
        sg.Input(
            '1',
            tooltip='Ring Setting',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1),
            key='-LRING-'
        ),
        sg.Text('A')
    ]
]


rotor_m = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'II',
        tooltip='Rotor Name',
        size=(6, 1),
        key='-MROTOR-',
    )],
    [sg.Input(
        'A',
        tooltip='Starting Letter',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1),
        key='-MSTART-'
    )],
    [
        sg.Input(
            '1',
            tooltip='Ring Setting',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1),
            key='-MRING-'
        ),
        sg.Text('A')
    ]
]

rotor_r = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'III',
        tooltip='Rotor Name',
        size=(6, 1),
        key='-RROTOR-',
    )],
    [sg.Input(
        'A',
        tooltip='Starting Letter',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1),
        key='-RSTART-'
    )],
    [
        sg.Input(
            '1',
            tooltip='Ring Setting',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1),
            key='-RRING-'
        ),
        sg.Text('A')
    ]
]

reflector = [
    [
        sg.Combo(
            ['A', 'B', 'C'],
            'B',
            tooltip='Reflector',
            size=(6, 1),
            key='-REFLECTOR-',
            pad=((5, 5), (24, 24))
        )
    ]
]

rotor_column = [
    [
        sg.Frame('Reflector', reflector, relief=RELIEF_GROOVE),
        sg.Frame('Left Rotor', rotor_l, relief=RELIEF_GROOVE),
        sg.Frame('Middle Rotor', rotor_m, relief=RELIEF_GROOVE),
        sg.Frame('Right Rotor', rotor_r, relief=RELIEF_GROOVE)
    ],
    [
        sg.Checkbox('Keyboard'),
        sg.Checkbox('Monitor'),
        sg.Button('Encrypt')
    ]
]

output_column = [
    [sg.Text('Output:')],
    [sg.Multiline(size=(45, 10), key='-OUTPUT-', disabled=True)]
]

layout = [
    [
        sg.Column(input_column),
        sg.VerticalSeparator(),
        sg.Column(rotor_column),
        sg.VerticalSeparator(),
        sg.Column(output_column),
    ],
    [sg.HorizontalSeparator()]

]

# Create the window
window = sg.Window("Enigma Machine", layout)


while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    print(values['-IN-'][:-1])
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Encrypt':
        e = Enigma(
            True,
            True,
            True,
            [
                values['-LROTOR-'],
                values['-MROTOR-'],
                values['-RROTOR-'],
            ],
            [
                values['-LSTART-'].upper(),
                values['-MSTART-'].upper(),
                values['-RSTART-'].upper(),
            ],
            [
                str(values['-LRING-']),
                str(values['-MRING-']),
                str(values['-RRING-']),
            ],
            str(values['-REFLECTOR-']),
            []  # Steckers
        )

        cipher_text = e.encrypt(values['-IN-'][:-1].upper())
        # change the "output" element to be the value of "input" element
        window['-OUTPUT-'].update('')
        window['-OUTPUT-'].update(cipher_text)


window.close()
