% il faut copier les deux variable a multiplier dans la memoire vive 
% de la façon suivante (ex: 2*4):
% 0111001111100
% ensuite il faut se deplacer dans la memoire vive a l'extremite gauche du premier nombre
% sur le premier baton
% 0111001111100
%  X
boucle si (0) fin } D }
% 0111001111100
%     X
boucle D si (1) fin } }
% 0111001111100
%       X
boucle D si (0) fin } }
% 0111001111100
%            X
D
1
% 01110011111010
%             X
G
boucle G si (0) fin } }
% 01110011111010
%      X
boucle G si (1) fin } }
% 01110011111010
%    X
boucle
  0
  G
  si (0) fin }
  % 01100011111010
  %   X
  D
  boucle D si (1) fin } }
  % 01100011111010
  %       X
  boucle D si (0) fin } }
  G
  % 01100011111010
  %           X
  boucle
    0
    G
    si (0) fin }
    % 01100011110010
    %          X
    D
    boucle D si (1) fin } }
    % 01100011110010
    %             X
    boucle D si (0) fin } }
    % 01100011110010
    %              X
    1
    % 011000111100110
    %              X
    boucle G si (0) fin } }
    % 011000111100110
    %            X
    boucle G si (1) fin } }
    % 011000111100110
    %          X
  }
  % 011000000000111110
  %      X
  D
  1
  % 011000100000111110
  %       X
  boucle D si (1) fin } }
  % 011000100000111110
  %             X
  G
  boucle G si (1) fin } 1 }
  % 011000111110111110
  %       X
  boucle G si (1) fin } }
  % 011000111110111110
  %   X
}
% 0000001111101111111110
% X
D 1
% 0100001111101111111110
%  X
boucle D si (1) fin } }
% 0100001111101111111110
%       X
boucle 0 D si (0) fin } }
% 0100000000001111111110
%            X
D
% 0100000000001111111110
%             X
boucle
  0
  D 
  % 0100000000000111111110
  %              X
  si (0) fin }

  boucle G si (1) fin } }
  % 0100000000000111111110
  %  X
  D
  1
  % 0110000000000111111110
  %   X
  boucle D si (1) fin } }
  % 0110000000000111111110
  %              X
}
% 0111111111000000000000
%                      X
boucle G si (1) fin } }
% 0111111111000000000000
%          X
boucle G si (0) fin } }
% 0111111111000000000000
% X
D
% 0111111111000000000000
%  X