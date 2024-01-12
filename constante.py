from variable import Variable

class Constante(Variable):
  def __init__(self, adresse, nom, valeur):
      super().__init__(adresse, nom, valeur)