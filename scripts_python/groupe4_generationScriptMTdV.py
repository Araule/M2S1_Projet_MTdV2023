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
    script+="\n%%%%%%%%% COPIE_VARIABLE"
    script+="\n% On se place au niveau de l'adresse de destination et on place un 0 au niveau du premier \"bit\"\n"
    if pos > adresse_destination:
        script+="G " * dep_pos_adr_dest
    elif pos < adresse_destination:
        script+="D " * dep_pos_adr_dest
    script += "\n0"

    # On calcule la distance entre l'adresse de la variable qu'on veut copier et l'adresse à laquelle on veut la copier

    dep_adr_prov_adr_dest = abs(adresse_provenance - adresse_destination)
    script+="\n\n% On initialise la boucle de copie"
    script+="\nboucle\n "
    # On se trouve au niveau de l'adresse de destination (adresse_destination[0])
    # Si l'adresse destination est "supérieure" à l'adresse provenance, on doit 
    # se déplacer à gauche pour atteindre l'adresse de provenance
    if adresse_destination > adresse_provenance:
        # On parcourt la distance + 1 pour avancer dans l'adresse de provenance
        # (on se situe au premier tour de boucle à adresse_provenance[1] puis [2], etc
        script+="\n% On se place au niveau de adresse_provenance[1] (puis 2, puis 3)\n "
        script+="G " * (dep_adr_prov_adr_dest-1)
        pos -= (dep_adr_prov_adr_dest-1)
        script+="\n\n % Si il y a un 1, on se déplace sur l'adresse de destination à la position correspondante puis on écrit 1"
        script+=("\n si(1)\n ")
        # On revient à l'adresse de destination (adresse_destination[1] au premier tour)
        script+="D " * (dep_adr_prov_adr_dest)
        pos += (dep_adr_prov_adr_dest)
        script += "\n 1}"
        script+="\n\n % Si il y a un 0, on est arrivé à la fin de notre variable. On se déplace sur l'adresse de destination à la position correspondante puis on écrit 0 et on met fin à la boucle de copie."
        script += "\n si(0)\n "
        script+="D " * (dep_adr_prov_adr_dest)
        pos += (dep_adr_prov_adr_dest)
        script+="\n 0 fin }\n}"
    # Si l'adresse destination est "inférieure" à l'adresse provenance, on doit 
    # se déplacer à droite pour atteindre l'adresse de provenance
    elif adresse_destination < adresse_provenance :
        script+="\n% On se place au niveau de adresse_provenance[1] (puis 2, puis 3)\n "
        script+="D " * (dep_adr_prov_adr_dest+1)
        pos += (dep_adr_prov_adr_dest+1)
        script+=("\n\n si(1)\n ")
        script+="G " * (dep_adr_prov_adr_dest)
        pos -= (dep_adr_prov_adr_dest)
        script += "\n 1 }"
        # script += "\n\n si(0)}\n "
        script+="\n\n %Si il y a un 0, on est arrivé à la fin de notre variable. On se déplace sur l'adresse de destination à la position correspondante puis on écrit 0 et on met fin à la boucle de copie."
        script += "\n si(0)\n "
        script+="G " * (dep_adr_prov_adr_dest)
        pos += (dep_adr_prov_adr_dest)
        script+="\n 0 fin }\n}"
    script+="\n\n%On est sur le 0 qui \"ferme\" la valeur de notre variable. On doit retourner au début de l'adresse pour savoir où on se trouve sur la bande."
    return script

def revenir_debut_adresse(adresse_variable_actuelle):
    script = ""
    script+="\n%%%%%%%%% REVENIR DEBUT ADRESSE"
    script+="\nboucle"
    script+="\n %On fait un pas à gauche pour se situer au niveau du \"dernier\" 1 et on continue de se déplacer tant qu'on ne se situe pas sur le 0 d'initialisation."
    script+="\n G\n si(0) fin }\n}"
    script+="\n%Notre pos actuelle correspond à variable_destination[0]"
    pos = adresse_variable_actuelle
    return script, pos

def copie_deux_variables_memoire_vive(adresse_1, adresse_2,adresse_mv, pos):
    script = ""
    script += "\n%%%%%%%%% COPIE_VARIABLE"
    script1, pos = copie_variable(adresse_1, adresse_mv, pos)
    script2, pos = revenir_debut_adresse(adresse_mv)
    script = script1 + script2
    adresse_mv_2 = adresse_mv+32
    script3, pos = copie_variable(adresse_2, adresse_mv_2, pos)
    script4, pos = revenir_debut_adresse(adresse_mv_2)
    script += script3 + script4
    script+="\n%On se situe au niveau du 0 d'initialisation de la deuxième variable dans la mémoire vive, donc adresse_memoire_vive + 32"
    return script, pos

###############
# COMPARAISONS
###############
def comparaison(adresse_variable1, adresse_variable2, pos) : 
    code_mdtv = "" 
    code_mdtv += "\n%%%%%%%%% COMPARAISON\n"
    distance_ad1_ad2 = abs(adresse_variable1 - adresse_variable2)
    # beginV1, endv1 = get_position(variable1)
    # beginV2, endV2 = get_position(variable2)
    #si la position actuelle est différent que position de variable avec laquelle on compare 
    if pos != adresse_variable1 : 
        #on cherche la valeur de distance absolue
        to_variable1 = abs(pos - adresse_variable1)
        #on regarde s'il faut bouger à gauche ou à droite
        if pos > adresse_variable1 : 
            instr, delta = "G ", -1
        else : 
            instr, delta = "D ", 1        
        # on bouge autant de fois qu'il faut pour se deplacer à la variable 1 et génération du code équivalent.
        code_mdtv += instr * to_variable1
        pos += delta * to_variable1
    
    #pour définir les directions entre les variables
    if adresse_variable1 < adresse_variable2 : 
    	v1_to_v2 = "D "
    	v2_to_v1 = "G "
    else:
    	v1_to_v2 = "G "
    	v2_to_v1 = "D "

    code_mdtv += "\nboucle"
    code_mdtv += "\n % on se place sur le supposé premier baton de la variable 1"
    code_mdtv += "\n D"
    code_mdtv += "\n % on vérifie que c'est bien un baton, si c'est le cas on va au niveau de la position équivalente à v1 de v2"
    code_mdtv += "\n si(1) " + v1_to_v2*distance_ad1_ad2
    code_mdtv += "\n  % si c'est différent de v1, on retourne sur l'adresse de v1"
    code_mdtv += "\n  si(0)"
    code_mdtv += "\n   " + v2_to_v1*distance_ad1_ad2
    code_mdtv += "\n   boucle G si(0) fin } }"
    code_mdtv += "\n  }"
    code_mdtv += "\n  " + v2_to_v1*distance_ad1_ad2
    code_mdtv += "\n }"
    code_mdtv += "\n % on arrive à la fin de la variable 1"
    code_mdtv += "\n si(0) " + v1_to_v2*distance_ad1_ad2
    code_mdtv += "\n % si v2 est différent, on retourne à l'adresse de v1"
    code_mdtv += "\n  si(1)"
    code_mdtv += "\n   " + v2_to_v1*distance_ad1_ad2
    code_mdtv += "\n   boucle G si(0) fin } }"
    code_mdtv += "\n  }"
    code_mdtv += "\n  % si v1==v2 alors on se place sur le premier baton de v1"
    code_mdtv += "\n  " + v2_to_v1*distance_ad1_ad2
    code_mdtv += "\n  boucle G si(0) fin } }"
    code_mdtv += "\n  D"
    code_mdtv += "\n }"
    code_mdtv += "\n}"
    code_mdtv += "\n% si on est sur un 1 alors v1==v2 et on se place sur l'adresse de v1, sinon v1!=v2 et on ne bouge pas"
    code_mdtv += "\nsi(1) G "
    return code_mdtv, pos

#############
# OPÉRATIONS
#############
def addition(adresse_var1, adresse_var2, pos_bande, pos_memoire_vive):
    script = "\n%%%%%%%%% ADDITION"
    script1, pos_bande = copie_deux_variables_memoire_vive(adresse_var1, adresse_var2, pos_memoire_vive, pos_bande)
    script += script1
    distance = abs(pos_memoire_vive - pos_bande)
    script += "G " * distance
    pos_bande -= distance
    script += "D \n" # on se place sur le premier baton de la premiere valeur de MV
    pos_bande += 1
    with open("TS/addition.TS", 'r') as fin:
        script += fin.read()
    script += "\n"
    return script, pos_bande

def multiplication(adresse_var1, adresse_var2, pos_bande, pos_memoire_vive):
    script += "\n%%%%%%%%% MULTIPLICATION"
    script1, pos_bande = copie_deux_variables_memoire_vive(adresse_var1, adresse_var2, pos_memoire_vive, pos_bande)
    script += script1
    distance = abs(pos_memoire_vive - pos_bande)
    script += "G " * distance
    pos_bande -= distance
    script += "D \n" # on se place sur le premier baton de la premiere valeur de MV
    pos_bande += 1
    print(pos_bande) 
    with open("TS/multiplication.TS", 'r') as fin:
        script += fin.read()
    script += "\n"
    return script, pos_bande

def nettoyage_mv(adresse_mv, pos):
    script = "\n%%%%%%%%% COPIE_VARIABLE"
    script += "\n%On était au niveau du 0 initialisant la variable qui a été copiée à partir de la mémoire vive.\n%La mémoire vive se situant à la fin de la bande, pos < adresse_mv. On se place au début de la mémoire vive"
    distance = adresse_mv - pos
    script+="D " * distance
    script+="\n\n%Il ne reste qu'une valeur dans la mémoire vive, placée au début."
    script+="\n%On efface la mémoire du dernier bâton au premier pour connaître la position de la tête de bande à la fin.\n%On commence donc par chercher la fin de la valeur."
    script+="\nboucle\n D\n si(0) fin }\n}"
    script+="\n\n%On est maintenant au niveau du 0 clôturant la valeur."
    script+="\nG "
    script+="\n\n%On est maintenant au niveau du dernier 1 de la valeur."
    script+="\nboucle\n si(1) 0 G }\n si(0) fin }\n}"
    pos = adresse_mv
    return script, pos
