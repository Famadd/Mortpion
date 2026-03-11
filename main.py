from model.classes import Jeu, Joueur
from controleurs.equipe import GUInomJoueur1, GUInomJoueur2, GUIdimension

def main():

    # Initialiser le modèle (Console)
    """
    joueur1 = Joueur(input("nom" + "\n"))        # Recupérer le nom des joueurs via l'interface graphique
    joueur2 = Joueur(input("nom" + "\n"))
    dimension = int(input("dimension" + "\n"))       # Recupérer la dimension via l'interface graphique

    game = Jeu(dimension, joueur1, joueur2)

    game.mortpion_Game_console()

    """

    joueur1 = Joueur(GUInomJoueur1)
    joueur2 = Joueur(GUInomJoueur2)
    dimension = GUIdimension

    game = Jeu(dimension,joueur1,joueur2)

    game.mortpion_Game_GUI()


    return 0


if __name__ == "__main__":
    main()