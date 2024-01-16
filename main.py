#!/bin/python3
# -*- coding: utf-8 -*-

""" 
    Ce que l'on peut ecrire sur le terminal depuis le dossier Projet_MTdV2023 :
    $ python main.py ./TSV/fichier.tsv
    
    exemple de fichier écrit par le groupe 2 pour utiliser le gestionnaire de noms de mémoires 
    pendant la lecture du fichier TSV
"""

from typing import List, Dict
from pprint import pprint
from collections import defaultdict
from groupe2_gestionVariables import GestionnaireVariables
from memory_manager import MemoryManager
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


def affectations_variables(fichier_tsv: list) -> Dict[str, Dict]:
    """lit le fichier une première fois pour extaire 
    les colonnes « affectations » et leur « numéro d'instruction »

    Args:variables
        fichier_tsv (list): fichier tsv avec les instructions mtdV+

    Returns:
        dict(dict): { instruction_n : { "G" : variable, "D" : valeur }
    """
    # on nettoie le fichier pour ne garder que les affectations
    lines = [line.rstrip().split("\t") for line in fichier_tsv if line.rstrip().split("\t")[5] == "affectation"]

    # 'affectations' contiendra l'affectation de chaque variable
    affectations = {}
    for line in lines:
        instruction_n, token, position = line[4], line[2], line[6]  # position = G, M ou D

        if instruction_n not in affectations.keys() and position == "G":
            # nouvelle instruction
            # token est forcément le variable en cours d'affectation
            affectations[instruction_n] = { 'G' : token }
        elif instruction_n in affectations.keys() and position == "D" and position not in affectations[instruction_n].keys() :
            # il s'agit de la première valeur
            affectations[instruction_n]['D'] = token
        elif instruction_n in affectations.keys() and position == "D" and position in affectations[instruction_n].keys() :
            # s'il s'agit de la deuxième valeur
            affectations[instruction_n]['D'] += " " + token
        elif instruction_n in affectations.keys() and position == "M":
            pass
        else:
            print("erreur dictionnaire 'affectations' dans la fonction affectation variables")

    return affectations
    
def afficher_triviaux(fichier_tsv: list) -> Dict[str, Dict] :
    """
    Cette fonction permet d'afficher les instructions triviales du fichier TSV.

    Args:
        fichier_tsv (list): fichier tsv avec les instructions mtdV+
    Returns:
        dict(dict): { instruction_n : { '-' : token }
    """
    # nettoyer le fichier pour ne garder que les triviaux
    lines = [line.rstrip().split("\t") for line in fichier_tsv if line.rstrip().split("\t")[5] == "MTdV"]
    
    # 'triviaux' contiendra le caractère trivial et '-' car il n'a pas de position (G,D,M) et sera ignoré
    triviaux = {}
    for line in lines:
    	# récupérer les valeurs depuis leurs colonnes
        instruction_n, token, position = line[4], line[2], line[6] # position = - (car pas de position)
        if instruction_n not in triviaux.keys() and position == "-":
            triviaux[instruction_n] = { '-' : token }
        else:
            print("erreur dictionnaire 'triviaux' dans la fonction triviaux variables")
    
    return triviaux

# on a essayé de prendre en compte les boucles
# notre logique n'est peut-être pas parfaite, n'hésitez pas à nous le dire !
def suppression_variables(fichier_tsv: list) -> Dict[str, Dict]: 
    
    """lit le fichier une première fois pour extaire 
    les endroits où supprimer des variables inutiles

    Args:variables
        fichier_tsv (list): fichier tsv avec les instructions mtdV+

    Returns:
        dict(dict): { instruction_n : [variables à supprimer]
    """
    # on nettoie le fichier pour ne garder que les variables
    lines = [line.rstrip().split("\t") for line in fichier_tsv if line.rstrip().split("\t")[3] == "variable"]

    # 'dict' contiendra les infos de suppression pour chaque variable
    dict = {}
    for line in lines:
        token, instruction_n, scope_boucle = line[2], line[4], line[7]
        if token not in dict.keys() and scope_boucle == '-':
            dict[token] = str(int(instruction_n) + 1)
        elif token in dict.keys() and scope_boucle == '-':
            dict[token] = str(int(instruction_n) + 1)
        elif scope_boucle != '-':
            dict[token] = scope_boucle
        else:
            print("erreur dictionnaire 'dict' dans la fonction suppression variables")
    
    # 'suppressions' contiendra les numéros d'instructions où supprimer chaque variable  
    # c'est le dictionnaire qu'on va utiliser ensuite   
    suppressions = {}
    for variable in dict.keys():
        if dict[variable] not in suppressions.keys():
            suppressions[dict[variable]] = [variable]
        else:
            suppressions[dict[variable]].append(variable)

    return suppressions


def lectureTSV(tsv: list, affectations: dict, suppressions: dict, variables: GestionnaireVariables, memoire: MemoryManager):
    """lecture du fichier TSV,
    mise à jour des gestionnaires,
    et génération du code machine mtdV

    Args:
        fichier_tsv (list): fichier tsv avec les instructions mtdV+
        affectations (dict): dictionnaire des affectations, utile pour la mise à jour
                            des gestionnaires
        suppressions (dict): dictionnaire des suppressions de variables
        variables (GestionnaireVariables) : gestionnaire des noms de variable
    """

    for line in tsv:
        # 'num_instruction' (str) correspond à 'instruction_n' dans le fichier tsv
        num_instruction = line.rstrip().split("\t")[4]

        # s'il s'agit d'une affectation, c'est au tour du groupe 2 et 3 de commencer !
        if line.rstrip().split("\t")[5] == "affectation":
            
            # on gère les affectations
            if num_instruction in affectations.keys():
                # l'instruction n'a pas encore été géré
                nom_variable = affectations[num_instruction]['G']
                # vérifier si la variable n'existe pas

                if not variables.doesVariableExist(nom_variable):
                    # on l'ajoute au gestionnaire de noms de variable
                    variables.addVariable(nom_variable, memoire.get_adress(nom_variable))
                else:
                    # la variable existe déjà dans le gestionnaire
                    pass

                # maitenant que l'affectation a été gérer par groupe 2, c'est bon !
                # on peut supprimer l'entrée dans le dictionnaire d'affectations
                del affectations[num_instruction]
                
            # on gère les suppressions
            elif num_instruction in suppressions.keys():
                # il est temps de supprimer la variable car elle n'est utilisée nul part
                for nom_variable in suppressions[num_instruction]:
                    # suppression de la variable dans le gestionnaire des noms de variables
                    variables.deleteVariable(nom_variable)
                
                # maitenant que la suppression a été gérer par groupe 2 et 3, c'est bon !
                # on peut supprimer l'entrée dans le dictionnaire de suppressions
                del suppressions[num_instruction]

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
    print("affectations")
    pprint(affectations)
    
    # 'suppressions' est un dictionnaire avec toutes les
    # informations sur les suppressions de variable
    # pour faciliter le travail de lecture du TSV
    suppressions = suppression_variables(fichier_tsv)
    print("suppressions")
    pprint(suppressions)
    
    # 'triviaux' est un dictionnaire avec toutes les
    # informations sur les caractères triviaux
    # pour faciliter le travail de lecture du TSV
    triviaux = afficher_triviaux(fichier_tsv)
    print("triviaux")
    pprint(triviaux)
    
    # initialisation du gestionnaire de mémoires
    memoire = MemoryManager(affectations)

    # là ou tout se passe
    lectureTSV(fichier_tsv, affectations, suppressions, variables, memoire)

    # nous avons un module pour effacer complètement
    # ce qu'il y a dans le gestionnaire de noms de variable
    # comme cela se ferait à la fin d'une compilation
    variables.effacementGestionnaire()

    # on vérifie que tout à bien été effacé
    variables.printVariables()
