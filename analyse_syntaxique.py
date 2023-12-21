#!/bin/python3
# -*- coding: utf-8 -*-

import sys

import tokenize

import os

def main(file):
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
	print(lines)
	tokens = tokenize.make_tokens(lines, lines_number)
	print(tokens)
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

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Il manque le fichier TS.")
		print("Usage:\n\tpython main.py FICHIER.TS")
		sys.exit(1)
	main(sys.argv[1])
