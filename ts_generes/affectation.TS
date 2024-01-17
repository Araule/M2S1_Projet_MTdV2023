
%%%%%%%%% COPIE_VARIABLE
% On se place au niveau de l'adresse de destination et on place un 0 au niveau du premier "bit"
D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D 
0

% On initialise la boucle de copie
boucle
 
% On se place au niveau de adresse_provenance[1] (puis 2, puis 3)
 G G G G G G G G G G G G G G G G G G G G G G G G G G G G G G G 

 % Si il y a un 1, on se déplace sur l'adresse de destination à la position correspondante puis on écrit 1
 si(1)
 D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D 
 1}

 % Si il y a un 0, on est arrivé à la fin de notre variable. On se déplace sur l'adresse de destination à la position correspondante puis on écrit 0 et on met fin à la boucle de copie.
 si(0)
 D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D D 
 0 fin }
}

%On est sur le 0 qui "ferme" la valeur de notre variable. On doit retourner au début de l'adresse pour savoir où on se trouve sur la bande.
%%%%%%%%% REVENIR DEBUT ADRESSE
boucle
 %On fait un pas à gauche pour se situer au niveau du "dernier" 1 et on continue de se déplacer tant qu'on ne se situe pas sur le 0 d'initialisation.
 G
 si(0) fin }
}
%Notre pos actuelle correspond à variable_destination[0]
#
