# Journal de bord

## 11/01/24
Nous nous sommes rencontrés pour faire un point sur ce que nous devions faire pour pouvoir générer les scripts en MTdV à partir des sorties que nous devrions récupérer des autres groupes et avons fait une attribution provisoire des tâches que nous avons identifiées : 
1. Utiliser les sorties des autres groupes → **Valentina**
2. Créer une fonction `copy` pour pouvoir copier le contenu d'une adresse à une autre adresse → **Agathe**
3. Créer une fonction `comparison` pour pouvoir comparer deux variables entre elles (directement au niveau des adresses de chacune) → **Sandra**
4. Regarder l'utilisation d'`addition.TS` et `multiplication.TS` pour les adapter à notre script → **Florian**
5. Gestion des triviaux → **Valentina**
6. main → *à venir*

## 14/01/24
**Agathe** : 
- Création de la fonction `copie_une_variable` : 
	- On part du principe que le premier emplacement d'une adresse mémoire est toujours à 0 pour la séparer de l'adresse précédente. 
	- On commence donc par mettre un 0 au premier emplacement de l'adresse de destination puis on se place au niveau du deuxième emplacement de l'adresse de la variable qu'on veut copier et on effectue une boucle.
	- Notre boucle continue de copier tant qu'on a un 1 à l'adresse de notre variable à copier et dès qu'elle atteindra le 0 indiquant la fin de la variable, le 0 sera copié à l'adresse de destination puis un `fin` mettra fin à la boucle.
	- Comme nous ne savons pas cb de tours de boucles il va y avoir, on ne peut pas connaître la position finale de notre tête de bande. Il faut donc ajouter une boucle qui nous remet au niveau du premier "bit" de l'adresse pour savoir où l'on se trouve.

## 15/01/24
**Agathe** :
- Création d'une fonction `copie_deux_variables` qui sera utilisée pour copier deux variables au sein de la mémoire vive pour faire des opérations dessus.
	- Problème rencontré : où se trouve-t-on une fois la variable 1 copié. On ne connait pas la valeur réelle de la variable_1 donc on ne peut savoir où l'on se trouve. Or, on a besoin de la position pour savoir le nombre de déplacement jusqu'à l'adresse de la variable 2. Deux solutions possibles, mais aucune ne me satisfait vraiment (la deuxième plus satisfaisante que la première toutefois):
		1. On calcule la pos actuelle en récupérant la vraie valeur de variable_1 → interprétation ?
		2. On copie la seconde valeur en partant de la fin de la mémoire → + de deux 0 entre les deux valeurs sur lesquelles on effectue les opérations donc pb ? Possible problème de réécriture de la variable 1 si variable 1 + variable 2 + les zéros entourant > 32 → erreur retournée par groupe 1 ?

## 16/01/24
Journée de travail en groupe
**Agathe** :
- Pour copier deux variables au niveau de la mémoire vive, comme la mémoire vive est largement plus grande que la taille d'une adresse de variable ou de constante, et que les scripts addition et multiplication peuvent s'appliquer même qd on a plus de deux 0 entre les deux variables, on a simplement copié la seconde variable à `adresse_memoire_vive+32`
- On a maintenant :
	- une fonction `copie_variable(adresse_A, adresse_B, pos)` permettant de copier le contenu d'une adresse A à l'adresse B en fonction de la position actuelle de notre tête de bande.
	- une fonction `revenir_debut_adresse()` permettant de revenir à la position initiale de la variable dans laquelle on se trouve pour retrouver la position de la tête de la bande, peu importe la valeur stockée dans la variable.
	- une fonction `copie_deux_variables_memoire_vive()` utilisant les deux fonctions précédentes et permettant de copier deux variables dans la mémoire vive. À la fin de celle-ci, on se trouve à la position initiale de la **deuxième** valeur écrite dans la mémoire vive.

