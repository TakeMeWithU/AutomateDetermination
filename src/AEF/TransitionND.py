import sys 
sys.path.insert(1, "src/")
from AEF.Etat import Etat

class TransitionND:

    def __init__(self, etatEntree, etatSortie, c):
        self.etatEntree = etatEntree
        self.etatSortie = etatSortie
        self.caractere = c

    def toString(self):
        string = "EtatEntree: "
        for etat in self.etatEntree:
            string = string + etat.toString()
        return string