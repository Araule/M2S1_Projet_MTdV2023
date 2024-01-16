#!/bin/python3
# -*- coding: utf-8 -*-

def copie_variable(adresse_provenance: int, adresse_destination: int, pos: int) -> str:
	"""
	Cette fonction permet de copier le contenu d'une adresse à une autre adresse
	"""
	script = ""
	dep_pos_adr_dest = abs(pos - adresse_destination)
	
	# On se place au niveau de l'adresse de destination
	script+="% On se place au niveau de l'adresse de destination et on place un 0 au niveau du premier \"bit\"\n"
	if pos > adresse_destination:
		script+="G " * dep_pos_adr_dest
		# pos -= dep_pos_adr_dest
	elif pos < adresse_destination:
		script+="D " * dep_pos_adr_dest
		# pos += dep_pos_adr_dest
	# On place au niveau du premier élément un 0, ce qui est commun à toutes les adresses mémoire pour pouvoir les séparer les unes des autres
	script += "\n0"

	# On calcule la distance entre l'adresse de la variable qu'on veut copier et l'adresse à laquelle on veut la copier

	dep_adr_prov_adr_dest = abs(adresse_provenance - adresse_destination)
	# On initialise la boucle
	script+="\n\n%On initialise la boucle de copie"
	script+="\nboucle\n\t"
	# On se trouve au niveau de l'adresse de destination (adresse_destination[0])
	# Si l'adresse destination est "supérieure" à l'adresse provenance, on doit 
	# se déplacer à gauche pour atteindre l'adresse de provenance
	if adresse_destination > adresse_provenance:
		# On parcourt la distance + 1 pour avancer dans l'adresse de provenance
		# (on se situe au premier tour de boucle à adresse_provenance[1] puis [2], etc
		script+="%On se place au niveau de adresse_provenance[1] (puis 2, puis 3)\n\t"
		script+="G " * (dep_adr_prov_adr_dest-1)
		pos -= (dep_adr_prov_adr_dest-1)
		script+="\n\n\t%Si il y a un 1, on se déplace sur l'adresse de destination à la position correspondante puis on écrit 1"
		script+=("\n\tsi(1)\n\t")
		# On revient à l'adresse de destination (adresse_destination[1] au premier tour)
		script+="D " * (dep_adr_prov_adr_dest)
		pos += (dep_adr_prov_adr_dest)
		script += "\n\t1}"
		script+="\n\n\t%Si il y a un 0, on est arrivé à la fin de notre variable. On se déplace sur l'adresse de destination à la position correspondante puis on écrit 0 et on met fin à la boucle de copie."
		script += "\n\tsi(0)\n\t"
		script+="D " * (dep_adr_prov_adr_dest)
		pos += (dep_adr_prov_adr_dest)
		script+="\n\t0 fin}\n}"
	# Si l'adresse destination est "inférieure" à l'adresse provenance, on doit 
	# se déplacer à droite pour atteindre l'adresse de provenance
	elif adresse_destination < adresse_provenance :
		script+="%On se place au niveau de adresse_provenance[1] (puis 2, puis 3)\n\t"
		script+="D " * (dep_adr_prov_adr_dest+1)
		pos += (dep_adr_prov_adr_dest+1)
		script+=("\n\n\tsi(1)\n\t")
		script+="G " * (dep_adr_prov_adr_dest)
		pos -= (dep_adr_prov_adr_dest)
		script += "\n\t1}"
		script += "\n\n\tsi(0)}\n\t"
		script+="\n\n\t%Si il y a un 0, on est arrivé à la fin de notre variable. On se déplace sur l'adresse de destination à la position correspondante puis on écrit 0 et on met fin à la boucle de copie."
		script += "\n\tsi(0)\n\t"
		script+="G " * (dep_adr_prov_adr_dest)
		pos += (dep_adr_prov_adr_dest)
		script+="\n\t0 fin}\n}"
	script+="\n\n%On est sur le 0 qui \"ferme\" la valeur de notre variable. On doit retourner au début de l'adresse pour savoir où on se trouve sur la bande."
	return script

def revenir_debut_adresse(adresse_variable_actuelle):
	script = ""
	script+="\nboucle"
	script+="\n\t%On fait un pas à gauche pour se situer au niveau du \"dernier\" 1 et on continue de se déplacer tant qu'on ne se situe pas sur le 0 d'initialisation."
	script+="\n\tG\n\tsi(0) fin}\n}"
	script+="\n%Notre pos actuelle correspond à variable_destination[0]\n"
	pos = adresse_variable_actuelle
	return pos, script

def copie_deux_variables_memoire_vive(adresse_1, adresse_2,adresse_mv, pos):
	script1 = copie_variable(adresse_1, adresse_mv, pos)
	pos, script2 = revenir_debut_adresse(adresse_mv)
	script = script1 + script2
	adresse_mv_2 = adresse_mv+32
	script3 = copie_variable(adresse_2, adresse_mv_2, pos)
	pos, script4 = revenir_debut_adresse(adresse_mv_2)
	script += script3 + script4
	script+="\n%On se situe au niveau du 0 d'initialisation de la deuxième variable dans la mémoire vive, donc adresse_memoire_vive + 32"
	return script, pos

def nettoyage_mv(adresse_mv, pos):
	script = "\n%On était au niveau du 0 initialisant la variable qui a été copiée à partir de la mémoire vive.\n%La mémoire vive se situant à la fin de la bande, pos < adresse_mv. On se place au début de la mémoire vive\n"
	distance = adresse_mv - pos
	script+="D " * distance
	script+="\n\n%Il ne reste qu'une valeur dans la mémoire vive, placée au début.\n"
	script+="\n%On efface la mémoire du dernier bâton au premier pour connaître la position de la tête de bande à la fin.\n%On commence donc par chercher la fin de la valeur."
	script+="\nboucle\n\tD\n\tsi(0) fin }\n}"
	script+="\n\n%On est maintenant au niveau du 0 clôturant la valeur."
	script+="\nG "
	script+="\n\n%On est maintenant au niveau du dernier 1 de la valeur."
	script+="\nboucle\n\tsi(1) 0 G }\n\tsi (0) fin }\n}"
	pos = adresse_mv
	return script, pos


if __name__=="__main__":
	adresse1 = 32
	adresse2 = 96
	dest_var_1 = 128
	pos = 0
	# script, pos = copie_deux_variables_memoire_vive(adresse1, adresse2, dest_var_1, pos)
	script, pos = nettoyage_mv(dest_var_1, pos)
	print(script)
	print(pos)
	# print(script)
	# print(f"\n\nposition actuelle : {pos}")