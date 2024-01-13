from constante import Constante 
from variable import Variable
from bande import Bande

class MemoryManager:
    def __init__(self):
        self.memory = {} # nom -> adresse
        self.bande = Bande(3200)

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