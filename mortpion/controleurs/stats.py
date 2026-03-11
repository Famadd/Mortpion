from mortpion.model.model_pg import *

# Morpions existants
"""
REQUEST_VARS['morpions'] = get_morpions(SESSION['CONNEXION'])
"""

# Nombre d'instances des tables 'morpion', 'partie', 'equipe'
REQUEST_VARS['nb_instances_morpions'] = count_instances(SESSION['CONNEXION'], "morpion")[0][0]
REQUEST_VARS['nb_instances_parties'] = count_instances(SESSION['CONNEXION'], "partie")[0][0]
REQUEST_VARS['nb_instances_equipes'] = count_instances(SESSION['CONNEXION'], "equipe")[0][0]


# Top 3 des équipes ayant le plus de victoires
REQUEST_VARS['top_3_teams'] = get_top_teams(SESSION['CONNEXION'])

# Partie la plus rapide / la plus longue
REQUEST_VARS['shortest_game'] = get_shortest_game(SESSION['CONNEXION'])
REQUEST_VARS['longest_game'] = get_longest_game(SESSION['CONNEXION'])

# Nombre moyen de ligne de journalisation par mois/année
REQUEST_VARS['average_lines'] = get_average_line_nb_per_game(SESSION['CONNEXION'])

# Morpions liés à une certaine équipe (couleur)
"""
REQUEST_VARS['MORPIONS_RED'] = get_morpions_color(SESSION['CONNEXION'],"red")
REQUEST_VARS['MORPIONS_BLUE'] = get_morpions_color(SESSION['CONNEXION'],"blue")
REQUEST_VARS['MORPIONS_GREEN'] = get_morpions_color(SESSION['CONNEXION'],"green")
REQUEST_VARS['MORPIONS_YELLOW'] = get_morpions_color(SESSION['CONNEXION'],"yellow")

"""