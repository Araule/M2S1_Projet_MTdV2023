#!/bin/bash

# Vérifier qu'il y a un argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

TSP=$1

# Vérifier que c'est un lien vers un fichier qui existe, sinon quitter le programme.

if [ ! -f "$TSP" ]; then
    echo "Error: File $TSP not found."
    exit 1
fi

python3 scripts_python/groupe1_analyseurSyntaxique.py "$TSP"

# Check the exit status of script1.py
if [ $? -eq 1 ]; then
    exit 1
fi

# changer l'extension de TSP en .tsv et le ranger dans la variable TSV.
TSV=$(echo "$TSP" | sed 's/\.[^.]*$/.tsv/')

python3 scripts_python/main.py $TSV

# supprimer le fichier TSV.
#rm "$TSV"

TS=ts_generes/$(basename "$TSP" | sed 's/\.[^.]*$/.TS/')

echo "Fichier compilé : $TS"
