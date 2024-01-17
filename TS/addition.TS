% il faut copier les deux variable a additionner dans la memoire vive 
% de la façon suivante (ex: 2+4):
% 0111001111100
% ensuite il faut se deplacer dans la memoire vive a l'extremite gauche du premier nombre
% sur le premier baton
% 0111001111100
%  X
boucle 
  si (0) fin }
  D
}
% 0111001111100
%     X
boucle
  boucle 
    D
    si (1) fin }
  }
  % 0111001111100
  %       X
  0
  D
  % 0111000111100
  %        X
  si (0) fin }
  boucle 
    G
    si (1) fin }
  }
  % 0111000111100
  %    X
  D
  1
  D
  % 0111100111100
  %      X
} 
% 0111111100000
%             X
boucle 
  G
  si (1) fin }
}
% 0111111100000
%        X
boucle 
  G
  si (0) fin }
}
% 0111111100000
% X
D
% 0111111100000
%  X