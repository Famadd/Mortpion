# Fichier grid.py (Plateau du jeu)

import numpy as np
from .case import Case



class Grid:

    def __init__(self, dimension):
        if dimension != 3 and dimension != 4:
            raise ValueError("Dimension de grille invalide : doit être 3 ou 4.")

        self.dimension = dimension
        self.playGround = np.empty((dimension, dimension), dtype=object)

        for i in range(dimension):
            for j in range(dimension):
                self.playGround[i,j] = Case(i,j)

    def add_morpion(self, row, col, morpion):
        return self.playGround[row,col].add_morpion(morpion)

    def to_dict_grid(self):
        return {
            'dimension': self.dimension,
            'playGround' : self.playGround
        }
    
    def from_dict_grid(grid_data):

        if isinstance(grid_data, Grid):
            return grid_data
    
        grid = Grid(grid_data['dimension'])
        grid.playGround = grid_data['playGround']

        return grid

    def get_morpion_player(self, row, col):
        return self.playGround[row,col].get_morpion_player()

    def remove_morpion(self, row, col):
        return self.playGround[row, col].remove_morpion()

    def destroy_case(self, row, col):
        return self.playGround[row, col].destroy_case()

    def get_neighbours(self, row, col):
        adj = []
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        for (dr, dc) in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < self.playGround.shape[0] and 0 <= c < self.playGround.shape[1]:
                adj.append(self.playGround[r,c])
        
        return adj

    def is_grid_full(self):
        for i in range(self.playGround.shape[0]):
            for j in range(self.playGround.shape[1]):
                case = self.playGround[i,j]
                # vérif si la case est vide
                if case.morpionPlayer is None:  
                    return False
        return True
    
    def printGrid(self):
        dimension = self.playGround.shape[0]

        for i in range(dimension):  # lignes
            row_display = []
            for j in range(dimension):  # colonnes
                if not self.playGround[i,j].state:
                    row_display.append("A")
                elif self.playGround[i,j].morpionPlayer is not None:
                    row_display.append("M")
                else:
                    row_display.append("0")
            print(" | ".join(row_display))
            if i < dimension - 1 :
                print("---" * dimension + "-")