#!/bin/python3
# -*- coding: utf-8 -*-

import sys

import tokenize_MTdVplus as tokenize

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
	# TODO : faire une recherche récursive dans les tokens pour vérifier les indentations
	# ainsi que d'écrire la dernière colonne du fichier TSV.
	# Cette colonne correspond au token qui est après le } de la Boucle la plus externe, ou un - si on n'est pas dans une boucle.
	# Cette colonne sera utile pour le Garbage Collector (certaines variables disparaissent en sortant des boucles si elles n'apparaissent plus après)
	# par exemple:
	# 1 boucle	7		
	# 2   boucle	7
	# 3     ...	7
	# 4     ...	7
	# 5   }		7
	# 6 }		7
	# 7 boucle	10
	# 8   ...	10
	# 9 }		10
	# 10 ...	-
	write_tsv(tokens, output_tsv_file)

def write_tsv(tokens, output_tsv_file):
	header = "line_n\ttoken\ttype_token\tinstruction_n\ttype_instruction\tposition_instruction\n"
	# Quand scope_boucle sera calculé:
	#header = "line_n\ttoken\ttype_token\tinstruction_n\ttype_instruction\tposition_instruction\tscope_boucle\n"
	with open(output_tsv_file, 'w') as f:
		f.write(header)
		for token in tokens:
			string = ""
			for t in token:
				string += str(t) + "\t"
			string = string[:-1] # suppression du dernier \t
			f.write(string + "\n")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Il manque le fichier TS.")
		print("Usage:\n\tpython main.py FICHIER.TSplus (SORTIE.tsv)")
		sys.exit(1)
	if len(sys.argv) > 2:
		output_tsv_file = sys.argv[2]
	else:
		output_tsv_file = ''.join(sys.argv[1].split('.')[:-1]) + '.tsv' # change l'extension en .tsv
	main(sys.argv[1], output_tsv_file)
