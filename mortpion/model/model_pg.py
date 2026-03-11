import psycopg
from psycopg import sql
from logzero import logger

def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def execute_other_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.rowcount
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)

def get_morpions(connexion):
    """
    Retourne tous les morpions existants dans la base de données
    """
    query = 'SELECT * FROM morpion'
    morpions = execute_select_query(connexion, query)

    """
    morpions = [list(m) for m in morpions]

    for m in morpions:
        if m[1] == None:
            m[1] = 0
    print(morpions)
    """

    return morpions

def get_teams(connexion):
    """
    Retourne toutes les equipes existants dans la base de données
    """
    query = 'SELECT * FROM equipe'
    teams = execute_select_query(connexion, query)

    teams = [list(m) for m in teams]

    print(teams)
    return teams
    
def get_morpions_color(connexion, color):
    """
    Retourne tous les morpions d'une certaine couleur
    """
    query = 'SELECT id_morpions FROM appartenir WHERE color = %s'
    morpions = execute_select_query(connexion, query, [color])

    morpions = [list(m) for m in morpions]

    print(morpions)
    return morpions

def get_top_teams(connexion):
    """
    Retourne le top 3 des équipes avec le plus grand nombre de victoire
    """
    query = 'SELECT nom, couleur, nb_victoire FROM equipe ORDER BY nb_victoire DESC LIMIT 3'
    top_3_teams = execute_select_query(connexion, query)

    top_3_teams_list = [list(m) for m in top_3_teams]

    print(top_3_teams_list)
    return top_3_teams_list

def get_shortest_game(connexion):
    """
    Retourne la partie la plus rapide
    """
    query = 'SELECT id_partie, date_debut - date_fin AS temps_partie, equipe_gagnante FROM partie ORDER BY temps_partie ASC LIMIT 1'
    shortest_game = execute_select_query(connexion, query)

    if any(shortest_game):
        shortest_game_id = shortest_game[0]
        shortest_game_time = shortest_game[1]
        shortest_game_winner = shortest_game[2]
        return list(shortest_game_id,shortest_game_time, shortest_game_winner)

    print("Aucune instance dans la base de donnée -- get_shortest_game()")
    return []

def get_longest_game(connexion):
    """
    Retourne la partie la plus rapide
    """
    query = 'SELECT id_partie, date_debut - date_fin AS temps_partie, equipe_gagnante FROM partie ORDER BY temps_partie DESC LIMIT 1'
    longest_game = execute_select_query(connexion, query)
    if any(longest_game):
        return list(longest_game[0], longest_game[1], longest_game[3])

    print("Aucune instance dans la base de donnée -- get_longest_game()")
    return []

def get_average_line_nb_per_game(connexion):
    """
    Retourne le nombre moyen de ligne de journalisation des parties par mois, annee
    """

    """
    EXPLICATION REQUETE :

        On fait une sous requete qui selectionne l'id des parties et tous les journaux (lignes) lié à cette partie
        On joint les resultats de cette requete avec la table partie, càd qu'on a une nouvelle table qui contient id_partie et journal_count
        (le nombre de ligne de journalisation pour cette partie)

        Dans cette nouvelle table on selectionne :
        l'annee (annee),
        le mois (mois),
        la moyenne des lignes de journalisation (AVG(journal_count))

        Pour finir, on regroupe les resultats par mois, annee
        on ordonne les resultats par annee décroissante, mois décroissant pour garder une cohérence de le
    """

    query = (
    "SELECT EXTRACT(MONTH FROM p.date_debut) AS mois, "
    "EXTRACT(YEAR FROM p.date_debut) AS annee, "
    "AVG(journal_count) AS nb_moyen_lignes "
    "FROM (SELECT id_partie, COUNT(*) AS journal_count FROM Journal GROUP BY id_partie) j "
    "JOIN Partie p ON p.id_partie = j.id_partie "
    "GROUP BY mois, annee ORDER BY annee DESC, mois DESC"
)
    average_lines = execute_select_query(connexion, query)
    if any(average_lines):
        return average_lines
    
    print("Aucune instance dans la base de donnée -- get_average_line_nb_per_game()")
    return []

def get_episodes_for_num(connexion, numero):
    """
    Retourne le titre des épisodes numérotés numero
    Integer numero : numéro des épisodes
    """
    query = 'SELECT titre FROM episodes where numéro=%s'
    return execute_select_query(connexion, query, [numero])

def get_serie_by_name(connexion, nom_serie):
    """
    Retourne les informations sur la série nom_serie (utilisé pour vérifier qu'une série existe)
    String nom_serie : nom de la série
    """
    query = 'SELECT * FROM series where nomsérie=%s'
    return execute_select_query(connexion, query, [nom_serie])

def insert_team(connexion, color):
    """
    Insère une nouvelle équipe dans la BD
    String color : couleur de l'équipe créee
    Retourne le nombre de tuples insérés, ou None
    """
    query = 'INSERT INTO equipe VALUES(%s)'
    return execute_other_query(connexion, query, [color])

def insert_morpion_appartenir_equipe(connexion, id, color):
    """
    Insère une nouvelle série dans la BD
    String nom_serie : nom de la série
    Retourne le nombre de tuples insérés, ou None
    """
    insert_team(connexion, color)
    query = 'INSERT INTO appartenir VALUES(%s)'
    return execute_other_query(connexion, query, [id, color])

def insert_serie(connexion, nom_serie):
    """
    Insère une nouvelle série dans la BD
    String nom_serie : nom de la série
    Retourne le nombre de tuples insérés, ou None
    """
    query = 'INSERT INTO series VALUES(%s)'
    return execute_other_query(connexion, query, [nom_serie])

def get_table_like(connexion, nom_table, like_pattern):
    """
    Retourne les instances de la table nom_table dont le nom correspond au motif like_pattern
    String nom_table : nom de la table
    String like_pattern : motif pour une requête LIKE
    """
    motif = '%' + like_pattern + '%'
    nom_att = 'nomsérie'  # nom attribut dans séries (à éviter)
    if nom_table == 'actrices':  # à éviter
        nom_att = 'nom'  # nom attribut dans actrices (à éviter)
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.Identifier(nom_table),
        sql.Identifier(nom_att),
        sql.Placeholder())
    #    like_pattern=sql.Placeholder(name=like_pattern))
    return execute_select_query(connexion, query, [motif])



