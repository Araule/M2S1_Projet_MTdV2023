#!/bin/python3
# -*- coding: utf-8 -*-


#################
# COPIE VARIABLE 
#################
def copie_variable(adresse_provenance: int, adresse_destination: int, pos: int) -> str:
	"""
	Cette fonction permet de copier le contenu d'une adresse à une autre adresse
	"""
	script = ""
	dep_pos_adr_dest = abs(pos - adresse_destination)
	
	script+="% On se place au niveau de l'adresse de destination et on place un 0 au niveau du premier \"bit\"\n"
	if pos > adresse_destination:
		script+="G " * dep_pos_adr_dest
	elif pos < adresse_destination:
		script+="D " * dep_pos_adr_dest
	script += "\n0"

	# On calcule la distance entre l'adresse de la variable qu'on veut copier et l'adresse à laquelle on veut la copier

	dep_adr_prov_adr_dest = abs(adresse_provenance - adresse_destination)
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

###############
# COMPARAISONS
###############
def comparaison(variable1, variable2,pos, bande) : 
    code_mdtv = "" 
    beginV1, endv1 = get_position(variable1)
    beginV2, endV2 = get_position(variable2)
    #si la position actuelle est différent que position de variable avec laquelle on compare 
    if pos != beginV1 : 
        #on cherche la valeur de distance absolue
        to_variable = abs(pos-beginV1)
        #on regarde s'il faut bouger à gauche ou à droite
        if pos > beginV1 : 
            instr, delta = "G ", -1
        else : 
            instr, delta = "D ", 1
        #on bouge autant de fois qu'il faut pour se deplacer à la variable 1 et génération du code équivalent.
        for i in range(to_variable) : 
            code_mdtv = code_mdtv + instr
            pos+=delta
        #indentation pour le code jolie et propre 
        tab = 0
        #parcours de la variable 2, dans x==2, ça sera 2, car on veut que X soit égaux à 2
        #donc on prend index de début de la variable et index de la fin
        for i in range(beginV2, endV2-1) : 
            #génération des 0 ou des 1 selon ce qui est rencontré dans la variable 2
            cond = bande[i]
            #compteur des identations
            implement = "\t"*tab
            #écriture de condition
            code_mdtv+=f"\n{implement}si({cond}) D"
            tab+=1
            pos+=1
        #dernier condition ne nécessite par de bougement à droite
        code_mdtv+=f"\n\t{implement}si({bande[endV2]})"
        tab+=1
        #fin d'instruction
        code_mdtv+=" fin }"
        #fermeture avec des accolades
        for i in range(tab) :
            tab-=1
            implement = "\t"*tab
            code_mdtv+=f"\n{implement}"+"}\n" 
    return code_mdtv, pos

#############
# OPÉRATIONS
#############
def addition(pos, addresse_var1, addresse_var2):
    script, pos = copie_deux_variables_memoire_vive(addresse_var1, addresse_var2, ADDRESSE_MV, pos)
    distance = abs(ADDRESSE_MV - pos)
    script += "G " * distance
    pos -= distance
    script += "D \n" # on se place sur le premier baton de la premiere valeur de MV
    pos += 1
    with open("TS/addition.TS", 'r') as fin:
        script += fin.read()
    return script, pos

def multiplication(pos, addresse_var1, addresse_var2):
    script, pos = copie_deux_variables_memoire_vive(addresse_var1, addresse_var2, ADDRESSE_MV, pos)
    distance = abs(ADDRESSE_MV - pos)
    script += "G " * distance
    pos -= distance
    script += "D \n" # on se place sur le premier baton de la premiere valeur de MV
    pos += 1
    print(pos) 
    with open("TS/multiplication_bis.TS", 'r') as fin:
        script += fin.read()
    return script, pos


