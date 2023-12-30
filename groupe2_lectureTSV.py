#!/bin/python3
# -*- coding: utf-8 -*-

""" 
    Ce que l'on peut ecrire sur le terminal depuis le dossier Projet_MTdV2023 :
    $ python groupe2_lectureTSV.py ./TSV/fichier.tsv
    
    Ce fichier lit les fichiers tsv et et met à jour le gestionnaire de noms de variables au fur et à mesure.
    Je ne sais pas encore il peut être utilisé par les autres groupes, mais j'essaye d'écrire le maximum
    de fonctions qui peuvent être utile par les autres groupes. 
    Les groupes 3, puis 4 devront surement partir de ce fichier pour rajouter leurs modules.
    
    # info du groupe 2 pour groupe 3 : pour l'instant, on donne comme adresse 0 ou 1 pour les tests
    Nous attendons votre module pour reprendre cette partie-là !

    # question du groupe 2 pour groupe 4 : comment sera gérer le test "==" ?
    
    # info du groupe 2 pour les groupes 3 et 4 :
    lorsque rencontre d'une variable, on fait variables.doesVariableExist()
    - si True, la variable existe dans le gestionnaire de noms de variable
    => réallocation ? Nous on ne fait rien pour l'instant
    - si False, la variable n'existe pas dans le gestionnaire
    => pour le groupe 3, on a besoin que vous créiez une adresse pour la variable,
        quelque chose comme memoires.createAdresse("nomvar")
        de sorte que nous puissons faire quelque chose comme ceci 
        variables.addVariable("nomvar", memoires.getAdresse("nomvar"))
    
    TO DO LIST :
        - faire attention à bien commenter les fonctions
        - ne pas hésiter à rajouter des si else pour prendre en compte les possibles erreurs
            - \033[91 permet d'écrire en rouge sur le terminal
            - \033[0m pour redevenir normal
            - \033[92 permet d'écrire en vert sur le terminal
"""

from typing import List
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


def extract_dict(fichier_tsv):
    """_summary_

    Args:
        fichier_tsv (_type_): _description_
    
    Returns:
        _type_: _description_
    """
    result_dict = defaultdict(lambda: defaultdict(str))
    lines = [line.rstrip().split('\t') for line in fichier_tsv if line.rstrip().split('\t')[5] == 'affectation']
    ''' rajout «test» ?  '''
    for line in lines:
        key, inner_key, value = int(line[1]), line[6], line[2] # instruction_num, position, variable
        if key not in result_dict:
           result_dict[key] = {}
        if inner_key in result_dict[key]:
            result_dict[key][inner_key] += ' '+value
        else:
            result_dict[key][inner_key] = value

    return(dict(result_dict))


# extract 
def extract_vars(var_dict):

    # 'variables' est le gestionnaire de noms de variable
    # à l'initialisation, il est vide
    variables = GestionnaireVariables()
    variables.getVariables

    for instruction in var_dict:
        var = var_dict[instruction]['G']
        #pour affectation M toujours = et test M toujours == ??
        # qui récup "D" les valeurs 

        # vérifier si 'var' existe déjà 
        if not variables.doesVariableExist(var):
            variables.addVariable(var)
        # else re-assign ?

        # allouer adresseMémoire ? appel fonction groupe3 ?
        # valeur 'D'
        value = var_dict[instruction]['D']
        if not value.isnumeric():
            # c'est une affectation plus longue type [x+y, x+y+z, x+1+y, x+2, ...]
            # et chaque valeur alterné depuis 1er est:  soit variable , soit int
                # on part du principe chaque valeur alterné depuis le 2eme est opérateur 
            
            # vérifie syntaxe ## à discuter si utile ou pas
            value = value.split() 
            print(f'value = {value}')
            operators = ['+', '*', '-' ] # les opérateur permis pour 'D' donc sans = ou ==
            for is_val in value[0::2]:
                if is_val.isnumeric() :
                    is_val = int(is_val)
                    print(type(is_val).__name__)
                    if type(is_val).__name__ not in ['int', 'str']:
                        if value[1: :2] not in operators :
                            print(f'invalid syntax')
                    elif type(is_val).__name__ == 'str' and not variables.doesVariableExist(is_val):
                        print(f'Erreur, {is_val} utilisé avant son affectation.')
                    
                
        '''   reste à gérér réallocation x = x+y , mais fatiguée pour aujourd'hui'''

if __name__ == "__main__":
    
    # on vérifie le nombre d'arguments
    if len(sys.argv) != 2 :
        print("\033[91mIl faut le chemin vers le fichier tabulaire.") # affiche en rouge
        print("Usage:\n\t$ python groupe2_lectureTSV.py .\\TSV\\fichier.tsv\033[0m")
        sys.exit(1)
    
    # 'fichier_tsv' est une liste contenant le fichier tsv
    # on garde le contenu du fichier sans le titre
    fichier_tsv = getTSV(sys.argv[1])[1:]
    var_dict = extract_dict(fichier_tsv)  # { num_instruction : {'G': var , 'M': = , 'D'= valeur }}
    pprint(var_dict)
    extract_vars(var_dict) # là ou tout se passe 