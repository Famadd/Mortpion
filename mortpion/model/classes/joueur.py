# Fichier joueur.py (Joueur du jeu)

import random
from .case import Case
from .morpion import Morpion
from .grid import Grid
from .action import Action


class Joueur:

    def __init__(self, nom, morpion_team=None, team_color=None):
        self.nom = nom
        self.morpion_team = morpion_team if morpion_team is not None else []
        self.team_color = team_color

    def to_dict_Joueur(self):
        return {
            "nom" : self.nom,
            "morpion_team": self.morpion_team,
            "team_color": self.team_color
        }

    def from_dict_Joueur(player_data):

        if isinstance(player_data, Joueur):
            return player_data

        joueur = Joueur(player_data["nom"],player_data["morpion_team"], player_data["team_color"])
        return joueur

    def set_team_color(self, color):
        self.team_color = color

    def set_morpion_team(self, morpionlist):
        random.shuffle(morpionlist)
        self.morpion_team = morpionlist
        for m in self.morpion_team:
            m.morpionColor = self.team_color
            m.morpionTeam = self.morpion_team

    def get_morpion_in_team(self, id_morpion):
        for m in self.morpion_team:
            if m.id_morpion == id_morpion:
                return m
        return None

    def update_state_of_morpion(self):
        for m in self.morpion_team:
            if m is None or not m.check_alive():
                m = None

    def print_team_morpion(self):
        for morpion in self.morpion_team:
            print(morpion)
    
    def action_joueur(self ,grid ,case_actor ,action_type ,case_target=None ,spell=None, morpion_to_place=None):
        self.action = Action(grid ,self ,case_actor ,action_type ,case_target ,spell ,morpion_to_place)
        return self.action.execute()

    def is_alive(self):
        for m in self.morpion_team :
            if m is not None:
                return True
        return False
