import sys 
import re

sys.path.insert(1, "src/")

from AEF.Etat import Etat
from AEF.Transition import Transition
from AEF.Automate import Automate
from AEF.TransitionND import TransitionND

class AEFND:
    def __init__(self, automate):
        self.automate = automate
    
    #Récupérer toutes les transitions de l'état entrant
    def getTransitionsOf(self, etat):
        T = []
        for t in self.automate.transitions:
            if etat == t.etatEntree:
                T.append(t)
        return T

    def lambda_fermeture(self, T):
        F = []                 #Liste de sortie
        P = []                 #Liste manipulé pendant l'opération

        for e in T:
            P.append(e)
        
        while P != []:
            t = P[len(P)-1]
            if not t in F:
                F.append(t)
                trans_t = self.getTransitionsOf(t)
                for t2 in trans_t:
                    if t2.entree == self.automate.meta:
                        P.append(t2.etatSortie)
            P.remove(t)
        return F

    #Récupérer la liste tous les états 
    def transiter(self, T, a):
        F = []
        for e in T:
            trans = self.getTransitionsOf(e)
            for t in trans:
                if t.entree == a:
                    u = t.etatSortie
                    if not u in F:
                        F.append(u)
        return F
        
    def toAutomate(self, L, D):
        etats = []
        transitions = []

        for e in L:
            etat = Etat()
            etat.numero = L.index(e)
            etats.append(etat)
        etats[0].isInit = True

        for t in D:
            e = etats[L.index(t.etatEntree)]

            for a in t.etatEntree:
                if a.isFinit:
                    e.isFinit = True
            
            s = etats[L.index(t.etatSortie)]
            
            transition = Transition(e, s, t.caractere, sortie=None)
            transitions.append(transition)

        self.automate.etats = etats
        self.automate.transitions = transitions

            
    def determiniser(self):
        #Initialise la pile avec les lambda-fermetures des états initiaux
        P = []
        P.append(self.lambda_fermeture(self.automate.getInits()))

        #Liste des ensembles d'états générés
        L = []

        #Liste des transitions générées
        D = []

        #Vocabulaire d'entrée
        voc = self.automate.entrees

        voc.remove(voc[len(voc)-1])

        while P != []:
            T = P[0]
            if not T in L:
                L.append(T)
                for c in voc:
                    U = self.lambda_fermeture(self.transiter(T, c))
                    transitionND = TransitionND(T, U, c)
                    D.append(transitionND)
                    P.append(U)
            P.remove(T)
        
        self.toAutomate(L, D)
                