#!/bin/python3
# -*- coding: utf-8 -*-

""" 
    Ce que l'on peut ecrire sur le terminal depuis le dossier Projet_MTdV2023 :
    $ python groupe2_lectureTSV.py ./TSV/fichier.tsv
    
    Ce fichier lit les fichiers tsv et et met à jour le gestionnaire de noms de variables au fur et à mesure.
    Je ne sais pas encore il peut être utilisé par les autres groupes, mais j'essaye d'écrire le maximum
    de fonctions qui peuvent être utilile par les autres groupes. 
    Les groupes 3, puis 4 devront surement partir de ce fichier pour rajouter leurs modules.
    
    TO DO LIST :
        - continuer de lire le fichier tsv pour arriver à lire les lignes 
            et modifier le gestionnaire de noms de variables
        - pour l'instant, l'adresse est 0 à l'initialisation, 1 si on le modifie 
            (cela le restera que le groupe 3 n'aura pas fait leur gestionnaire)
        - faire attention à bien commenter les fonctions
        - ne pas hésiter à rajouter des si else pour prendre en compte les possibles erreurs
            - \033[91 permet d'écrire en rouge sur le terminal
            - \033[0m pour redevenir normal
            - \033[92 permet d'écrire en vert sur le terminal
"""

from groupe2_GestionVariables import GestionnaireVariables
import os
import sys

def getTSV(path: str) -> str:
    """ verifie que le chemin est correcte 
        et renvoie le contenu du fichier tsv

    Args:
        path (str): chemin vers le fichier tsv

    Returns:
        str: contenu du fichier tsv
    """

    # on vérifie que le chemin existe
    if not os.path.exists(path):
        print("\033[91mLe fichier {} n'existe pas.\033[0m".format(path)) # affiche en rouge
        sys.exit(1)
    # alors on vérifie que le chemin renvoie bien un fichier
    elif not os.path.isfile(path):
        print("\033[91mLe chemin {} ne renvoie pas vers un fichier.\033[0m".format(path)) # affiche en rouge
        sys.exit(1)
    # alors on récupère le fichier
    else:
        with open(path, "r", encoding="ASCII") as f :
            return f.read()

if __name__ == "__main__":
    
    # on vérifie le nombre d'arguments
    if len(sys.argv) != 2 :
        print("\033[91mIl manque le chemin vers le fichier tabulaire.") # affiche en rouge
        print("Usage:\n\t$ python groupe2_lectureTSV.py .\\TSV\\fichier.tsv\033[0m")
        sys.exit(1)
    
    # 'fichier' est une variable str contenant le fichier tsv
    fichier = getTSV(sys.argv[1])
    
    # 'variables' est le gestionnaire de noms de variable
    # à l'initialisation, il est vide
    variables = GestionnaireVariables()
    
    print(fichier)
    variables.getVariables