from typing import Dict, List
from constante import Constante 
from variable import Variable
from bande import Bande

# 0 à 9 -> 10 constantes
# on met 6 variables
# 1/3 variable, 2/3 mémoire vive
# 16*32 = 512
# 1024 pour la mémoire vive
# taille totale : 1536

# on doit récupérer les constantes du programme

# le nombre de variables aussi

class MemoryManager:
    def __init__(self):
        self.memory = {} # nom -> adresse
        self.bande = Bande(3200)
        # on met tout de suite les constantes
        for i in range(0, 10):
            self.bande.add_constant(i)
    
    def __init__(self, input_affectations: Dict):
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
        destination = self.bande.nb_variables * 32
        self.bande.ecrire(valeur, destination)
        self.memory[nom_constante] = destination
        self.bande.nb_variables += 1
        #print("La constante a bien été ajoutée.")
    
    def add_variable(self, nom: str, valeur: int):
        # ajoute une variable dans la mémoire
        if nom in self.memory.keys():
            raise ValueError(f"La variable existe déjà : {nom} à l'adresse {self.memory[nom]}. Utilisez plutôt update_variable().")
        
        # sinon ok, on crée cette variable à la fin de la bande
        destination = self.bande.nb_variables * 32
        self.bande.ecrire(valeur, destination)
        self.memory[nom] = destination
        self.bande.nb_variables += 1
        #print("La variable a bien été ajoutée.")

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
        # j'écris que des 0
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
                    
        for c in constantes:
            self.add_constant(c)

    def isInMemory(self, nom_variable: str) -> bool:
        return nom_variable in self.memory.keys()
    
    def readVariable(self, nom_variable: str) -> int:
        adresse = self.memory[nom_variable]
        return self.bande.lire(adresse)

    def readConstant(self, valeur: int) -> int:
        nom_constante = 'CONST_' + str(valeur)
        adresse = self.memory[nom_constante]
        return self.bande.lire(adresse)

    def afficher_memoire(self):
        """
            Affiche toutes les variables et leur adresse
        """
        for (nom_var, adresse) in self.memory.items():
            print(f"{nom_var} : adresse {adresse}")