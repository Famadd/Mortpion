# Fichier case.py (Case du plateau)

from .morpion import Morpion

class Case:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = True
        self.morpionPlayer = None


    def to_dict_case(self):
        return{
            'row': self.row,
            'col': self.col,
            'state': self.state,
            'morpionPlayer': self.morpionPlayer
        }
    
    def from_dict_case(case_data):

        if isinstance(case_data, Case):
            return case_data

        case = Case(
            case_data['row'],
            case_data['col'],
            case_data['state'],
            case_data['morpionPlayer'] 
        )

        return case

    def add_morpion(self, morpion):
        if self.morpionPlayer is None and self.state:
            self.morpionPlayer = morpion
            return True
        return False
    
    def get_morpion_player(self):
        if self.morpionPlayer is not None:
            return self.morpionPlayer.get_player()
    
    def remove_morpion(self):
        self.morpionPlayer = None

    def reset(self):
        self.state = True
        self.morpionPlayer = None

    def destroy_case(self):
        if self.state:
            self.state = False
            self.remove_morpion()
            return True
        return False
