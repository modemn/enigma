from typing import Text
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import RELIEF_GROOVE, TEXT_LOCATION_CENTER

input_column = [
    [sg.Text(text='Input:')],
    [sg.Multiline(size=(45, 10))]
]

rotor_l = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'I',
        tooltip='Rotor Name',
        size=(6, 1)
    )],
    [sg.Input(
        'A',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1)
    )],
    [
        sg.Input(
            '1',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1)
        ),
        sg.Text('A')
    ]
]


rotor_m = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'I',
        tooltip='Rotor Name',
        size=(6, 1)
    )],
    [sg.Input(
        'A',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1)
    )],
    [
        sg.Input(
            '1',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1)
        ),
        sg.Text('A')
    ]
]

rotor_r = [
    [sg.Combo(
        ['I', 'II', 'III', 'IV', 'V'],
        'I',
        tooltip='Rotor Name',
        size=(6, 1)
    )],
    [sg.Input(
        'A',
        justification=TEXT_LOCATION_CENTER,
        size=(8, 1)
    )],
    [
        sg.Input(
            '1',
            justification=TEXT_LOCATION_CENTER,
            size=(3, 1)
        ),
        sg.Text('A')
    ]
]

rotor_column = [
    [
        sg.Frame('Left Rotor', rotor_l, relief=RELIEF_GROOVE),
        sg.Frame('Middle Rotor', rotor_m, relief=RELIEF_GROOVE),
        sg.Frame('Right Rotor', rotor_r, relief=RELIEF_GROOVE)
    ],
    [sg.Button('Encrypt')]
]

output_column = [
    [sg.Text('Output:')],
    [sg.Output(size=(45, 10))]
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

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == 'Encrypt':
        print(values[0])
    if event == sg.WIN_CLOSED:
        break

window.close()
