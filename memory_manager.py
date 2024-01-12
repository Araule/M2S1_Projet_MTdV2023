from constante import Constante 
from variable import Variable
from bande import Bande

class MemoryManager:
    def __init__(self):
        self.memory = {} # nom -> adresse
        self.bande = Bande()

    def add_constant(self, valeur):
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
    
    def add_variable(self, nom, valeur):
        # ajoute une variable dans la mémoire
        if nom in self.memory.keys():
            raise ValueError(f"La variable existe déjà : {nom} à l'adresse {self.memory[nom]}. Utilisez plutôt update_variable().")
        
        # sinon ok, on crée cette variable à la fin de la bande
        destination = self.bande.nb_variables * 32
        self.bande.ecrire(valeur, destination)
        self.memory[nom] = destination

    def update_variable(self, nom, valeur):
        # il faut que la variable soit dans la mémoire
        if nom not in self.memory.keys():
            raise ValueError(f"La variable {nom} n'existe pas en mémoire.")
        # sinon ok 
        # on récupère l'adresse de la variable
        destination = self.memory[nom]
        self.bande.ecrire(valeur, destination)
