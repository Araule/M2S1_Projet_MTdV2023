#!/bin/python3
# -*- coding: utf-8 -*-

""" 
	Ce que l'on peut ecrire sur le terminal depuis le dossier Projet_MTdV2023 :
    $ python groupe1_AnalyseSyntaxique.py
	
 	conseil Laura 1 : dans ce commentaire, il serait bien de rajouter un résumé du fichier à rajouter pour savoir ce qu'il fait
	conseil Laura 2 : Le fichier TSV est au format ASCII. Serait-il possible de le print au format utf-8 pour éviter tout problème
"""

import sys
import groupe1_TokenizeTSplus as tokenize
import os

def main(file, output_tsv_file):
	if not os.path.exists(file):
		print("\033[91m", end="") # Met les prochains prints en rouge
		print("Le fichier '"+ file + "' n'existe pas. (404 Not Found :( )")
		sys.exit(1)
	elif not os.path.isfile(file):
		print("\033[91m", end="") # Met les prochains prints en rouge
		print("'"+ file + "' n'est pas un fichier.")
		sys.exit(1)
		
	with open(file, 'r', encoding='ISO-8859-1') as f:
		program = f.read()
	lines, lines_number = tokenize.clean_lines(program)
	tokens = tokenize.make_tokens(lines, lines_number)
	for i, t in enumerate(tokens): # ajout du numéro du token
		t.insert(0, i+1)

	# vérification de la profondeur et ajout de la dernière colonne (scope_boucle)
	tokens = tokenize.check_structure(tokens)
	write_tsv(tokens, output_tsv_file)

def write_tsv(tokens, output_tsv_file):
	header = "token_n\tline_n\ttoken\ttype_token\tinstruction_n\ttype_instruction\tposition_instruction\tscope_boucle\n"
	with open(output_tsv_file, 'w') as f:
		f.write(header)
		for token in tokens:
			string = ""
			for t in token:
				string += str(t) + "\t"
			if len(token) == 7:
				string += "-\t" # scope_boucle vide
			string = string[:-1] # suppression du dernier \t
			f.write(string + "\n")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Il manque le fichier TS.")
		print("Usage:\n\tpython groupe1_AnalyseSyntaxique.py FICHIER.TSplus (SORTIE.tsv)")
		sys.exit(1)
	if len(sys.argv) > 2:
		output_tsv_file = sys.argv[2]
	else:
		output_tsv_file = ''.join(sys.argv[1].split('.')[:-1]) + '.tsv' # change l'extension en .tsv
	main(sys.argv[1], output_tsv_file)
