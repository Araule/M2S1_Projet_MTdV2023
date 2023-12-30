#!/bin/python3
# -*- coding: utf-8 -*-

""" Gestionnaire de noms de variable pour programme MdtV+ au format de dictionnaire
    Le fichier contient la classe et ses méthodes
    
    Pour le groupe 3 et 4 : n'hésitez pas à nous contacter si vous avez besoin 
    d'une nouvelle méthode ou si vous avez besoin que l'on modifie une déjà existante
"""

import regex
import sys

class GestionnaireVariables:

    def __init__(self):
        """ initialisation du gestionnaire de noms de variable
        """
        self.variables = {}

    def addVariable(self, nom: str, adresse):
        """ ajout de la variable dans le gestionnaire

        Args:
            nom (str): nom de la variable
        """
        # si le nom de la variable est autorisé
        if regex.match(r'([a-z]|[A-Z]|_)|([a-z][A-Z][0-9]_)*', nom):
            # on va d'abord chercher l'adresse de la variable
            # attente groupe 3
            adresse = 0
            # on ajoute la variable au gestionnaire avec son adresse
            self.variables[nom] = adresse
        else :
            # sinon, fin du programme
            print("\033[91mLe nom de variable {} n'est pas autorisé.\033[0m".format(nom)) # affiche en rouge
            sys.exit(1)

    def updateAdresse(self, nom: str):
        """ mise à jour de l'adresse de la variable dans le gestionnaire

        Args:
            nom (str): nom de la variable
        """
        # si la variable existe dans le gestionnaire
        if nom in self.variables:
            # on va d'abord chercher l'adresse de la variable
            # attente groupe 3
            adresse = 1
            # on met à jour l'adresse de la variable
            self.variables[nom] = adresse
        else:
			# sinon, fin du programme
            print("\033[91mL'adresse de la variable '{}' n'a pas pu être mise à jour.".format(nom)) # affiche en rouge
            print("La variable n'existe pas dans le gestionnaire.\033[0m")
            sys.exit(1)

    def deleteVariable(self, nom: str):
        """ suppression de la variable dans le gestionnaire

        Args:
            nom (str): nom de la variable
        """
        # si la variable est bien dans le gestionnaire
        if nom in self.variables:
            # suppression de la variable
            del self.variables[nom]
        else :
            # sinon, fin du programme
            print("\033[91mLa variable '{}' n'a pas pu être supprimé.".format(nom)) # affiche en rouge
            print("La variable n'existe pas dans le gestionnaire.\033[00m")
            sys.exit(1)

    def printVariables(self):
        """ affichage de toutes les variables du gestionnaire
        """
        if len(self.variables.keys()) > 0 :
            for nom, adresse in self.variables.items() :
                print(f"{nom}: {adresse}")
        else :
            print("\033[92mLe gestionnaire de noms de variable est actuellement vide.\033[00m")

    def getDict(self) -> dict :
        """ retourne le dictionnaire de noms de variable
        
        Returns:
            dict: gestionnaire de noms de variable
        """
        return self.variables

    # peut servir pour vérifier que l'adresse est bien la même
    # dans le module gestion variables et gestion mémoires
    # si il n'est pas utile
    # nous le supprimerons plus tard
    def getAdresse(self, nom: str) -> int:
        """ retourne l'adresse de la variable

        Args:
            nom (str): nom de la variable

        Returns:
            int: adresse de la variable (pour l'instant de type int)
        """
        if nom in self.variables:
            # si la variable est bien dans le gestionnaire
            return self.variables[nom]
        else :
            # sinon, fin du programme
            print("\033[91mL'adresse de la variable '{}' n'a pas pu être obtenu.".format(nom)) # affiche en rouge
            print("La variable n'existe pas dans le gestionnaire ")
            print("\033[0m", end="") # remet la couleur par défaut
            sys.exit(1)

    def doesVariableExist(self, nom: str) -> bool:
        """ vérifie si une variable se trouve dans le gestionnaire

        Args:
            nom (str): nom de la variable

        Returns:
            bool: renvoie True ou False 
                selon si la variable existe dans le gestionnaire
        """
        if nom in self.variables:
            # si la variable se trouve bien dans le gestionnaire
            return True
        else:
            # sinon
            return False