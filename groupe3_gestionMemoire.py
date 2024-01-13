from memory_manager import MemoryManager

input_affectations = {    
    '1': {'D': '0', 'G': 'x'},
    '2': {'D': 'x + 1', 'G': 'x'},
    '3': {'D': 'x * 2', 'G': 'y'},
    '8': {'D': 'y', 'G': 'x'}
}

input_suppressions = {
    '10': ['x', 'y']
}

def etatMemoire(input_affectations, input_suppressions):
    """
        Prend en entrée le dictionnaire du groupe 2, qui à chaque numéro d'instruction
        associe les membres gauches et droits d'une affectation

        Renvoie en sortie un dictionnaire qui pour chaque instruction du programme contient les variables
        et constantes en mémoire et leur adresse
    """

    memoire = {}

    mm = MemoryManager()

    # calcul de l'indice maximum
    max_step = 0
    for etape in input_suppressions.keys():
        if int(etape) > max_step:
            max_step = int(etape)
    print("indice max : " + str(max_step))

    for i in range(1, max_step+1):
        print()
        if str(i) in input_affectations.keys():
            #print(f"Étape n°{i}")
            (nom_variable, membre_droite) = (input_affectations[str(i)]['G'], input_affectations[str(i)]['D'])
            #print(f"membre de gauche : {nom_variable}, membre de droite : {membre_droite}")

            membre_droite_ready = False

            if membre_droite.isdigit():
                # c'est une contante, je l'enregistre en mémoire si elle n'existe pas déjà
                #print("C'est une constante !")
                if mm.isInMemory('CONST_' + str(membre_droite)):
                    membre_droite = mm.bande.lire(mm.memory['CONST_' + str(membre_droite)])
                else:
                    mm.add_constant(int(membre_droite))
                    membre_droite = mm.bande.lire(mm.memory['CONST_' + str(membre_droite)])
                membre_droite_ready = True 
            elif len(membre_droite) == 1:
                # le membre de droite est une variable, qu'il faut aller lire !
                if not mm.isInMemory(membre_droite):
                    print(f"Erreur : la variable {membre_droite} n'existe pas en mémoire")
                    exit(1)
                else:
                    membre_droite = mm.readVariable(membre_droite)
                    membre_droite_ready = True 
            else:
                # c'est un truc de la forme 'x + 1'
                (terme1, operateur, terme2) = membre_droite.split(" ")
                terme1_ok = False 
                terme2_ok = False
                # il faut résoudre ça

                if terme1.isdigit():
                    # c'est un constante, il faut aller la lire
                    if mm.isInMemory('CONST_' + terme1):
                        terme1 = mm.readConstant(int(terme1))
                    else:
                        mm.add_constant(int(terme1))
                        terme1 = mm.readConstant(int(terme1))
                    
                    terme1_ok = True 
                else:
                    # c'est une variable
                    if mm.isInMemory(terme1):
                        terme1 = mm.readVariable(terme1)
                        terme1_ok = True 
                    else:
                        print(f"La variable {terme1} n'existe pas en mémoire")
                    
                if terme2.isdigit():
                    # c'est un constante, il faut aller la lire
                    if mm.isInMemory('CONST_' + terme2):
                        terme2 = mm.readConstant(int(terme2))
                    else:
                        mm.add_constant(int(terme2))
                        terme2 = mm.readConstant(int(terme2))
                    
                    terme2_ok = True 
                else:
                    # c'est une variable
                    if mm.isInMemory(terme2):
                        terme2 = mm.readVariable(terme2)
                        terme2_ok = True 
                    else:
                        print(f"La variable {terme2} n'existe pas en mémoire")

                if terme1_ok and terme2_ok:
                    # on continue, on gère l'opérateur (+ ou *)
                    if operateur == "+":
                        membre_droite = terme1 + terme2 
                        membre_droite_ready = True 
                    elif operateur == "*":
                        membre_droite = terme1 * terme2 
                        membre_droite_ready = True 
                    else:
                        print("Opérateur invalide")
                        exit(1)
                else:
                    print("Erreur dans le parsing du membre de droite")
                    exit(1)

            # Arrivé ici, on devrait avoir un membre de droite valide.
            if not mm.isInMemory(nom_variable):
                #print(f"Type de nom_variable : {type(nom_variable)}")
                #print(f"Type de membre_droite : {type(membre_droite)}, valeur = {membre_droite}")
                mm.add_variable(nom_variable, int(membre_droite))
                #print("La variable a bien été ajoutée !")
            else:
                mm.update_variable(nom_variable, int(membre_droite))
                #print("La variable a bien été mise à jour ! ")
        
            #mm.afficher_memoire()
            memoire[i] = mm.memory
        
        elif str(i) in input_suppressions.keys():
            #print(f"Étape n°{i}")
            # on supprime les variables demandées
            variables_a_supprimer = input_suppressions[str(i)]
            for var in variables_a_supprimer:
                mm.delete_variable(var)
            #mm.afficher_memoire()

        else:
            #print(f"Étape n°{i}")
            #mm.afficher_memoire()
            memoire[i] = mm.memory
    
    return memoire

#etatMemoire(input_affectations, input_suppressions)