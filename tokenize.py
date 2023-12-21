import regex

from typing import List

import sys

def clean_lines(text: str):
	# split lines
	text = regex.split(r"\r\n|\n", text)
	new_text = []
	lines_number = []
	line_n = 0
	for line in text:
		line_n += 1
		# Ajout d'espaces autour de certains caractères
		line = regex.sub("}", " }", line)
		line = regex.sub("si\(", "si ( ", line) # si la parenthèse du si est collée
		line = regex.sub("[^=]=[^=]", " = ", line)
		line = regex.sub("==", " == ", line)
		line = regex.sub("\*", " * ", line)
		line = regex.sub("\+", " + ", line)

		new_line = ""
		for token in line.split():
			token = token.strip()
			if len(token) > 0 and token[0] == '%':
				break
				# ignore comment lines or inline comments
			new_line += token + " "
		if len(new_line) > 0:
			new_text.append(new_line)
			lines_number.append(line_n)
	return (new_text, lines_number)

def make_tokens(lines: List[str], lines_number: List[int]):
	"""
	Coupe les lignes en tokens (token, line_number, instruction_number).
	"""
	tokens = []
	instruction_n = 0
	assert(len(lines) == len(lines_number))
	for line, line_n in zip(lines, lines_number):
		if regex.match(r".*==.*", line):
			type_instruction = "test"
			line = regex.sub(r"\(", " ( ", line)
			line = regex.sub(r"\)", " ) ", line)
			# Ici, il faut vérifier qu'on a deux expressions à gauche et à droite du ==
			# puis il faut mettre G, M et D.
			tokens.extend(check_test(line, line_n, instruction_n))
			instruction_n += 1
		elif regex.match(r".* = .*", line):
			type_instruction = "affectation"
			tokens.extend(check_affectation(line, line_n))
			instruction_n += 1
		else:
			for token in regex.findall(r'((si +\( *(0|1)\))|[^ ]+)', line):
				token = token[0]
				if token in ('boucle', 'si (0)', 'si (1)', '}', '#', 'I', 'P', 'fin'):
					type_token = "trivial"
					type_instruction = "MTdV"
				elif token in ('G', 'D', '0', '1'):
					warning()
					type_token = "memoire"
					type_instruction = "MTdV"
				elif regex.match(r'[0-9]+', token):
					erreur("Token de type entier non autorisé à cette position", token=token, line=line, line_n=line_n)
				else:
					erreur("Token non autorisé", token=token, line=line, line_n=line_n)
				instruction_n += 1
				tokens.append([line_n, token, type_token, instruction_n, type_instruction, '-']) # le '-' est la position operation.
	return tokens

def check_test(expression, line_n, instruction_n):
	"""
	Fonction qui vérifie qu'on a bien si (expression == expression),
	et envoie un message d'erreur sinon.

	returns: un tableau de tokens, avec pour chaque token les informations [line_n, token, type_token, instruction_n, type_instruction, position_operation], dans cet ordre-là.
	"""
	variable_regex = r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|[0-9]|_)*"
	chiffre_regex = r"[0-9]+" # TODO il faudra vérifier que c'est entre 0 et 29
	egalite_regex = r"=="
	si_regex = r"si"
	operateur_regex = r"[\+\*]"
	tokens = regex.findall("[^ ]+", expression)

	# Vérification de la structure externe du test : si ( ... )
	if tokens[0] != "si":
		erreur("Un test doit commencer par le mot-clé si.", token=tokens[0], line_n=line_n, line=expression)
	elif tokens[1] != "(":
		erreur("Un test doit être entouré par des parenthèses.", token=tokens[1], line_n=line_n, line=expression)
	elif tokens[-1] != ")":
		erreur("Un test doit être entouré par des parenthèses.", token=tokens[-1], line_n=line_n, line=expression)
	position = 'G'
	operations_g_d = {'G': [[],[]], 'D': [[],[]]} # ['G'][0] => les tokens de gauche. ['D'][0] => les tokens de droite.
	# ['G'][1] => les types des tokens de gauche. ['D'][1] => les types des tokens de droite.

	# Vérification des tokens
	# et création de la liste de sortie
	sortie = []
	for token in tokens:
		if token in ("boucle", "D", "G", '#', '}', 'fin', 'I', 'P', '='):
			erreur("Mot-clé non autorisé dans un test.", token=token, line_n=line_n, line=expression)
		elif regex.match(si_regex, token):
			sortie.append([line_n, token, "complexe", instruction_n, "test", '-'])
		elif regex.match(variable_regex, token):
			sortie.append([line_n, token, "variable", instruction_n, "test", position])
			operations_g_d[position][0].append(token)
			operations_g_d[position][1].append("variable")
		elif regex.match(chiffre_regex, token):
			sortie.append([line_n, token, "valeur", instruction_n, "test", position])
			operations_g_d[position][0].append(token)
			operations_g_d[position][1].append("valeur")
		elif regex.match(egalite_regex, token):
			if (position == 'D'):
				erreur("Un test d'égalité ne peut pas contenir deux fois l'opérateur ==.", token=token, line_n=line_n, line=expression)
			sortie.append([line_n, token, "operateur", instruction_n, "test", 'M'])
			position = 'D'
		elif regex.match(operateur_regex, token):
			sortie.append([line_n, token, "operateur", instruction_n, "test", position])
			operations_g_d[position][0].append(token)
			operations_g_d[position][1].append("operateur")
		elif token not in ['(', ')']:
			erreur("Token non autorisé dans un test", token=token, line_n=line_n, line=expression)
	check_operation(operations_g_d["G"][0], operations_g_d["G"][1], line_n, expression)
	check_operation(operations_g_d["D"][0], operations_g_d["D"][1], line_n, expression)
	return sortie

#TODO
def check_affectation(expression, line_n):
	"""
	Vérifier qu'à gauche on a un seul token de type variable, et qu'à droite on a une operation valide (appel de check_operation(tokens, types, line_n))
	et renvoyer les types des tokens etc.

	returns: un tableau de tokens, avec pour chaque token les informations [line_n, token, type_token, instruction_n, type_instruction, position_operation], dans cet ordre-là.
	"""
	variable_regex = r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|[0-9]|_)*"
	chiffre_regex = r"[0-9]+"
	affectation_regex = r"="
	si_regex = r"si"
	operateur_regex = r"[\+\*]"
	tokens = regex.findall("[^ ]+", expression)

	resultat = [] 

	print(expression)
	return ()

#TODO
"""
Les paramètres line_n et line servent à l'affichage des erreurs.

returns: None
"""
def check_operation(tokens, types, line_n, line):
	"""
	tokens: liste des tokens de l'opération.
	types: type des tokens de l'opération.
	Fonction qui ne fait rien si l'opération est valide.
	Sinon, elle affiche une erreur avec la fonction erreur.
	TODO
	Vérifie qu'on a bien une suite de types qui fasse v o v o v o v, et que les o sont soit * soit +
	avec: v = variable ou valeur, o = operateur.

	par exemple
	- autorisé : v tout seul , v o v, v o v o v, v o v (o v)*
	- non autorisé : o, v o, o v, o v o, o o, v v.

	Si ce n'est pas au bon format, il faut afficher une erreur (cf le power point)
	Si un objet de type "valeur" est < 0 ou > 29 (tester en convertissant int(token) ), renvoyer une erreur de valeur.
	"""
	print(tokens, types)
	i = 0
	for token, typen in zip(tokens, types):
		i += 1
		continue
		# Boucle sur les tokens et les types en même temps
		# on vérifie ici qu'on a bien v sur les tokens impairs, o sur les pairs.
		# affichage de l'erreur d'opération:
		# erreur("Opération invalide", token=token, line_n = line_n, line = line)
	# en sortant de la boucle, il faut que i est bien un chiffre impair; sinon il manque
	# sans doute un 'v' final.
	# affichage de l'erreur d'opération sur le dernier token de l'opération:
	# erreur("Opération invalide", token=tokens[-1], line_n = line_n, line = line)

def erreur(erreur_str, token="", line_n="", line=""):
	print("\033[91m", end="") # Met les prochains prints en rouge
	print(erreur_str)
	if line_n != "":
		print("A la ligne n°" + str(line_n))
	if line != "":
		print("\t" + line)
	if token != "":
		print("Sur le token:" + str(token))
	sys.exit(1)

def warning(warning_str, token="", line_n="", line=""):
	print("\031[91m", end="") # Met les prochains prints en jaune
	print(erreur_str)
	if line_n != "":
		print("A la ligne n°" + str(line_n))
	if line != "":
		print("\t" + line)
	if token != "":
		print("Sur le token:" + str(token))
	# pas de exit, un warning n'est qu'un avertissement.
