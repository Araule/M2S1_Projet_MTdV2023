from typing import Dict
from copy import deepcopy
from memory_manager import MemoryManager
from collections import defaultdict

input_affectations = {    
    '1': {'D': '0', 'G': 'x'},              # x = 0
    '2': {'D': 'x + 1', 'G': 'x'},          # x = x+1
    '3': {'D': 'x * 2', 'G': 'y'},          # y = x*2
    '8': {'D': 'y', 'G': 'x'}               # x = y
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

    memoire = defaultdict(int)

    # initialisation de la mémoire, avec les constantes
    mm = MemoryManager(input_affectations)
    # copie par valeur, et pas par référence
    memoire[0] = deepcopy(mm.memory)

    # calcul de l'indice maximum
    max_step = 0
    for etape in input_suppressions.keys():
        if int(etape) > max_step:
            max_step = int(etape)

    for i in range(1, max_step+1):
        if str(i) in input_affectations.keys():
            (nom_variable, membre_droite) = (input_affectations[str(i)]['G'], input_affectations[str(i)]['D'])

            membre_droite_ready = False

            if membre_droite.isdigit():
                # c'est une contante, elle doit déjà exister en mémoire
                if mm.isInMemory('CONST_' + str(membre_droite)):
                    membre_droite = mm.bande.lire(mm.memory['CONST_' + str(membre_droite)])
                else:
                    raise ValueError(f"La constante {membre_droite} n'est pas chargée en mémoire")
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
                        raise ValueError(f"La constante {terme1} n'existe pas en mémoire.")
                    terme1_ok = True 
                else:
                    # c'est une variable
                    if mm.isInMemory(terme1):
                        terme1 = mm.readVariable(terme1)
                        terme1_ok = True 
                    else:
                        raise ValueError(f"La variable {terme1} n'existe pas en mémoire")
                    
                if terme2.isdigit():
                    # c'est un constante, il faut aller la lire
                    if mm.isInMemory('CONST_' + terme2):
                        terme2 = mm.readConstant(int(terme2))
                    else:
                        raise ValueError(f"La constante {terme2} n'existe pas en mémoire.")
                    terme2_ok = True 
                else:
                    # c'est une variable
                    if mm.isInMemory(terme2):
                        terme2 = mm.readVariable(terme2)
                        terme2_ok = True 
                    else:
                        raise ValueError(f"La variable {terme2} n'existe pas en mémoire")

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
                mm.add_variable(nom_variable, int(membre_droite))
            else:
                mm.update_variable(nom_variable, int(membre_droite))

        
        elif str(i) in input_suppressions.keys():
            # on supprime les variables demandées
            variables_a_supprimer = input_suppressions[str(i)]
            for var in variables_a_supprimer:
                mm.delete_variable(var)
        
        # fin du tour de boucle, j'enregistre l'état de la mémoire
        memoire[i] = deepcopy(mm.memory)
    
    return memoire

def adresse_memoire_vive(memoire: Dict[int, Dict[int, int]]) -> Dict[int, int]:
    """
        Étant donné l'historique de mémoire instruction par instruction,
        renvoie l'adresse de la mémoire vive à chaque instruction
    """
    memoire_vive = defaultdict(int)
    for instruction in memoire.keys():
        # 32 * nombres de variables et constantes
        adresse_mv = len(memoire[instruction].keys()) * 32
        memoire_vive[instruction] = adresse_mv
    return memoire_vive

#etat = etatMemoire(input_affectations, input_suppressions)

#for i in etat.keys():
#    print(f"Mémoire à l'instruction {i} :")
#    print(etat[i])

#mv = adresse_memoire_vive(etat)
#for (i, adresse) in mv.items():
#    print(f"adresse de la mémoire vive à l'instruction {i} : {adresse}")