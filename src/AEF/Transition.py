import sys 
sys.path.insert(1, "src/")
from AEF.Etat import Etat

class Transition:

    def __init__(self, etatEntree, etatSortie, entree, sortie):
        self.etatEntree = etatEntree
        self.etatSortie = etatSortie
        if entree == None:
            self.entree = entree
        else:
            self.entree = entree
        if sortie == None:
            self.sortie = "#"
        else:
            self.sortie = sortie
        

    def toString(self):
        return "EtatEntree: " + str(self.etatEntree.numero) + ", EtatSortie: " + str(self.etatSortie.numero) + ", Entree: " + self.entree + ", Sortie: " + self.sortie + ";"
