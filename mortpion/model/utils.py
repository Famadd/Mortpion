from model.classes.morpion import Morpion
from model.model_pg import *

import random

def generate_random_morpions(n):
        morpions = []
        for i in range(1, n+1):
            # Définir aléatoirement si c'est un guerrier (pas de mana) ou un mage (avec mana)
            is_mage = random.choice([True, False])

            id_morpion = i + 1 
            point_hp = random.randint(10, 18)
            point_att = random.randint(3, 8)
            point_hit = random.randint(0, 10)  # valeur entre 4 et 10 (au minimum 40% de réussite)

            if is_mage:
                point_mana = random.randint(5, 20)
                morpion = Morpion(
                    id_morpion=id_morpion,
                    point_hp=point_hp,
                    point_att=point_att,
                    point_mana=point_mana,
                    point_hit=point_hit
                    )
            else:

                morpion = Morpion(
                    id_morpion=id_morpion,
                    point_hp=point_hp,
                    point_att=point_att,
                    point_mana=0,
                    point_hit=point_hit
                    )
            morpions.append(morpion)

        return morpions


def get_list_morpions_bd(connexion):

    morpions_list = []
    for m in get_morpions(connexion):
            morpion = Morpion(
                m[0],
                m[2],
                m[3],
                m[1],
                m[4]
            )
            random_img = random.randint(1,16)
            morpion.img_path = f"/static/img/t{random_img}.png"
            morpions_list.append(morpion)

    return morpions_list

def add_player_name_to_morpion(morpion_list, nom):
        for m in morpion_list:
            m.player = nom

def to_dict_morpions_list(morpions):

    morpion_dict_list = []
    for m in morpions:
        morpion_dict_list.append(m.to_dict_morpion())
    return morpion_dict_list

def from_dict_morpions_list(morpions_dict):
    morpion_list = []
    for m in morpions_dict:
        morpion_list.append(Morpion.from_dict_morpion(m))
    return morpion_list

def get_joueur_from_morpion_team(j1, j2, morpion_team):
        if morpion_team == None:
            return None
        elif  j1.morpion_team == morpion_team:
            return j1
        else:
            return j2

def placementConsole(grid, dimensionGame, currentPlayer):
    choix_morpion = None
    morpion_to_place = None
    while True:
        try:
            choix_morpion = int(input("Choisissez l'ID du morpion que vous voulez placer : "))
        except ValueError:
            print("Veuillez entrer un nombre entier.")
            continue

        morpion_to_place = currentPlayer.get_morpion_in_team(choix_morpion)
        if morpion_to_place is not None:
            break
        else:
            print("Ce morpion n'est pas dans votre équipe, réessayez.")

    choix_ligne_case1 = 50
    choix_colonne_case1 = 50
    while not (0 <= choix_ligne_case1 < dimensionGame and 0 <= choix_colonne_case1 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez la case :")
        choix_ligne_case1 = int(input("ligne : "))
        choix_colonne_case1 = int(input("colonne : "))

    case_actor = grid.playGround[choix_ligne_case1,choix_colonne_case1]

    return case_actor, 'placement', None, None, morpion_to_place

def attackConsole(grid, dimensionGame, currentPlayer):

    choix_ligne_case1 = 50
    choix_colonne_case1 = 50
    while not (0 <= choix_ligne_case1 < dimensionGame and 0 <= choix_colonne_case1 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez votre morpion attaquant :")
        choix_ligne_case1 = int(input("ligne : "))
        choix_colonne_case1 = int(input("colonne : "))

    case_actor = grid.playGround[choix_ligne_case1,choix_colonne_case1]

    choix_ligne_case2 = 50
    choix_colonne_case2 = 50
    while not (0 <= choix_ligne_case2 < dimensionGame and 0 <= choix_colonne_case2 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez le morpion ennemi que vous voulez attaquer : ")
        choix_ligne_case2 = int(input("ligne : "))
        choix_colonne_case2 = int(input("colonne : "))

    case_target = grid.playGround[choix_ligne_case2,choix_colonne_case2]

    return case_actor, "attack", case_target, None, None

def spellConsole(grid, dimensionGame, currentPlayer):
    spell = None
    while spell not in {"fire_ball", "heal", "armageddon"}:
        print("Quel sort voulez vous lancer ? ")
        spell = input("Sort : ")

    choix_ligne_case1 = 50
    choix_colonne_case1 = 50
    while not (0 <= choix_ligne_case1 < dimensionGame and 0 <= choix_colonne_case1 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez votre morpion attaquant :")
        choix_ligne_case1 = int(input("ligne : "))
        choix_colonne_case1 = int(input("colonne : "))

    case_actor = grid.playGround[choix_ligne_case1,choix_colonne_case1]

    choix_ligne_case2 = 50
    choix_colonne_case2 = 50
    while not (0 <= choix_ligne_case2 < dimensionGame and 0 <= choix_colonne_case2 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez le morpion ennemi que vous voulez attaquer : ")
        choix_ligne_case2 = int(input("ligne : "))
        choix_colonne_case2 = int(input("colonne : "))

    case_target = grid.playGround[choix_ligne_case2,choix_colonne_case2]

    return case_actor, "spell", case_target, spell, None

def placementGUI(grid, dimensionGame, currentPlayer):
    choix_morpion = None
    morpion_to_place = None
    while True:
        try:
            choix_morpion = int(input("Choisissez l'ID du morpion que vous voulez placer : "))
        except ValueError:
            print("Veuillez entrer un nombre entier.")
            continue

        morpion_to_place = currentPlayer.get_morpion_in_team(choix_morpion)
        if morpion_to_place is not None:
            break
        else:
            print("Ce morpion n'est pas dans votre équipe, réessayez.")

    choix_ligne_case1 = 50
    choix_colonne_case1 = 50
    while not (0 <= choix_ligne_case1 < dimensionGame and 0 <= choix_colonne_case1 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez la case :")
        choix_ligne_case1 = int(input("ligne : "))
        choix_colonne_case1 = int(input("colonne : "))

    case_actor = grid.playGround[choix_ligne_case1,choix_colonne_case1]

    return case_actor, 'placement', None, None, morpion_to_place

def attackGUI(grid, dimensionGame, currentPlayer):

    choix_ligne_case1 = 50
    choix_colonne_case1 = 50
    while not (0 <= choix_ligne_case1 < dimensionGame and 0 <= choix_colonne_case1 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez votre morpion attaquant :")
        choix_ligne_case1 = int(input("ligne : "))
        choix_colonne_case1 = int(input("colonne : "))

    case_actor = grid.playGround[choix_ligne_case1,choix_colonne_case1]

    choix_ligne_case2 = 50
    choix_colonne_case2 = 50
    while not (0 <= choix_ligne_case2 < dimensionGame and 0 <= choix_colonne_case2 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez le morpion ennemi que vous voulez attaquer : ")
        choix_ligne_case2 = int(input("ligne : "))
        choix_colonne_case2 = int(input("colonne : "))

    case_target = grid.playGround[choix_ligne_case2,choix_colonne_case2]

    return case_actor, "attack", case_target, None, None

def spellGUI(grid, dimensionGame, currentPlayer):
    spell = None
    while spell not in {"fire_ball", "heal", "armageddon"}:
        print("Quel sort voulez vous lancer ? ")
        spell = input("Sort : ")

    choix_ligne_case1 = 50
    choix_colonne_case1 = 50
    while not (0 <= choix_ligne_case1 < dimensionGame and 0 <= choix_colonne_case1 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez votre morpion attaquant :")
        choix_ligne_case1 = int(input("ligne : "))
        choix_colonne_case1 = int(input("colonne : "))

    case_actor = grid.playGround[choix_ligne_case1,choix_colonne_case1]

    choix_ligne_case2 = 50
    choix_colonne_case2 = 50
    while not (0 <= choix_ligne_case2 < dimensionGame and 0 <= choix_colonne_case2 < dimensionGame):
        print(f"\n--- Tour de {currentPlayer.nom} ---")

        # 1. Choisir le morpion qui joue
        print("Choisissez le morpion ennemi que vous voulez attaquer : ")
        choix_ligne_case2 = int(input("ligne : "))
        choix_colonne_case2 = int(input("colonne : "))

    case_target = grid.playGround[choix_ligne_case2,choix_colonne_case2]

    return case_actor, "spell", case_target, spell, None