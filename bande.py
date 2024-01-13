class Bande:
    def __init__(self, longueur: int):
        self.bande = ['0'] * longueur # Initialise la bande avec des espaces vides
        self.position_courante = 0 # Position courante à l'extrême gauche de la bande
        self.nb_variables = 0
        self.longueur = longueur

    def afficher(self):
        """
            Affiche la bande
        """
        for baton in self.bande:
            print(baton, end='')
        print()

    def get_position_courante(self):
        return self.position_courante

    def lire_position_courante(self) -> int:
        return int(self.bande[self.get_position_courante()])
    
    def lire(self, adresse_variable) -> int:
        """
            Cette méthode renvoie la valeur d'une variable en décimal :
            1. se place sur la dernière case de la série de cases allouées à la variable
            2. lit les cases en se déplaçant à gauche 32 fois
            3. stocke chaque variable dans un tableau, et convertit le binaire en décimal
        """
        # sur la dernière case
        destination = adresse_variable + 31
        self.se_deplacer(destination)
        # je remplis un tableau en lisant de droite à gauche
        batons = []
        for i in range(32):
            batons.append(self.lire_position_courante())
            self.se_deplacer1('G')
        # convertir le résultat en binaire
        # on ne compte pas le premier et le dernier zéro
        batons = batons[1:-2]
        resultat = 0
        for (baton, idx) in enumerate(batons):
            resultat += baton * 2**idx
        return resultat

    def ecrire_position_courante(self, valeur):
        """
            Écrit la valeur (0 ou 1) à la position courante
        """
        #print(self.position_courante)
        #print(f"nombre de variables : {self.nb_variables}")
        self.bande[self.position_courante] = valeur

    def ecrire(self, valeur: int, destination: int):
        """
            Variable : la valeur à encoder en décimal
            destination = adresse à laquelle on va écrire notre variable
            1. convertir en binaire
            2. se placer à droite. écrire le 1er zéro. écrire le nombre. écrire des zéros jusqu'à la fin
        """
        # on se déplace sur la bonne adresse + 32 pour écrire de droite à gauche
        self.se_deplacer(destination+32)
        # conversion en binaire
        binary_representation = bin(valeur)[2:]
        # on le parcourt à l'envers (de droite à gauche)
        binary_reverse = binary_representation[::-1]
        # on écrit sur la bande
        self.ecrire_position_courante(0)
        self.se_deplacer1('G') # écrit le 1er zéro
        for baton in binary_reverse:
            self.ecrire_position_courante(int(baton))
            self.se_deplacer1('G')
        # il faut compléter avec des zéros jusqu'au bout
        for i in range(32-len(binary_reverse)-1):
            self.ecrire_position_courante(0)
            self.se_deplacer1('G')
            
    def se_deplacer1(self, direction: str):
        if direction == 'D':
            self.position_courante += 1
        elif direction == 'G':
            self.position_courante -= 1
        else:
            raise ValueError("Direction invalide. Doit être soit 'droite', soit 'gauche'.")
       
    def se_deplacer(self, adresse: int):
        #print(f"type de l'adresse : {type(adresse)}")
        #print(f"type de longueur : {type(self.longueur)}")
        if adresse > int(self.longueur):
            raise ValueError("L'adresse demandée dépasse la mémoire")
        
        pos_courante = self.lire_position_courante()

        distance = pos_courante - adresse

        if distance < 0:
            # on avance, de abs(distance)
            for i in range(abs(distance)):
                self.se_deplacer1('D')
        else:
            # on recule, de abs(distance)
            for i in range(abs(distance)):
                self.se_deplacer1('G')#