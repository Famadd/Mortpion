# Fichier action.py (action d'un joueur)

from .case import Case
from .morpion import Morpion
from .grid import Grid



class Action:

    def __init__(self, grid, player, action_type, case_target_row, case_target_col, case_actor_row = None, case_actor_col = None, spell=None, morpion_to_place=None):
        self.grid = grid
        self.player = player
        self.case_actor_row = case_actor_row
        self.case_actor_col = case_actor_col
        self.action_type = action_type
        self.case_target_row = case_target_row
        self.case_target_col = case_target_col
        self.spell = spell
        self.morpion_to_place = morpion_to_place

    def to_dict(self):
        return {
            'grid': self.grid,
            'player': self.player,
            'case_actor_row': self.case_actor_row,
            'case_actor_col': self.case_actor_col,
            'action_type': self.action_type,
            'case_target_row': self.case_target_row,
            'case_target_col': self.case_target_col,
            'spell': self.spell,
            'morpion_to_place': self.morpion_to_place
        }

    def from_dict(action_data):

        if isinstance(action_data, Action):
            return action_data

        case_actor_row = action_data['case_actor_row'] if action_data['case_actor_row'] else None
        case_actor_col = action_data['case_actor_col'] if action_data['case_actor_col'] else None
        spell = action_data['spell'] if action_data['spell'] else None
        morpion_to_place = action_data['morpion_to_place'] if action_data['morpion_to_place'] else None

        action = Action(
            action_data['grid'],
            action_data['player'],
            case_actor_row,
            case_actor_col,
            action_data['action_type'],
            action_data['case_target_row'],
            action_data['case_target_col'],
            spell,
            morpion_to_place 
        )

        return action

    def execute(self):
        if self.action_type == "placement":
            # on vérifie que la case cible est vide
            if self.grid.playGround[self.case_target_row, self.case_target_col].morpionPlayer is None:
                # on vérifie que le morpion n'est pas déjà placé ailleurs sur la grille
                for row in range(self.grid.dimension):
                    for col in range(self.grid.dimension):
                        if self.grid.playGround[row, col].morpionPlayer is not None:
                            morpion_on_grid = self.grid.playGround[row, col].morpionPlayer
                            # On compare l'ID ET le propriétaire (player) pour être sûr que c'est le même morpion
                            if (morpion_on_grid.id_morpion == self.morpion_to_place.id_morpion and 
                                morpion_on_grid.player == self.morpion_to_place.player):
                                print(f"MESSAGE ERREUR : Le morpion {self.morpion_to_place.id_morpion} de {self.morpion_to_place.player} est déjà placé sur la grille à la position [{row},{col}]")
                                return False
                return self.grid.add_morpion(self.case_target_row, self.case_target_col, self.morpion_to_place)
            else:
                print("MESSAGE ERREUR : Il y a déjà un morpion sur cette case")
                return False
        elif self.action_type in ("attack","spell"):
            if self.action_type == 'attack':
                if self.grid.playGround[self.case_actor_row, self.case_actor_col].morpionPlayer is not None:
                    if self.grid.playGround[self.case_target_row, self.case_target_col].morpionPlayer is not None:
                        if self.grid.playGround[self.case_target_row, self.case_target_col] in self.grid.get_neighbours(self.case_actor_row, self.case_actor_col):
                            if self.grid.playGround[self.case_actor_row, self.case_actor_col].morpionPlayer.player != self.grid.playGround[self.case_target_row, self.case_target_col].morpionPlayer.player:
                                attack_result = self.grid.playGround[self.case_actor_row, self.case_actor_col].morpionPlayer.attack(self.grid.playGround[self.case_target_row, self.case_target_col].morpionPlayer)
                                self.attack_message = attack_result['message']
                                return True
                            else:
                                print("Vous ne pouvez pas attaquer un allié")
                                return False
                        else:
                                print("l'ennemi est trop loin")
                                return False
                    else:
                        print("Pas de morpion à cibler")
                        return False
                else:
                    print("Pas de morpion pour attaquer")
                    return False

            elif self.action_type == 'spell':
                if self.grid.playGround[self.case_actor_row, self.case_actor_col].morpionPlayer is None:
                    print("Pas de morpion pour lancer un sort")
                    return False
                
                actor_morpion = self.grid.playGround[self.case_actor_row, self.case_actor_col].morpionPlayer
                target_morpion = self.grid.playGround[self.case_target_row, self.case_target_col].morpionPlayer
                
                if self.spell == 'fire_ball':
                    if target_morpion is None:
                        print("Pas de morpion à cibler pour fire_ball")
                        return False
                    if actor_morpion.player != target_morpion.player:
                        return actor_morpion.fire_ball_spell(target_morpion)
                    else:
                        print("Vous ne pouvez pas utiliser boule de feu sur vos alliés")
                        return False

                elif self.spell == 'heal':
                    if target_morpion is None:
                        print("Pas de morpion à soigner")
                        return False
                    if actor_morpion.player == target_morpion.player:
                        return actor_morpion.healing_spell(target_morpion)
                    else:
                        print("Vous ne pouvez soigner que vos alliés")
                        return False

                elif self.spell == 'armageddon':
                    if actor_morpion.mana >= 5:
                        result = actor_morpion.armageddon_spell(target_morpion if target_morpion else None)
                        if result:
                            return self.grid.destroy_case(self.case_target_row, self.case_target_col)
                        return False
                    else:
                        print("Vous n'avez pas assez de mana pour lancer armageddon !")
                        return False
                
                print("Sort invalide")
                return False
        
        print('PAS PLACEMENT / ATTAQUE / SORT')
        return False
