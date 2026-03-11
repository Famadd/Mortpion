import json
from model.classes.jeuGUI import *
from model.classes.joueur import *
from model.classes.grid import *
from model.classes.action import *
from model.utils import *


def check_max_tours():
    if SESSION.get('game') and SESSION.get('max_tours'):
        jeu_temp = JeuGUI.from_dict(SESSION['game'])
        tour_actuel = jeu_temp.get_tour_number()
        max_tours = SESSION['max_tours']
        if tour_actuel >= max_tours:
            return True
    return False


def get_placed_morpions_for_player(player_name):
    placed = []
    if SESSION.get('game'):
        jeu = JeuGUI.from_dict(SESSION['game'])

        for row in range(jeu.mortpionGrid.dimension):
            for col in range(jeu.mortpionGrid.dimension):
                morpion = jeu.mortpionGrid.playGround[row, col].morpionPlayer
                if morpion and morpion.player == player_name:
                    placed.append((morpion.id_morpion, player_name))
    

    for dead_id, dead_player in SESSION.get('dead_morpions', []):
        if dead_player == player_name:
            if (dead_id, dead_player) not in placed:
                placed.append((dead_id, dead_player))
    
    return placed


if SESSION.get('current_action') is None:
    SESSION['current_action'] = {"type": None, 
                                 "morpion": None, 
                                 "actor_row": None, 
                                 "actor_col" : None, 
                                 "target_row" : None, 
                                 "target_col": None,
                                 "spell": None
                                 }

SESSION['morpion'] = None
SESSION['game_over'] = False
SESSION['winner'] = None
SESSION['action_message'] = None

if SESSION.get('dead_morpions') is None:
    SESSION['dead_morpions'] = []

# Initialisation des nombreuses conditions pour différencier les actions effectuées par les joueurs

POST_grid = 'grid_morpion_row' in POST and 'grid_morpion_col' in POST
morpion_choice_menu = 'morpion' in POST
is_morpion_choice_in_menu = SESSION['morpion'] is not None
morpion_target_grid = SESSION['current_action']['target_row'] is not None
morpion_choice_grid = SESSION['current_action']['actor_row'] is not None and SESSION['current_action']['target_row'] is None
action_type_choice = 'choix' in POST
spell_choice = 'choix_sort' in POST
team_color_choice = 'couleurJoueur1' in POST and 'couleurJoueur2' in POST

first_click_on_grid = POST_grid and not morpion_target_grid and SESSION['current_action']['actor_row'] is None
second_click_on_grid = POST_grid and morpion_choice_grid

print("POST RECU : ", POST)
print(f"first_click_on_grid: {first_click_on_grid}, second_click_on_grid: {second_click_on_grid}")
print(f"SESSION['current_action']: {SESSION['current_action']}")

if SESSION['team_joueur1'] is None and int(SESSION['dimension']) == 3:

    # Test si l'equipe de morpion des joueurs existe déjà
    teamJoueur1 = generate_random_morpions(6)
    teamJoueur2 = generate_random_morpions(6)

    add_player_name_to_morpion(teamJoueur1,SESSION['joueur1'])
    add_player_name_to_morpion(teamJoueur2,SESSION['joueur2'])
    
    SESSION['team_joueur1'] = to_dict_morpions_list(teamJoueur1)
    SESSION['team_joueur2'] = to_dict_morpions_list(teamJoueur2)


elif SESSION['team_joueur1'] is None and int(SESSION['dimension']) == 4:

    # Test si l'equipe de morpion des joueurs existe déjà
    teamJoueur1 = generate_random_morpions(8)
    teamJoueur2 = generate_random_morpions(8)

    add_player_name_to_morpion(teamJoueur1,SESSION['joueur1'])
    add_player_name_to_morpion(teamJoueur2,SESSION['joueur2'])

    SESSION['team_joueur1'] = to_dict_morpions_list(teamJoueur1)
    SESSION['team_joueur2'] = to_dict_morpions_list(teamJoueur2)

if team_color_choice and not action_type_choice and not morpion_choice_menu and not POST_grid:

    SESSION['tour'] = 1
    couleurJoueur1 = POST['couleurJoueur1'][0]
    couleurJoueur2 = POST['couleurJoueur2'][0]

    SESSION['couleurJoueur1'] = couleurJoueur1
    SESSION['couleurJoueur2'] = couleurJoueur2

    joueur1 = Joueur(SESSION['joueur1'],from_dict_morpions_list(SESSION['team_joueur1']),couleurJoueur1)
    joueur2 = Joueur(SESSION['joueur2'],from_dict_morpions_list(SESSION['team_joueur2']),couleurJoueur2)

    dimension = int(SESSION['dimension'])

    jeu = JeuGUI(dimension, joueur1, joueur2)

    jeu.choose_Current_Player()

    SESSION['game'] = jeu.to_dict()

if action_type_choice:
    action_type = POST['choix'][0]
    # On convertit les noms français en noms anglais pour la logique
    if action_type == 'attaque':
        action_type = 'attack'
    elif action_type == 'sort':
        action_type = 'spell'
    SESSION['action_type'] = action_type
    SESSION['current_action']['type'] =  action_type
    SESSION['action_message'] = None
    # On réinitialise les coordonnées pour une nouvelle action
    SESSION['current_action']['actor_row'] = None
    SESSION['current_action']['actor_col'] = None
    SESSION['current_action']['target_row'] = None
    SESSION['current_action']['target_col'] = None

    print(SESSION['current_action'])

if spell_choice:
    spell = POST['choix_sort'][0]
    SESSION['spell'] = spell
    SESSION['current_action']['spell'] = SESSION['spell']

# Ici, on fait la première sélection (1er choix de morpion pour l'action a exécuter)
if first_click_on_grid:

    row = int(POST.get("grid_morpion_row")[0])
    col = int(POST.get("grid_morpion_col")[0])
    SESSION['actor_row'] = row
    SESSION['actor_col'] = col

    SESSION['current_action'] = {"type": SESSION['action_type'],
                                 "morpion": SESSION['current_action']["morpion"],
                                 "actor_row": row, 
                                 "actor_col": col,
                                 "target_row": None,
                                 "target_col": None,
                                 "spell": SESSION['current_action']['spell']
                                 }

    # Vérifications et actions pour placement
    if SESSION['current_action']['type'] == 'placement':
        tour_joueur1 = Joueur.from_dict_Joueur(SESSION['game']['joueurCourant']).nom == SESSION['joueur1'] == SESSION['current_action']["morpion"]['player']
        tour_joueur2 = Joueur.from_dict_Joueur(SESSION['game']['joueurCourant']).nom == SESSION['joueur2'] == SESSION['current_action']["morpion"]['player']
    else:
        tour_joueur1 = False
        tour_joueur2 = False

    if(tour_joueur1):
        if SESSION['current_action']['type'] == 'placement':
                action = Action(Grid.from_dict_grid(SESSION['game']['grid']), 
                    Joueur.from_dict_Joueur(SESSION['game']['joueurCourant']),
                    SESSION['current_action']["type"],
                    SESSION['current_action']["actor_row"],
                    SESSION['current_action']["actor_col"],
                    None,
                    None,
                    None,
                    Morpion.from_dict_morpion(SESSION['current_action']["morpion"])
                    )
                
                action_reussi = action.execute()
                print(action_reussi)
                if action_reussi:
                    jeu = JeuGUI.from_dict(SESSION['game'])
                    jeu.choose_Current_Player()
                    jeu.mortpionGrid.printGrid()
                    if jeu.mortpionGrid.is_grid_full(): print("La grille est rempli ! ")
                    
                    SESSION['game'] = jeu.to_dict()
                    
                    # Vérifier s'il y a un gagnant
                    winner = jeu.is_winner()
                    if winner is not None:
                        SESSION['game_over'] = True
                        SESSION['winner'] = winner
                        print(f"VICTOIRE : {winner} a gagné !")
                    # Vérifier si max de tours atteint
                    elif check_max_tours():
                        SESSION['game_over'] = True
                        SESSION['winner'] = "Match Nul"
                        print("Match Nul : nombre max de tours atteint !")

                    JeuGUI.from_dict(SESSION['game']).choose_Current_Player()
                SESSION['current_action'] = {"type": None, 
                                "morpion": None, 
                                "actor_row": None, 
                                "actor_col" : None, 
                                "target_row" : None, 
                                "target_col": None,
                                "spell": None
                                }

    elif(tour_joueur2):
        if SESSION['current_action']['type'] == 'placement':
                action = Action(Grid.from_dict_grid(SESSION['game']['grid']), 
                    Joueur.from_dict_Joueur(SESSION['game']['joueurCourant']),
                    SESSION['current_action']["type"],
                    SESSION['current_action']["actor_row"],
                    SESSION['current_action']["actor_col"],
                    None,
                    None,
                    None,
                    Morpion.from_dict_morpion(SESSION['current_action']["morpion"])
                    )

                action_reussi = action.execute()
                print(action_reussi)
                if action_reussi:
                    jeu = JeuGUI.from_dict(SESSION['game'])
                    jeu.choose_Current_Player()

                    SESSION['game'] = jeu.to_dict()
                    
                    # Vérifier s'il y a un gagnant
                    winner = jeu.is_winner()
                    if winner is not None:
                        SESSION['game_over'] = True
                        SESSION['winner'] = winner
                        print(f"VICTOIRE : {winner} a gagné !")
                    # Vérifier si max de tours atteint
                    elif check_max_tours():
                        SESSION['game_over'] = True
                        SESSION['winner'] = "Match Nul"
                        print("Match Nul : nombre max de tours atteint !")
                    SESSION['game'] = jeu.to_dict()

                    JeuGUI.from_dict(SESSION['game']).choose_Current_Player()
                SESSION['current_action'] = {"type": None, 
                                "morpion": None, 
                                "actor_row": None, 
                                "actor_col" : None, 
                                "target_row" : None, 
                                "target_col": None,
                                "spell": None
                                }

    print(f'FIRST CLICK ------')

# Ici, on fait la dernière sélection (2ème choix du morpion pour l'action a exécuter)
if second_click_on_grid:

    target_row = int(POST.get("grid_morpion_row")[0])
    target_col = int(POST.get("grid_morpion_col")[0])

    SESSION['current_action']["target_row"] = target_row
    SESSION['current_action']["target_col"] = target_col

    if SESSION['current_action']['type'] in ('attack','spell'):
        if SESSION['current_action']['type'] == 'attack':
            print("ENTREE BLOC ATTACK")
            grid_action = Grid.from_dict_grid(SESSION['game']['grid'])
            action = Action(grid_action,
                Joueur.from_dict_Joueur(SESSION['game']['joueurCourant']),
                SESSION['current_action']["type"],
                SESSION['current_action']["target_row"],
                SESSION['current_action']["target_col"],
                SESSION['current_action']["actor_row"],
                SESSION['current_action']["actor_col"],
                None,
                None
                )
            print(action)
            action_reussi = action.execute()
            print(f"Action réussie : {action_reussi}")
            if action_reussi:
                # Capturer le message d'attaque (hit ou miss)
                if hasattr(action, 'attack_message'):
                    SESSION['action_message'] = action.attack_message
                # Mettre à jour la grille dans SESSION['game']
                SESSION['game']['grid'] = grid_action.to_dict_grid()
                jeu = JeuGUI.from_dict(SESSION['game'])
                
                # Vérifier et retirer les morpions morts AVANT choose_Current_Player
                for row in range(jeu.mortpionGrid.dimension):
                    for col in range(jeu.mortpionGrid.dimension):
                        morpion = jeu.mortpionGrid.playGround[row, col].morpionPlayer
                        if morpion and morpion.hp <= 0:
                            # Tracker le morpion mort
                            dead_id = (morpion.id_morpion, morpion.player)
                            if dead_id not in SESSION['dead_morpions']:
                                SESSION['dead_morpions'].append(dead_id)
                            jeu.mortpionGrid.remove_morpion(row, col)
                            print(f"Morpion mort! Case [{row},{col}] libérée.")
                
                jeu.choose_Current_Player()
                SESSION['game'] = jeu.to_dict()
                
                # Vérifier s'il y a un gagnant (alignement)
                winner = jeu.is_winner()
                if winner is not None:
                    SESSION['game_over'] = True
                    SESSION['winner'] = winner
                    print(f"VICTOIRE : {winner} a gagné !")
                # Vérifier si max de tours atteint
                elif check_max_tours():
                    SESSION['game_over'] = True
                    SESSION['winner'] = "Match Nul"
                    print("Match Nul : nombre max de tours atteint !")

        elif SESSION['current_action']['type'] == 'spell':
            print("ENTREE BLOC SPELL")
            grid_action = Grid.from_dict_grid(SESSION['game']['grid'])
            action = Action(grid_action, 
                Joueur.from_dict_Joueur(SESSION['game']['joueurCourant']), 
                SESSION['current_action']["type"],
                SESSION['current_action']["target_row"],
                SESSION['current_action']["target_col"],
                SESSION['current_action']["actor_row"],
                SESSION['current_action']["actor_col"],
                SESSION['current_action']["spell"],
                None
                )
            print(f"Action créée: type={action.action_type}, spell={action.spell}, actor=[{action.case_actor_row},{action.case_actor_col}], target=[{action.case_target_row},{action.case_target_col}]")
            action_reussi = action.execute()
            print(f"Action réussie : {action_reussi}")
            if action_reussi:
                # Mettre à jour la grille dans SESSION['game']
                SESSION['game']['grid'] = grid_action.to_dict_grid()
                jeu = JeuGUI.from_dict(SESSION['game'])
                
                # Vérifier et retirer les morpions morts APRÈS les sorts
                for row in range(jeu.mortpionGrid.dimension):
                    for col in range(jeu.mortpionGrid.dimension):
                        morpion = jeu.mortpionGrid.playGround[row, col].morpionPlayer
                        if morpion and morpion.hp <= 0:
                            # Tracker le morpion mort
                            dead_id = (morpion.id_morpion, morpion.player)
                            if dead_id not in SESSION['dead_morpions']:
                                SESSION['dead_morpions'].append(dead_id)
                            jeu.mortpionGrid.remove_morpion(row, col)
                            print(f"Morpion mort! Case [{row},{col}] libérée.")
                
                jeu.choose_Current_Player()
                SESSION['game'] = jeu.to_dict()
                
                # Vérifier s'il y a un gagnant (alignement)
                winner = jeu.is_winner()
                if winner is not None:
                    SESSION['game_over'] = True
                    SESSION['winner'] = winner
                    print(f"VICTOIRE : {winner} a gagné !")
                # Vérifier si max de tours atteint
                elif check_max_tours():
                    SESSION['game_over'] = True
                    SESSION['winner'] = "Match Nul"
                    print("Match Nul : nombre max de tours atteint !")
        
        SESSION['current_action'] = {"type": None, 
                                "morpion": None, 
                                "actor_row": None, 
                                "actor_col" : None, 
                                "target_row" : None, 
                                "target_col": None,
                                "spell": None
                                }
    print(f'SECOND CLICK + {SESSION["current_action"]}')


if action_type_choice and morpion_choice_menu and first_click_on_grid:
    print("CHOIX DU MORPION A PLACER ---------------")

if morpion_choice_menu:
    morpion = POST.get("morpion", [""])[0]

    print(type(morpion))
    SESSION['current_action']["morpion"] = json.loads(morpion)
    print(morpion)


# Calculer le numéro de tour à partir du compteur
if SESSION.get('game'):
    jeu_temp = JeuGUI.from_dict(SESSION['game'])
    SESSION['tour_number'] = jeu_temp.get_tour_number()
else:
    SESSION['tour_number'] = 0

# Récupérer les morpions déjà placés pour chaque équipe
SESSION['placed_morpions_joueur1'] = get_placed_morpions_for_player(SESSION.get('joueur1', ''))
SESSION['placed_morpions_joueur2'] = get_placed_morpions_for_player(SESSION.get('joueur2', ''))

# if SESSION['action_type'] == 'placement':

# SESSION['game'] = jeu.to_dict()   # On sauvegarde l'état du jeu