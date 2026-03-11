# Fichier jeu.py (Jeu)

from .case import Case
from .morpion import Morpion
from .grid import Grid
from .joueur import Joueur
from .action import Action

from model.utils import *


class Jeu:

    def __init__(self, dimension, j1, j2):
        self.dimensionGame = dimension
        self.mortpionGrid = Grid(self.dimensionGame)
        self.joueur1 = j1
        self.joueur2 = j2
        self.currentPlayer = None
        self.notCurrentPlayer = None
        self.compteur = 0

    def choose_Current_Player(self):
        if self.compteur % 2 == 1 :
            self.currentPlayer = self.joueur1
            self.notCurrentPlayer = self.joueur2
        else :
            self.currentPlayer = self.joueur2
            self.notCurrentPlayer = self.joueur1

        self.compteur += 1
    
    def get_action_joueur(self, case_actor, action_type, case_target=None, spell=None, morpion_to_place=None):
        return Action(self.mortpionGrid, self.currentPlayer, case_actor, action_type, case_target, spell, morpion_to_place)

    def get_tour_number(self):
        return self.compteur // 2

    def ask_action_console(self):

        if self.compteur <= 2:          # 1er tour des joueurs, placement d'un morpion
            print("Lors de votre 1er tour, vous devez placer un morpion !")
            return placementConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

        else :            # Autres tours des joueurs, attaque / lancement d'un sort / placement d'un morpion
            action_type = None
            while action_type not in {"attack","spell","placement"}:
                print("Quel est le type d'action que voulez vous effectuer ?")
                action_type = input("attack / spell / placement : ")
                if action_type not in {"attack","spell", "placement"}:
                    print("Vous ne pouvez que placer un morpion, attaquer ou lancer un sort ! ")

        if action_type == "spell":
            return spellConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

        elif action_type == "placement":
            return placementConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

        elif action_type == "attack":
            return attackConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

    def mortpion_Game_console(self):

        morpionlist = generate_random_morpions(6)
        morpionlist2 = generate_random_morpions(6)

        self.joueur1.set_morpion_team(morpionlist)
        self.joueur2.set_morpion_team(morpionlist2)

        while self.joueur1.is_alive() and self.joueur2.is_alive():

            self.choose_Current_Player()

            while True:

                self.currentPlayer.update_state_of_morpion()
                self.notCurrentPlayer.update_state_of_morpion()

                self.mortpionGrid.printGrid()

                print(f"\nTour de {self.currentPlayer.nom}")

                self.currentPlayer.print_team_morpion()

                case_actor, action_type, case_target, spell, morpion_to_place = self.ask_action_console()


                action_valide = self.currentPlayer.action_joueur(
                    self.mortpionGrid,
                    case_actor,
                    action_type,
                    case_target,
                    spell,
                    morpion_to_place,
                )

                if action_valide:
                    print("Action exécutée !")
                    break
                else:
                    print("Action invalide. Réessayez.\n")

            if self.mortpionGrid.is_grid_full() :
                return print("Partie Terminée, Aucun gagnant")

            if self.is_winner() == None:
                continue
            elif self.is_winner() == self.joueur1:
                self.mortpionGrid.printGrid()
                return print(f"Le joueur {self.joueur1.nom} a gagné")
            else:
                self.mortpionGrid.printGrid()
                return print(f"Le joueur {self.joueur2.nom} a gagné")

    def mortpion_Game_GUI(self):

        morpionlist = generate_random_morpions(6)
        morpionlist2 = generate_random_morpions(6)

        self.joueur1.set_morpion_team(morpionlist)
        self.joueur2.set_morpion_team(morpionlist2)

        while self.joueur1.is_alive() and self.joueur2.is_alive():

            self.choose_Current_Player()

            while True:

                self.currentPlayer.update_state_of_morpion()
                self.notCurrentPlayer.update_state_of_morpion()

                self.mortpionGrid.printGrid()

                print(f"\nTour de {self.currentPlayer.nom}")

                self.currentPlayer.print_team_morpion()

                case_actor, action_type, case_target, spell, morpion_to_place = self.ask_action_console()


                action_valide = self.currentPlayer.action_joueur(
                    self.mortpionGrid,
                    case_actor,
                    action_type,
                    case_target,
                    spell,
                    morpion_to_place,
                )

                if action_valide:
                    print("Action exécutée !")
                    break
                else:
                    print("Action invalide. Réessayez.\n")

            if self.mortpionGrid.is_grid_full() :
                return print("Partie Terminée, Aucun gagnant")

            if self.is_winner() == None:
                continue
            elif self.is_winner() == self.joueur1:
                self.mortpionGrid.printGrid()
                return print(f"Le joueur {self.joueur1.nom} a gagné")
            else:
                self.mortpionGrid.printGrid()
                return print(f"Le joueur {self.joueur2.nom} a gagné")

    def ask_action_GUI(self):
        if self.compteur <= 2:          # 1er tour des joueurs, placement d'un morpion
            print("Lors de votre 1er tour, vous devez placer un morpion !")
            return placementConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

        else :            # Autres tours des joueurs, attaque / lancement d'un sort / placement d'un morpion
            action_type = None
            while action_type not in {"attack","spell","placement"}:
                print("Quel est le type d'action que voulez vous effectuer ?")
                action_type = input("attack / spell / placement : ")
                if action_type not in {"attack","spell", "placement"}:
                    print("Vous ne pouvez que placer un morpion, attaquer ou lancer un sort ! ")

        if action_type == "spell":
            return spellConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

        elif action_type == "placement":
            return placementConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

        elif action_type == "attack":
            return attackConsole(self.mortpionGrid,self.dimensionGame,self.currentPlayer)

    def is_winner(self):

                    # Test si une des lignes est gagnante pour un joueur

        for i in range(self.mortpionGrid.playGround.shape[0]):
            team_row1 = self.mortpionGrid.get_team_morpion(i, 0)
            team_row2 = self.mortpionGrid.get_team_morpion(i, 1)
            team_row3 = self.mortpionGrid.get_team_morpion(i, 2)

            joueur_team_row1 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_row1)
            joueur_team_row2 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_row2)
            joueur_team_row3 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_row3)

            if joueur_team_row1 == joueur_team_row2 == joueur_team_row3 != None:
                return joueur_team_row1

                    # Test si une des colonnes est gagnante pour un joueur

        for j in range(self.mortpionGrid.playGround.shape[1]):
                team_col1 = self.mortpionGrid.get_team_morpion(0, j)
                team_col2 = self.mortpionGrid.get_team_morpion(1, j)
                team_col3 = self.mortpionGrid.get_team_morpion(2, j)

                joueur_team_col1 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_col1)
                joueur_team_col2 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_col2)
                joueur_team_col3 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_col3)
                if joueur_team_col1 == joueur_team_col2 == joueur_team_col3 != None:
                    return joueur_team_col1

                    # Test si une des diagonales est gagnante pour un joueur

        for i in range(self.mortpionGrid.playGround.shape[0]):
            for j in range(self.mortpionGrid.playGround.shape[1]):

                team_case_diag1 = self.mortpionGrid.get_team_morpion(0, 0)
                team_case_diag2 = self.mortpionGrid.get_team_morpion(1, 1)
                team_case_diag3 = self.mortpionGrid.get_team_morpion(2, 2)

                joueur_team_case_diag1 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_case_diag1)
                joueur_team_case_diag2 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_case_diag2)
                joueur_team_case_diag3 = get_joueur_from_morpion_team(self.joueur1, self.joueur2, team_case_diag3)
                if joueur_team_case_diag1 == joueur_team_case_diag2 == joueur_team_case_diag3 != None:
                    return joueur_team_case_diag1
                
        return None