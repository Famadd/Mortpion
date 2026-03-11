# Fichier morpion.py (Morpion jouable)

import ast
import json
import random


class Morpion:

    def __init__(self, id_morpion, point_hp, point_att, point_mana, point_hit):
        self.id_morpion = id_morpion
        self.hp = point_hp
        self.att = point_att
        self.mana = point_mana
        self.hit = 10 * point_hit
        self.player = None
        self.morpionTeam = None
        self.morpionColor = None
        random_img = random.randint(1,16)
        self.img_path = f"/static/img/t{random_img}.png"

    
    def to_dict_morpion(self):
        return {
            'id_morpion': self.id_morpion,
            'hp': self.hp,
            'att': self.att,
            'mana': self.mana,
            'hit': self.hit,
            'player': self.player,
            'morpionTeam': self.morpionTeam,
            'morpionColor': self.morpionColor,
            'img_path' : self.img_path
        }

    def from_dict_morpion(morpion_data):

        if isinstance(morpion_data, Morpion):
            return morpion_data

        morpion = Morpion(
            morpion_data["id_morpion"],
            morpion_data["hp"],
            morpion_data["att"],
            morpion_data["mana"],
            morpion_data["hit"] // 10
            )
        morpion.player = morpion_data["player"]
        morpion.morpionTeam = morpion_data['morpionTeam']
        morpion.morpionColor = morpion_data['morpionColor']
        morpion.img_path = morpion_data['img_path']

        return morpion

    def get_player(self):
        return self.player
    
    def check_alive(self):
        return self.hp > 0

    def hit_Success(self):
        if self.hit > random.randint(0,100):
            return True
        else:
            return False

    def attack(self, enemy):
        if self.hit_Success():
            enemy.hp = max(0,enemy.hp - self.att)
            self.hit += 0.5
            return {'success': True, 'message': f'{self.player} a touché {enemy.player} pour {self.att} dégâts !'}
        else:
            self.hit += 0.2
            return {'success': False, 'message': f'{self.player} a raté son attaque contre {enemy.player} !'}

    def fire_ball_spell(self, enemy):
        if self.mana >= 2 :
            enemy.hp = max(0,enemy.hp - 3)
            self.hit += 0.5
            self.mana -= 2
            return True
        print("Vous n'avez pas assez de mana pour lancer le sort fire_ball")
        return False
    
    def healing_spell(self, ally):
        if self.mana >= 1 :
            ally.hp = ally.hp + 2
            self.hit += 0.5
            self.mana -= 1
            return True
        print("Vous n'avez pas assez de mana pour lancer le sort heal !")
        return False

    def armageddon_spell(self, enemy):
        if self.mana >= 5:
            if enemy is not None:
                enemy.hp = 0
            self.hit += 0.5
            self.mana -= 5
            return True
        return False
