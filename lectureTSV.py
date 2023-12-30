#!/bin/python3
# -*- coding: utf-8 -*-

""" 
    Ce que l'on peut ecrire sur le terminal depuis le dossier Projet_MTdV2023 :
    $ python lectureTSV.py ./TSV/fichier.tsv
    
    Ce fichier lit les fichiers tsv et et met à jour le gestionnaire de noms de variables au fur et à mesure.
    Les groupes 3, puis 4 devront surement partir de ce fichier pour rajouter leurs modules.
    
    # info du groupe 2 pour groupe 3 : pour l'instant, on donne comme adresse 0 ou 1 pour les tests
    Nous attendons votre module pour reprendre cette partie-là !
    On aura certainement besoin d'un module comme memoires.getAdresse("nomvar") pour qu'on puisse faire
    variables.addVariable("nomvar", memoires.getAdresse("nomvar"))

    # question du groupe 2 pour groupe 4 : comment sera gérer le test "==" ? Nous sommes là si
    vous avez besoin d'un module supplémentaire
    lorsque rencontre d'une variable, on fait variables.doesVariableExist()
    - si True, la variable existe dans le gestionnaire de noms de variable
    
    # info pour groupe 3 et groupe 4 : nous attendons un changement une fichier tsv pour 
    pouvoir effacer les variables au fur et à mesure
    Nous créerons surement une fonction pour cela plus tard
    
    TO DO LIST de Shami :
    - enlever le M:'=' dans le dictionnaire des affectation
        => j'ai tenté de le faire, il va falloir que tu vérifie !
    
    
    TO DO LIST du groupe 2 :
        - vérifier commentaires
        - verification si on a pris le max d'erreurs
"""

from typing import List, Dict
from pprint import pprint
from collections import defaultdict
from groupe2_GestionVariables import GestionnaireVariables
import os
import sys


def getTSV(path: str) -> List[str]:
    """ verifie que le chemin est correcte 
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
        print("\033[91mLe chemin {} ne renvoie pas vers un fichier.\033[0m".format(path))
        sys.exit(1)
    # alors on récupère le fichier
    else:
        with open(path, "r", encoding="ASCII") as f :
            return f.readlines()


def affectations_variables(fichier_tsv: list) -> Dict[int, Dict]:
    """ lit le fichier une première fois pour ne garder
    que les affectations et leur numéro d'instruction

    Args:
        fichier_tsv (list): fichier tsv avec les instructions mtdV+
    
    Returns:
        dict(dict): { num_instruction : [variable, valeur] }
        soit affectations[num_instruction][0] = variable
        et affectations[num_instruction][1] = valeur

    """
    # on nettoie le fichier pour ne garder que les affectation
    lines = [line.rstrip().split('\t') for line in fichier_tsv if line.rstrip().split('\t')[5] == 'affectation']
    
    affectations = {}
    for line in lines :
        
        num_instruction = line[4]
        token = line[2] 
        position = line[6] # G, M ou D
        
        if num_instruction not in affectations.keys() and position == 'G' :
            # nouvelle instruction
            # token est forcément le variable en cours d'affectation
            affectations[num_instruction] = [token]
        elif num_instruction in affectations.keys() and position == 'D' and len(affectations[num_instruction]) == 1 :
            # il s'agit de la première valeur
            affectations[num_instruction].append(token)
        elif num_instruction in affectations.keys() and position == 'D' and len(affectations[num_instruction]) > 1 :
            affectations[num_instruction][1] += ' '+token
        elif num_instruction in affectations.keys() and position == 'M' :
            pass
        else :
            print("erreur")

    return affectations


def lectureTSV(tsv: list, affectations: dict, variables: GestionnaireVariables):
    """ lecture du fichier TSV,
    mise à jour des gestionnaires,
    et génération du code machine mtdV

    Args:
        fichier_tsv (list): fichier tsv avec les instructions mtdV+
        affectations (dict): dictionnaire des affectations, utile pour la mise à jour
                            des gestionnaires
        variables (GestionnaireVariables) : gestionnaire des noms de variable
    """

    for line in tsv :
        # 'num_instruction' (str) correspond à 'instruction_n' dans le fichier tsv
        num_instruction = line.rstrip().split('\t')[4]
        
        # s'il s'agit d'une affectation, c'est au tour du groupe 2 et 3 de commencer !
        if line.rstrip().split('\t')[5] == 'affectation' :

            if num_instruction in affectations.keys() :
                # l'instruction n'a pas encore été géré
                nom_variable = affectations[num_instruction][0]
                # vérifier si la variable n'existe pas
                
                if not variables.doesVariableExist(nom_variable) :
                    # on l'ajoute au gestionnaire de noms de variable
                    variables.addVariable(nom_variable)
                else :
                    # la variable existe déjà dans le gestionnaire
                    pass # peut-être le groupe 3 veut faire quelque chose ?

                # maitenant que l'affectation à été gérer par groupe 2 et 3, c'est bon !
                # on peut supprimer l'entrée dans le dictionnaire d'affectations
                del affectations[num_instruction]
            
            else :
                # si c'est une affectation mais que la clé d'instruction n'est plus dans le dictionnaire 
                # ça veut dire que l'affectation a déjà été géré
                pass # peut-être que le groupe 4 a besoin de faire quelque chose ici ?
            
        # s'il ne s'agit pas d'une affectation, pas de modification au niveau du gestionnaire de noms de variable
        else :
            pass # peut-être qu'un autre groupe veut faire quelque chose ?

if __name__ == "__main__":

    # on vérifie le nombre d'arguments
    if len(sys.argv) != 2 :
        print("\033[91mIl faut le chemin vers le fichier tabulaire.") # affiche en rouge
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

    # là ou tout se passe
    # groupe 3 et 4, vous allez surement devoir rajouter
    # vos trucs ici
    lectureTSV(fichier_tsv, affectations, variables) 
    
    # on vérifie que toutes les variables sont bien dans le dictionnaire
    variables.printVariables()

    # on efface ce qui reste dans le gestionnaire de noms de variable
    variables.effacementGestionnaire()
    
    # on vérifie que tout à bien été effacé
    variables.printVariables()



