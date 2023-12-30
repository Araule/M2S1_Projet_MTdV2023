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

    ### Laura### , reallocation est certainement à groupe3 de gérer selon LEUR critères:
     (trop longues, corrompus etc. )
     - ce qui nous intéresse c'est une PREMIÈRE allocation d'espace, si nouvelle variable

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


def extract_dict(fichier_tsv) -> Dict[int, Dict]:
    """_summary_

    Args:
        fichier_tsv (_type_): fichier_tsv_MDTV+_groupe1
    
    Returns:
        dict(dict): {numero_instrucion : {'G' : lhs_nomvar , 'M': '=', 'D': rhs_valeur_de_nom_var}}

    ### Laura ### [ et autres  groupes ] 
    : sauf vérification des conditions pour les valeurs tel que x=x+1 (si x existe bla bla)
        que fait-on des valeurs 'rhs_valeur'
        => est-ce que groupe3 stocke valeur_de_variable(en même temps de l'adresse?)
    """
    result_dict = defaultdict(lambda: defaultdict(str))
    # pour l'instant nous traitons que les « affectations »
    lines = [line.rstrip().split('\t') for line in fichier_tsv if line.rstrip().split('\t')[5] == 'affectation']
    for line in lines:
        # instruction_num, position gauche milieu droite, valeur = int ou var_operator_int ou var_operateur_var
        lhs_var, middle_operator, rhs_value = int(line[1]), line[6], line[2] 
        if lhs_var not in result_dict:
           result_dict[lhs_var] = {}
        if middle_operator in result_dict[lhs_var]:
            result_dict[lhs_var][middle_operator] += ' '+rhs_value
        else:
            result_dict[lhs_var][middle_operator] = rhs_value

    return(dict(result_dict))


# fonction qui trouve les variables , ajou
def extract_vars(var_dict, variables):
    """_summary_

    - trouve les variables
    - ajoute_au_gestionnnaire de variable
    - demande au module_groupe3 d'allouer une espace pour cette nouvelle var
    - et je_ne_sais_quoi_d'autre...
    - qui à quelle moment gère SUPPRESSION ?

    Args:
        dictionnaire_variables_valeurs, objet_gestionnaire_nom_de_variable : _description_
    
    Returns:
        dict(dict): {numero_instrucion : {'G' : lhs_nomvar , 'M': '=', 'D': rhs_valeur}}

    ### Laura ### [ et autres  groupes ] 
    : que fait-on des valeurs 'D'
    """

    for instruction_num in var_dict:
        nom_var = var_dict[instruction_num]['G']

        # vérifier si 'var' existe déjà 
        if not variables.doesVariableExist(nom_var):
            variables.addVariable(nom_var, 0)

        # il faut certainement allouer une adresse mémoire ici 
        rhs_value = var_dict[instruction_num]['D']
        if not rhs_value.isnumeric():

            ### Laura ###
            # c'est une affectation plus longue type [x + y, x + y + z, x+1+y, x+2, ...]
            # on part du principe:
                # chaque valeur alternée depuis 1er est:  soit variable , soit int
                # chaque valeur alternée depuis le 2eme est opérateur 
                # retourne erreur si nouvelle variable est une rhs_valeur , alors qu'on ne la connait pas
                    # x = x+y =>  où «y» non connu ! 
            
            ### vérification syntaxe ##  utile ou pas ##
            rhs_value = rhs_value.split() 
            # print(f'value = {rhs_value}')
            operators = ['+', '*', '-' ] # les opérateur permis pour 'D' donc sans = ou ==
            for value_token in rhs_value[0::2]:
                if value_token.isnumeric() :
                    value_token = int(value_token)
                    # print(type(value_token).__name__)
                    if type(value_token).__name__ not in ['int', 'str']:
                        if rhs_value[1: :2] not in operators :
                            print(f'invalid syntax')
                    elif type(value_token).__name__ == 'str' and not variables.doesVariableExist(value_token):
                        print(f'Erreur, {value_token} utilisé avant son affectation.')
            '''
            -Ici, une fois syntaxe vérifié qu'est-ce qui reste à faire ?
            - à priori : nouvelle variable gérée 
            - il faut que qqun récup 'D'
            - faut-il faire une méthode/fonction qui puisee retourner la valeur
            - je sais nous ne nous occupons pas des valeurs 
            - mais qqun le stocke ?
            '''        

if __name__ == "__main__":
    
    # on vérifie le nombre d'arguments
    if len(sys.argv) != 2 :
        print("\033[91mIl faut le chemin vers le fichier tabulaire.") # affiche en rouge
        print("Usage:\n\t$ python groupe2_lectureTSV.py .\\TSV\\fichier.tsv\033[0m")
        sys.exit(1)

    # 'variables' est le gestionnaire de noms de variable
    # à l'initialisation, il est vide
    variables = GestionnaireVariables()
    #variables.getVariables
    
    # 'fichier_tsv' est une liste contenant le fichier tsv
    # contenu du fichier sans le titre 
    fichier_tsv = getTSV(sys.argv[1])[1:]
    var_dict = extract_dict(fichier_tsv)  # { num_instruction : {'G': lhs_var , 'M': = , 'D'= rhs_valeur }}
    #pprint(var_dict)
    extract_vars(var_dict, variables) # là ou tout se passe 