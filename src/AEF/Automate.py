import sys 
sys.path.insert(1, "src/")
from graphviz import Digraph

from AEF.Etat import Etat
from AEF.Transition import Transition
from AEF.TransitionND import TransitionND

class Automate:
    def __init__(self):
        self.commentaire = ""
        self.meta = "#"
        self.entrees = []
        self.sorties = []
        self.etats = []
        self.transitions = []

    def getFirstEtatInit(self):
        for e in self.etats:
            if e.isInit:
                return e
                break

    def getTransition(self, etatEntree, entree):
        transitions = []
        for t in self.transitions:
            if etatEntree == t.etatEntree:
                if entree == t.entree:
                    transitions.append(t)
        return transitions

    def getInits(self):
        finits = []
        for e in self.etats:
            if e.isInit:
                finits.append(e) 
        return finits

    def getFinaux(self):
        etats = []
        for e in self.etats:
            if e.isFinit:
                etats.append(e)
        return etats

    def findEtat(self, etat):
        isPresent = False
        for e in self.etats:
            if etat.numero == e.numero:
                isPresent = True
                break
        return isPresent
    
    def addEtat(self, etat):
        if not self.findEtat(etat):
            self.etats.append(etat)

    def getEtat(self, numero):
        for etat in self.etats:
            if etat.numero == numero:
                return etat
                break
        return None

    def showInfo(self):
        print("="*50)
        print("                     AUTOMATE")
        print("-"*50)
        print("C comment: " + self.commentaire)
        print("M meta: " + self.meta)
        etats = ""
        for e in self.etats:
            etats = etats + ("\t" + e.toString() + "\n")
        print("Etats:  \n" + etats)
        
        trans = ""
        for t in self.transitions:
            trans = trans + ("\t" + t.toString() + "\n")
        print("T trans: \n" + trans)
        print("="*50)

    def generateGraph(self):
        if not self.commentaire:
            graph = Digraph()
        else:
            graph = Digraph(comment=self.commentaire)

        for etat in self.etats:
            if etat.isFinit:
                graph.node(str(etat.numero), shape="doublecircle")
            else:
                graph.node(str(etat.numero))
        for trans in self.transitions:
            graph.edge(str(trans.etatEntree.numero), str(trans.etatSortie.numero), trans.entree+"/"+trans.sortie)

        return graph

