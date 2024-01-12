class Variable:
   def __init__(self, adresse, nom, valeur):
       self.adresse = adresse
       self.nom = nom
       self.valeur = valeur

   def affecter(self, nouvelle_valeur):
       self.valeur = nouvelle_valeur

   def comparer(self, autre_variable):
       return self.valeur == autre_variable.valeur
   
   def get_adresse(self):
        return self.adresse
   
# le groupe 2 donne : {'x' : 2, 'y' : 1}
