from typing import Dict, List
from constante import Constante 
from variable import Variable
from bande import Bande

class MemoryManager:
    def __init__(self):
        """
            Constructeur par défaut. Si on ne fournit pas de dictionnaire des affectations,
            on remplit les premières cases de la mémoire avec les constantes de 0 à 9
        """
        self.memory = {} # nom -> adresse
        self.bande = Bande(3200)
        # on met tout de suite les constantes
        for i in range(0, 10):
            self.bande.add_constant(i)
    
    def __init__(self, input_affectations: Dict):
        """
            Constructeur avec dictionnaire des affectations du groupe 2
            initialise les constantes en mémoire
        """
        self.memory = {} # nom -> adresse
        self.bande = Bande(3200)
        # on met tout de suite les constantes
        self.initialiser_constantes(input_affectations)

    def add_constant(self, valeur: int):
        # ajoute une constante dans la mémoire
        nom_constante = 'CONST_' + str(valeur)
        if nom_constante in self.memory.keys():
            # la variable existe déjà
            raise ValueError(f"La constante existe déjà : {nom_constante} à l'adresse {self.memory[nom_constante]}.")
        # sinon ok, on écrit la constante en mémoire
        # on se place au bout de la bande
        destination = self.bande.nb_constantes * 32
        self.bande.ecrire(valeur, destination)
        self.memory[nom_constante] = destination
        self.bande.nb_constantes += 1
    
    def add_variable(self, nom: str, valeur: int):
        # ajoute une variable dans la mémoire
        if nom in self.memory.keys():
            raise ValueError(f"La variable existe déjà : {nom} à l'adresse {self.memory[nom]}. Utilisez plutôt update_variable().")
        assert self.bande.nb_variables < 5, "Mémoire pleine, impossible de créer une nouvelle variable"
        
        # sinon ok, on crée cette variable à la fin de la bande
        destination = self.bande.nb_variables * 32
        self.bande.ecrire(valeur, destination)
        self.memory[nom] = destination
        self.bande.nb_variables += 1

    def update_variable(self, nom: str, valeur: int):
        # il faut que la variable soit dans la mémoire
        if nom not in self.memory.keys():
            raise ValueError(f"La variable {nom} n'existe pas en mémoire.")
        # sinon ok 
        # on récupère l'adresse de la variable
        destination = self.memory[nom]
        self.bande.ecrire(valeur, destination)

    def delete_variable(self, nom: str):
        # Je vais à son adresse
        adresse = self.readVariable(nom)
        # j'écris des 0
        self.bande.ecrire(0, adresse)
        del self.memory[nom]

    def initialiser_constantes(self, input_affectations: Dict):
        """
            parse les membres droits des affectations pour récupérer des constantes
            et les charge en mémoire
        """
        constantes = []
        for affectation in input_affectations.values():
            membre_droit = affectation['D']
            # 3 possibilités : un chiffre, un lettre ou a + b
            if len(membre_droit) == 1:
                if membre_droit.isdigit():
                    # c'est une constante
                    constantes.append(int(membre_droit))
            else:
                # c'est une expression 'X1 opérateur X2'
                (terme1, operateur, terme2) = membre_droit.split(" ")
                if terme1.isdigit():
                    # c'est une constante
                    constantes.append(int(terme1))
                if terme2.isdigit():
                    constantes.append(int(terme2))
        # on écrit les constantes récupérées
        for c in constantes:
            self.add_constant(c)

    def isInMemory(self, nom_variable: str) -> bool:
        """
            Vérifie si une variable est présente en mémoire
        """
        return nom_variable in self.memory.keys()
    
    def readVariable(self, nom_variable: str) -> int:
        """
            Renvoie la valeur d'une variable à partir de son nom
        """
        adresse = self.memory[nom_variable]
        return self.bande.lire(adresse)

    def readConstant(self, valeur: int) -> int:
        """
            Renvoie la valeur d'une constante à partir de sa valeur
        """
        nom_constante = 'CONST_' + str(valeur)
        adresse = self.memory[nom_constante]
        return self.bande.lire(adresse)

    def afficher_memoire(self):
        """
            Affiche toutes les variables et leur adresse
        """
        for (nom_var, adresse) in self.memory.items():
            print(f"{nom_var} : adresse {adresse}")

    def adresse_memoire_vive(self) -> int:
        """
            Renvoie l'adresse du point de départ de la mémoire vive
        """
        # on passe les constantes et les variables
        return self.bande.nb_constantes * 32 + self.bande.nb_variables * 32
    
    