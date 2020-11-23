ALPHABET = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'


class IndicatorRotor:
    def __init__(self, starting_letter):
        self.pos = ALPHABET.find(starting_letter)

    def current_letter(self):
        return ALPHABET[self.pos]

    def step(self):
        self.pos = (self.pos + 1) % 26


class Indicator:
    def __init__(self, starting_letters):
        self.starting_letters = starting_letters
        self.t_rotor = IndicatorRotor(starting_letters[0])
        self.m_rotor = IndicatorRotor(starting_letters[1])
        self.b_rotor = IndicatorRotor(starting_letters[2])

    def step_rotors(self):
        self.t_rotor.step()
        if (self.t_rotor.current_letter() == self.starting_letters[0]):
            self.m_rotor.step()
            if (self.m_rotor.current_letter() == self.starting_letters[1]):
                self.b_rotor.step()
