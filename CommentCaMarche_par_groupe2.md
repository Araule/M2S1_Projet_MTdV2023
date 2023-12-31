# Alors, comment marche ce truc ?

L'idée c'est d'avoir un programme commun «lectureTSV» via lequel :
1. groupes 2 3 et 4 puissent puissent lire les fichiers tsv MDTV+ **en même temps**
	- car chaque **instruction** « ex. affectation - test - boucle » doit être gérée l'une après l'autre
	ex:
	- étape1 - gestion de variable (groupe 2)
	- étape2 - gestion mémoire (groupe 3)
	- étape3 - récupération de l'adresse pour gestion de variable si besoin (groupe2)
	- étape4 - déplacement bande (groupe 4)
	- repeat jusqu'à la fin du fichier 


## fichiers TSV
- On obtient les fichiers TSV avec les fichiers python du groupe 1 
- pourquoi ne pas envisager un fichier python* **main.py** qui appelle les fonctions directement ?

## lecture des fichiers TSV et gestionnaire de noms de variable
- On a crée un fichier python "lectureTSV.py" pour lire les fichiers tabulaires. 
- Nous proposons au groupes 2, 3 et 4 de rajouter vos modules sur ce fichier. 
- **Qu'en pensez vous ?**
- Avez vous d'autres propositions ?

## Quelques précision sur le fonctionnement du fichier lectureTSV.py
**La fonction lecturetsv()** :

	- lit le fichier tsv ligne par ligne. 
	- nos (groupe 2) modules gèrent le gestionnaire de noms de variable 
	- on a laissé de l'espace pour que vous,  (groupe 3 et groupe 4) puissiez rajouter ce que vous voulez dans cette boucle.

**vider le gestionnaire à la fin du programme**
- C'est également avec cette vision de fichier commun qu'on a une fonction à la toute fin du programme pour "vider" le gestionnaire de noms de variable 
- comme le ferait un compilateur. => c'est-à-dire fin de fichier == fin du compilateur

## A vous de jouer
- Maintenant, nous attendons vos propositions et vos commentaires concernant le **fonctionnement entre modules**. 
- Fallait qu'on ait quelque chose pour voir si notre module fonctionne ^^
