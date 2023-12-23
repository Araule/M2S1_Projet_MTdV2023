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
	instruction_n = 1
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
			tokens.extend(check_affectation(line, line_n, instruction_n))
			instruction_n += 1
		else:
			for token in regex.findall(r'((si +\( *(0|1)\))|[^ ]+)', line):
				token = token[0]
				if token in ('boucle', 'si (0)', 'si (1)', '}', '#', 'I', 'P', 'fin'):
					type_token = "trivial"
					type_instruction = "MTdV"
				elif token in ('G', 'D', '0', '1'):
					warning("Mot-clé {m} rencontré. Cela pourrait corrompre la mémoire du programme.".format(m=token), token=token, line_n=line_n, line=line)
					type_token = "memoire"
					type_instruction = "MTdV"
				elif regex.match(r'[0-9]+', token):
					erreur("Token de type entier non autorisé à cette position", token=token, line=line, line_n=line_n)
				elif regex.match(r'([a-z]|[A-Z]|_)|([a-z][A-Z][0-9]_)*', token):
					erreur("Nom de variable non autorisé en dehors d'une affectation ou d'un test", token, line=line, line_n=line_n)
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
		erreur("Un test doit commencer par le mot-clé si.\n\t syntaxe: si (operation1 test operation2)", token=tokens[0], line_n=line_n, line=expression)
	elif tokens[1] != "(":
		erreur("Un test doit être entouré par des parenthèses.\n\t syntaxe: si (operation1 test operation2)", token=tokens[1], line_n=line_n, line=expression)
	elif tokens[-1] != ")":
		erreur("Un test doit être entouré par des parenthèses.\n\t syntaxe: si (operation1 test operation2)", token=tokens[-1], line_n=line_n, line=expression)
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
			erreur("Token non autorisé dans un test.", token=token, line_n=line_n, line=expression)
	check_operation(operations_g_d["G"][0], operations_g_d["G"][1], line_n, expression)
	check_operation(operations_g_d["D"][0], operations_g_d["D"][1], line_n, expression)
	return sortie

def check_affectation(expression, line_n, instruction_n):
	"""
	Vérifier qu'à gauche on a un seul token de type variable, 
	et qu'à droite on a une opération valide (appel de check_operation(tokens, types, line_n))
	et renvoyer les types des tokens etc.

	returns: un tableau de tokens, avec pour chaque token les informations [line_n, token, type_token, instruction_n, type_instruction, position_operation], dans cet ordre-là.
	"""
	variable_regex = r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|[0-9]|_)*"
	chiffre_regex = r"[0-9]+"
	affectation_regex = r"="
	operateur_regex = r"[\+\*]"
	tokens = regex.findall("[^ ]+", expression)
	
	resultat = []
	left_token = tokens[0].strip()
	right_tokens = tokens[2:]

	# Vérifier qu'on a bien une variable à gauche
	if left_token  in ("boucle", "si", "D", "G", 'fin', 'I', 'P'):
		erreur("Côté gauche de l'affectation ne peut pas être un mot-clé.", token=left_token, line_n=line_n, line=expression)

	if not regex.match(variable_regex, left_token):
		erreur("Côté gauche de l'affectation doit être une variable.", token=left_token, line_n=line_n, line=expression)

	# Vérifier qu'on a bien une affectation
	if tokens[1] != affectation_regex:
		erreur("Une affectation doit avoir un seul symbole à gauche du =.", token=tokens[1], line_n=line_n, line=expression)

	types = []	

	# Construire le tableau de sortie
	# Parcourir chaque token dans la liste des tokens
	for i, token in enumerate(tokens):
		# Si le token est le premier de la liste, il est considéré comme une variable
		if i == 0:  # Côté gauche
			type_token = "variable" 
			position_operation = 'G'
		# Si le token correspond à l'expression régulière d'affectation, il est considéré comme une affectation
		elif i == 1 : # Affectation
			type_token = "operateur"
			position_operation = 'M'
		# Si le token est sur le côté droit de l'affectation
		elif i > 1:  # Côté droit
			position_operation = 'D'
			# Si le token est le suivant sur le côté droit
			if regex.match(chiffre_regex, token):
				# Si le token correspond à l'expression régulière d'un chiffre, il est considéré comme une valeur
				type_token = "valeur"
				types.append(type_token)

			elif regex.match(operateur_regex, token):
				# Si le token correspond à l'expression régulière d'un opérateur, il est considéré comme un opérateur
				type_token = "operateur"
				types.append(type_token)

			# Si le token est le dernier sur le côté droit
			elif regex.match(variable_regex, token):
				# Si le token correspond à l'expression régulière d'une variable, il est considéré comme une variable
				type_token = "variable"
				types.append(type_token)
				if token  in ("boucle", "si", "D", "G", 'fin', 'I', 'P'):
					# Si le token est un mot clé, c'est une erreur
					erreur("Côté droite de l'affectation ne peut pas contenir un mot-clé.", token=token, line_n=line_n, line=expression)
			else:
				erreur("Token non autorisé dans une affectation.", token, line_n, expression)
		# Ajouter le token et ses informations à la liste des résultats
		resultat.append([line_n, token, type_token, instruction_n, "affectation", position_operation])

	check_operation(right_tokens, types, line_n, expression)
		

	return resultat

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
	Vérifie qu'on a bien une suite de types qui fasse v o v o v o v, et que les o sont soit * soit	avec: v = variable ou valeur, o = operateur.

	par exemple
	- autorisé : v tout seul , v o v, v o v o v, v o v (o v)*
	- non autorisé : o, v o, o v, o v o, o o, v v.

	Si ce n'est pas au bon format, il faut afficher une erreur (cf le power point)
	Si un objet de type "valeur" est < 0 ou > 29 (tester en convertissant int(token) ), renvoyer une erreur de valeur.
	"""
	operateur_regex = r"[\+\*]"
	assert len(tokens) == len(types)
	if len(tokens) == 0:
		erreur("Test ou affectation incomplète.", line_n=line_n, line=line)
	i = 0
	for token, typen in zip(tokens, types):
		# Boucle sur les tokens et les types en même temps
		# on vérifie ici qu'on a bien v sur les tokens impairs, o sur les pairs.
		# affichage de l'erreur d'opération:
		# erreur("Opération invalide", token=token, line_n = line_n, line = line)
		i += 1
		if i % 2 == 0:
			if typen != "operateur":
				erreur("Opérateur attendu (+ ou *) dans l'opération.\nOpération binaire incomplète.", token, line_n=line_n, line=line)
			elif not regex.search(operateur_regex, token):
				# Si l'opérateur n'est pas un opérateur valide (pas d'opérateur d'affectation ou de test)
				erreur("Opérateur invalide dans une opération.", token, line_n=line_n, line=line)
		elif i % 2 != 0:
			if typen != "variable" and typen != "valeur":
				erreur("Valeur ou variable attendue dans l'opération.\nOpération binaire incomplète.", token, line_n=line_n, line=line)
				# TODO afficher un message plus précis
			elif typen == "valeur":
				if int(token) < 0 or int(token) > 29:
					erreur("Entier dépassant la limite autorisée.\n\tValeurs autorisées: [0-29]", token=token, line_n=line_n, line=line)
	if i % 2 == 0:
		# en sortant de la boucle, il faut que i est bien un chiffre impair
		# sinon il manque sans doute un 'v' final.
		erreur("Une opération ne peut pas se terminer par un opérateur.", tokens[-1], line_n = line_n, line = line)

def erreur(erreur_str, token="", line_n="", line=""):
	print("\033[91m", end="") # Met les prochains prints en rouge
	print(erreur_str)
	if line_n or line or token:
		print("Erreur rencontrée ", end="")
	if line_n:
		print("à la ligne " + str(line_n))
	if line:
		print("\t" + line)
	if token:
		print("sur le token '" + str(token) + "'")
	print("\033[0m", end="") # Met les prochains prints en jaune
	sys.exit(1)

def warning(warning_str, token="", line_n="", line=""):
	print("\033[93m", end="") # Met les prochains prints en jaune
	print(warning_str)
	if line_n:
		print("A la ligne " + str(line_n))
	if line:
		print("\t" + line)
	if token:
		print("Sur le token '" + str(token) + "'")
	# pas de exit, un warning n'est qu'un avertissement.
	print("\033[0m", end="") # Met les prochains prints en jaune
