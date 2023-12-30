#!/bin/python3
# -*- coding: utf-8 -*-

""" 
    Ce que l'on peut ecrire sur le terminal depuis le dossier Projet_MTdV2023 :
    $ python lectureTSV.py ./TSV/fichier.tsv
    
    Ce fichier lit les fichiers tsv MDTV+
    -Pour l'instant, il met à jour le gestionnaire de noms de variables au fur et à mesure. 
    -groupe 3 et groupe 4 => vous pouvez rajouter vos modules dans la méthode X
    
    info du groupe 2 pour groupe 3 : pour l'instant, on donne comme adresse 0 ou 1 pour les tests
    Nous attendons votre module pour rajouter la vraie adresse mémoire.
    On aura certainement besoin d'un module comme memoires.getAdresse("nomvar") pour qu'on puisse faire
    variables.addVariable("nomvar", memoires.getAdresse("nomvar"))

    question du groupe 2 pour groupe 4 : comment sera gérer le test "==" ? Nous sommes là si
    vous avez besoin d'un module supplémentaire
    
    info pour groupe 3 et groupe 4 : Nous sommes en train de voirs pour avoir une modif du fichier tsv pour 
    pouvoir effacer les variables au fur et à mesure. Nous créerons surement une fonction pour cela plus tard !
    Pour l'instant, le gestionnaire se vide à la fin du fichier.

    ### Laura, il faut s'assurer auprès des autres groupes 
        -  si fin de fichier == fin du programme (sinon problème avec suppression)

        - si ce n'est pas déjà fait (je n'ai pas tout suivi ):
            -il faut bien expliquer nos «attentes» aux groupes 3 et 4 : aka, 
            - nous proposons d'avoir un programme_commun (lectureTSV.py) 
            pour la lecture des fichiers MDTV+
            - (raison)
            - logique 
        - si jamais tu te sens inspriré de faire un .md pour expliquer le  «flow» , comme pour PPE2 
        (j'exagère je sais)
        - mais c'est TRÈS IMPORTANT de comprendre les étapes
        - sinon à 15 , danger!

"""

from typing import List, Dict
from pprint import pprint
from collections import defaultdict
from groupe2_GestionVariables import GestionnaireVariables
import os
import sys


def getTSV(path: str) -> List[str]:
    """verifie que le chemin est correcte
        et renvoie le contenu du fichier tsv

    Args:
        path (str): chemin vers le fichier tsv

    Returns:
        List[str]: contenu du fichier tsv
    """

    # on vérifie que le chemin existe
    if not os.path.exists(path):
        print("\033[91mLe fichier {} n'existe pas.\033[0m".format(path))
        sys.exit(1)
    # alors on vérifie que le chemin renvoie bien un fichier
    elif not os.path.isfile(path):
        print("\0variables33[91mLe chemin {} ne renvoie pas vers un fichier.\033[0m".format(path))
        sys.exit(1)
    # alors on récupère le fichier
    else:
        with open(path, "r", encoding="ASCII") as f:
            return f.readlines()


def affectations_variables(fichier_tsv: list) -> Dict[int, Dict]:
    """lit le fichier une première fois pour extaire 
    les colonnes « affectations » et leur « numéro d'instruction »

    Args:variables
        fichier_tsv (list): fichier tsv avec les instructions mtdV+

    Returns:
        dict(dict): { num_instruction : [variable, valeur] }
        soit affectations[num_instruction][0] = variable
        et affectations[num_instruction][1] = valeur

    """
    # on nettoie le fichier pour ne garder que les affectation
    lines = [
        line.rstrip().split("\t")
        for line in fichier_tsv
        if line.rstrip().split("\t")[5] == "affectation"
    ]

    
    affectations = {}
    for line in lines:
        num_instruction = line[4]
        token = line[2]
        position = line[6]  # G, M ou D
    
        pprint(affectations)

        if num_instruction not in affectations.keys() and position == "G":
            # nouvelle instruction
            # token est forcément le variable en cours d'affectation
            affectations[num_instruction] = [token]
        elif num_instruction in affectations.keys() and position == "D" and len(affectations[num_instruction]) == 1 :
            # il s'agit de la première valeur
            affectations[num_instruction].append(token)
        elif num_instruction in affectations.keys() and position == "D" and len(affectations[num_instruction]) > 1 :
            # s'il s'agit de la deuxième valeur
            affectations[num_instruction][1] += " " + token
        elif num_instruction in affectations.keys() and position == "M":
            pass
        else:
            print("erreur")
    # pprint(affectations)
    return affectations


def lectureTSV(tsv: list, affectations: dict, variables: GestionnaireVariables):
    """lecture du fichier TSV,
    mise à jour des gestionnaires,
    et génération du code machine mtdV

    Args:
        fichier_tsv (list): fichier tsv avec les instructions mtdV+
        affectations (dict): dictionnaire des affectations, utile pour la mise à jour
                            des gestionnaires
        variables (GestionnaireVariables) : gestionnaire des noms de variable
    """

    for line in tsv:
        # 'num_instruction' (str) correspond à 'instruction_n' dans le fichier tsv
        num_instruction = line.rstrip().split("\t")[4]

        # s'il s'agit d'une affectation, c'est au tour du groupe 2 et 3 de commencer !
        if line.rstrip().split("\t")[5] == "affectation":
            if num_instruction in affectations.keys():
                # l'instruction n'a pas encore été géré
                nom_variable = affectations[num_instruction][0]
                # vérifier si la variable n'existe pas

                if not variables.doesVariableExist(nom_variable):
                    # on l'ajoute au gestionnaire de noms de variable
                    variables.addVariable(nom_variable)
                else:
                    # la variable existe déjà dans le gestionnaire
                    pass  # peut-être le groupe 3 veut faire quelque chose ?

                # maitenant que l'affectation à été gérer par groupe 2 et 3, c'est bon !
                # on peut supprimer l'entrée dans le dictionnaire d'affectations
                del affectations[num_instruction]

            else:
                # si c'est une affectation mais que la clé d'instruction n'est plus dans le dictionnaire
                # ça veut dire que l'affectation a déjà été géré
                pass  # peut-être que le groupe 4 a besoin de faire quelque chose ici ?

        # s'il ne s'agit pas d'une affectation, pas de modification au niveau du gestionnaire de noms de variable
        else:
            pass  # peut-être qu'un autre groupe veut faire quelque chose ?


if __name__ == "__main__":
    # on vérifie le nombre d'arguments
    if len(sys.argv) != 2:
        print("\033[91mIl faut le chemin vers le fichier tabulaire.")
        print("Usage:\n\t$ python lectureTSV.py .\\TSV\\fichier.tsv\033[0m")
        sys.exit(1)

    # 'variables' est le gestionnaire de noms de variable
    # à l'initialisation, il est vide
    variables = GestionnaireVariables()

    # 'fichier_tsv' est une liste contenant le fichier tsv
    # contenu du fichier sans le titre
    fichier_tsv = getTSV(sys.argv[1])[1:]

    # 'affectations' est un dictionnaire avec toutes les
    # informations sur les affectations
    # pour faciliter le travail de lecture du TSV
    affectations = affectations_variables(fichier_tsv)
    pprint(f'affectations= {affectations}')

    # là ou tout se passe
    # groupe 3 et 4, vous allez surement devoir rajouter
    # vos trucs ici
    lectureTSV(fichier_tsv, affectations, variables)

    # on vérifie que toutes les variables sont bien dans le dictionnaire
    print(f'Impression des variables courantes :')
    variables.printVariables()

    # on efface ce qui reste dans le gestionnaire de noms de variable

    ### Laura ###
    '''
    - Je pense qu'on devrait faire cette étape (effacement)
    seulement si les autres groupes rajoutent leurs modules dans ce fichier
    - Est-ce qu'on s'est mis d'accord dessus ?
    '''
    variables.effacementGestionnaire()

    # on vérifie que tout à bien été effacé
    variables.printVariables()

