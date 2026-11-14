import random
import sys

from lib import write_grid


def lire_options(arguments=None):
    raise NotImplementedError("P1 : lire_options")


def erreur(message):
    raise NotImplementedError("P1 : erreur")


def grille_aleatoire(nb_cells, seed):
    raise NotImplementedError("P2 : grille_aleatoire")


def lire_grille(texte):
    raise NotImplementedError("P2 : lire_grille")


def compter_voisins(grille, ligne, colonne, periodique):
    raise NotImplementedError("P3 : compter_voisins")


def generation_suivante(grille, periodique):
    raise NotImplementedError("P3 : generation_suivante")


def afficher_grille(grille, iteration):
    raise NotImplementedError("P4 : afficher_grille")


def enregistrer_png(grille, dossier, iteration):
    raise NotImplementedError("P4 : enregistrer_png")


def main():
    raise NotImplementedError("P1 : main")


if __name__ == "__main__":
    main()
