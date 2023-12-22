import tokenize

# 3 : n° ligne de l'expression
# expression complète :  "y = x * 3"

tokenize.check_operation(['_kenza', '+', '3', '*', 'liza'], ['variable', 'operateur', 'valeur', 'operateur', 'variable'], 1, "y = _kenza +")