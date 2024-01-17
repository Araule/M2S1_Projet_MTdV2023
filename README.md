# ALLOCATION ET GESTION DE LA MÉMOIRE 
Le présent README donne plus d'indication sur le module groupe3_gestionMemoire qui permet d'allouer et de gérer l'espace mémoire pour la réalisation du projet. 

3. Allocataire/Gestionnaire de mémoire
   - Clément
   - Tifanny
   - Fanny

La première variable du programme est enregistré en tant que constante. Ainsi, deux espaces mémoires seront allouer. Un premier pour le 0 qui sera une constante et une autre pour x, qui au début du programme a pour valeur 0. 

Ce module prend en input la sortie du groupe 2 : gestionnaire de nom de variable qui nous fournie un dictionnaire, qui a chaque numéro d'instruction associe les membres gauches et droits d'une affectation. (script groupe3_gestionMemoire.py). Cela nous permet de savoir quand une variable est créée ou supprimée. Ce qui nous permet de faire le traitement adéquate dans la mémoire. 

L'output se présente de la façon suivante, c'est un dictionnaire qui comprends l'adresse des variables à chacune des instructions mêmes si celles-ci ne sont pas importantes: 

Exemple d'output : 

```
Étape n°1: 
CONST_0 : adresse 0
x : adresse 32

Étape n°2: 
CONST_0 : adresse 0
x : adresse 32
CONST_1 : adresse 64

Étape n°3: 
CONST_0 : adresse 0
x : adresse 32
CONST_1 : adresse 64
CONST_2 : adresse 96
y : adresse 128

# Et ainsi de suite, jusqu'a ce que tout le dictionnaire ait été lu.

```

## Inventaires (et précisions) des scripts : 

### groupe3_gestionMemoire.py 
Le script principal, il prend en entrée un dictionnaire d'affectation (et de suppression) : 'input_affectations' (qui nous est fourni par le groupe 2). 
On simule l'évolution de la mémoire à chaque instruction, on lit une première fois le dictionnaire pour mettre en mémoire les constantes et on le fait une seconde fois pour enregistrer les variables. Cela nous permet par la suite de renvoyer un dictionnaire avec l'état de la mémoire. 
Tout d'abord, on initialise la mémoire , pour ensuite dans la boucle principale itérer sur chaque instruction du programme et ainsi faire le traitement approprié. On enregistre ensuite l'état de la mémoire dans le dictionnaire avec l'indice correspondant à chaque étape. Et on retourne mémoire qui représente l'état de la mémoire à chaque étape du programme. 

### memory_manager.py 
Voici le script de la classe MemoryManager. On y retrouve les constantes et les variables.
1. Les constructeurs :
   Il y a 2 constructeurs : un premier par défaut et un second qui prend en entrée un dictionnaire d'affectations (fournis par le groupe 2), pour initialiser la mémoire, on utilise la méthode 'initialiser_constantes' pour les constantes.
2. Les méthodes pour ajouter des constantes (+ méthode pour initialiser à partir d'affectation) et des variables( + modifier et supprimer):
   add_constant(self, valeur: int): Ajoute une constante à la mémoire en écrivant sa valeur sur la bande.
   add_variable(self, nom: str, valeur: int): Ajoute une variable à la mémoire en écrivant sa valeur sur la bande.
   update_variable(self, nom: str, valeur: int): Met à jour la valeur d'une variable existante en mémoire.
   delete_variable(self, nom: str): Supprime une variable de la mémoire en écrivant des zéros à son adresse sur  la bande.
   initialiser_constantes(self, input_affectations: Dict): Parse les membres droits des affectations pour récupérer des constantes et les charge en mémoire.
3. Les méthodes de lecture des valeurs déjà en mémoire :
   isInMemory(self, nom_variable: str) -> bool: Vérifie si une variable est présente en mémoire.
   readVariable(self, nom_variable: str) -> int: Renvoie la valeur d'une variable à partir de son nom.
   readConstant(self, valeur: int) -> int: Renvoie la valeur d'une constante à partir de sa valeur.
4. Méthode d'affichage et de gestion de la mémoire :
   afficher_memoire(self): Affiche toutes les variables et leurs adresses en mémoire.
   adresse_memoire_vive(self) -> int: Renvoie l'adresse du point de départ de la mémoire vive, après les constantes et les variables.

### bande.py : 
C'est le script qui nous permet de modéliser la bande mémoire pour notre machine de Turing. Comme nous l'avions présentés, elle est composée d'une séquences de "cases" initialement vides. On maintient la positions courante et on propose plusieurs méthodes : 
- afficher(self) : affiche le contenu de la bande.
- lire_position_courante(self) -> int: Lit la valeur (0 ou 1) à la position courante sur la bande.(qui est permise grâce à get_position_courante(self) juste avant.)
- lire(self, adresse_variable) -> int: Lit une valeur binaire à partir d'une adresse spécifiée sur la bande.
      Cette méthode renvoie la valeur d'une variable en décimal :
            1. se place sur la dernière case de la série de cases allouées à la variable
            2. lit les cases en se déplaçant à gauche 32 fois
            3. stocke chaque variable dans un tableau, et convertit le binaire en décimal
- ecrire_position_courante(self, valeur): Écrit la valeur (0 ou 1) à la position courante sur la bande.
- ecrire(self, valeur: int, destination: int): Écrit une valeur binaire (sous forme décimale) à une adresse spécifiée sur la bande.
  Précisions :
            Variable : la valeur à encoder en décimal
            destination = adresse à laquelle on va écrire notre variable
            1. convertir en binaire
            2. se placer à droite. écrire le 1er zéro. écrire le nombre. écrire des zéros jusqu'à la fin
- se_deplacer1(self, direction: str): Déplace la position courante d'une unité vers la droite ('D') ou la gauche ('G').
- se_deplacer(self, adresse: int): Déplace la position courante à une adresse spécifiée sur la bande.
- inverser_ecriture(self): Inverse le sens d'écriture des variables et constantes sur la bande.

### variable.py 
Permet de créer un objet variable à partir des informations qui nous sont fournies par le groupe 2. Cette classe à pour attributs adresse, nom et valeur ainsi que 3 méthodes : 
1. affecter
2. comparer
3. get_adresse
   
### constante.py 
C'est une classe qui hérite de la classe variable et qui permet de gérer les constantes. 

### operateurs.py 
Ce script contient une méthode pour chacun des opérateurs si cela est nécessaire pour le groupe 4. 

