from mortpion.model.model_pg import get_teams
from model.classes import *


if POST:

    GUInomJoueur1 = POST['joueur1'][0] 
    GUInomJoueur2 = POST['joueur2'][0]
    GUIdimension = int(POST['dimension'][0])
    GUImaxTours = int(POST.get('max_tours', ['10'])[0])  
    print(GUInomJoueur1)
    print(GUInomJoueur2)
    SESSION['joueur1'] = GUInomJoueur1
    SESSION['joueur2'] = GUInomJoueur2
    SESSION['dimension'] = GUIdimension
    SESSION['max_tours'] = GUImaxTours

    SESSION['team_joueur1'] = None
    SESSION['team_joueur2'] = None



    print("POST DES JOUEURS FONCTIONNEL ICI")

