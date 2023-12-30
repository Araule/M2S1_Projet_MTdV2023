#!/bin/python3
# -*- coding: utf-8 -*-

""" 
    Ce que l'on peut ecrire sur le terminal depuis le dossier Projet_MTdV2023 :
    $ python groupe2_exempleSimple.py
    
    Ce fichier sert à tester le gestionnaire de noms de variable sans lire de fichier tsv
"""

from groupe2_GestionVariables import GestionnaireVariables

# Exemple simple d'utilisation du gestionnaire avec la variable "a" et "b"

variables = GestionnaireVariables()

variables.printVariables() # vide

variables.addVariable("a")
variables.printVariables # a0

variables.updateAdresse("a")
variables.addVariable("b")
variables.printVariables # a1 b0

variables.deleteVariable("a")  
for v in ["a", "b"] :
    if variables.doesVariableExist(v) :
        print(f"la variable {v} existe.") # b
    else :
        print(f"la variable {v} n'existe pas.") # a

print(variables)
print(variables.getDict)