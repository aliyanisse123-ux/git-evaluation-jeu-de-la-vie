import random
import argparse
import sys

from lib import write_grid


def entier_strictement_positif(texte):
    """Convertit texte en entier > 0, sinon argparse affiche l'erreur."""
    try:
        valeur = int(texte)
    except ValueError:
        raise argparse.ArgumentTypeError(f"un entier est attendu : '{texte}'")
    if valeur <= 0:
        raise argparse.ArgumentTypeError(f"doit être strictement positif : {valeur}")
    return valeur


def entier_positif_ou_nul(texte):
    """Convertit texte en entier >= 0, sinon argparse affiche l'erreur."""
    try:
        valeur = int(texte)
    except ValueError:
        raise argparse.ArgumentTypeError(f"un entier est attendu : '{texte}'")
    if valeur < 0:
        raise argparse.ArgumentTypeError(f"doit être positif ou nul : {valeur}")
    return valeur


def lire_options(arguments=None):
    """Lit les options de la ligne de commande.

    Renvoie un objet dont les attributs sont nb_cells, max_iterations, seed,
    output_directory, output_type et periodic. arguments permet de passer
    une liste d'options pour les essais (None = la vraie ligne de commande).
    """
    parser = argparse.ArgumentParser(
        description="Simulation du jeu de la vie de Conway.",
        epilog="Sans grille sur l'entrée standard, une grille aléatoire est créée.",
    )
    parser.add_argument("-n", "--nb_cells", type=entier_strictement_positif, default=10,
                        help="nombre de cellules par côté pour une grille aléatoire (défaut : 10)")
    parser.add_argument("-m", "--max_iterations", type=entier_positif_ou_nul, default=20,
                        help="numéro de la dernière itération à calculer (défaut : 20)")
    parser.add_argument("-s", "--seed", type=int, default=42,
                        help="graine du générateur aléatoire (défaut : 42)")
    parser.add_argument("-o", "--output_directory", default="outputs",
                        help="dossier dans lequel écrire les images (défaut : outputs)")
    parser.add_argument("-t", "--output_type", choices=["image", "text"], default="image",
                        help="type de sortie : image ou text (défaut : image)")
    parser.add_argument("-p", "--periodic", action="store_true",
                        help="active les conditions aux limites périodiques")
    return parser.parse_args(arguments)

def erreur(message):
    """Écrit le message sur STDERR et arrête le programme avec le code 1."""
    print(f"Erreur : {message}", file=sys.stderr)
    sys.exit(1)

def grille_aleatoire(nb_cells, seed):
    raise NotImplementedError("P2 : grille_aleatoire")


def lire_grille(texte):
    raise NotImplementedError("P2 : lire_grille")


def compter_voisins(grille, ligne, colonne, periodique):
    if not grille or not grille[0]:
        return 0

    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])
    total = 0

    for decalage_ligne in (-1, 0, 1):
        for decalage_colonne in (-1, 0, 1):
            if decalage_ligne == 0 and decalage_colonne == 0:
                continue

            ligne_voisin = ligne + decalage_ligne
            colonne_voisin = colonne + decalage_colonne

            if periodique == True:
                ligne_voisin %= nb_lignes
                colonne_voisin %= nb_colonnes
            elif not (0 <= ligne_voisin < nb_lignes and 0 <= colonne_voisin < nb_colonnes):
                continue

            if grille[ligne_voisin][colonne_voisin] == 1:
                total += 1

    return total


def generation_suivante(grille, periodique):
    raise NotImplementedError("P3 : generation_suivante")


def afficher_grille(grille, iteration):
    raise NotImplementedError("P4 : afficher_grille")


def enregistrer_png(grille, dossier, iteration):
    raise NotImplementedError("P4 : enregistrer_png")


def main():
    """Enchaîne options, grille initiale, générations et sorties."""
    options = lire_options()

    # Une grille arrive par un pipe ou une redirection : on la lit.
    # Sinon (terminal), on crée une grille aléatoire.
    if sys.stdin.isatty():
        grille = grille_aleatoire(options.nb_cells, options.seed)
    else:
        try:
            grille = lire_grille(sys.stdin.read())
        except ValueError as exception:
            erreur(f"grille invalide : {exception}")

    # La génération 0 est la grille initiale ; on calcule jusqu'à max_iterations.
    for iteration in range(options.max_iterations + 1):
        if iteration > 0:
            grille = generation_suivante(grille, options.periodic)
        if options.output_type == "image":
            enregistrer_png(grille, options.output_directory, iteration)

    if options.output_type == "text":
        afficher_grille(grille, options.max_iterations)
    else:
        nb_images = options.max_iterations + 1
        print(f"Generation of {nb_images} images in directory {options.output_directory}")

if __name__ == "__main__":
    main()
