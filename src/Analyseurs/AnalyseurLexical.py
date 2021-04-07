import sys 
import re
sys.path.insert(1, "src/")

from AEF.Etat import Etat
from AEF.Transition import Transition
from AEF.Automate import Automate

class AnalyseurLexical:
    def __init__(self, data):
        self.C = ""
        self.M = "#"
        self.V = ""
        self.O = ""
        self.E = ""
        self.I = []
        self.F = []
        self.T = []

        self.automate = Automate()
        
        self.automate = Automate()
        for line in data:
            values = line.split(" ")
            if(values[0] == "C"):
                self.C = line
            elif(values[0] == "M"):
                self.M = values[1]
            elif(values[0] == "V"):
                vValue = values[1].replace('"', "")
                self.V = list(vValue)
            elif(values[0] == "O"):
                oValue = values[1].replace('"', "")
                self.O = list(oValue)
            elif(values[0] == "E"):
                self.E = values[1]
            elif(values[0] == "I"):
                values.pop(0)
                liste = list(values)
                for v in liste:
                    if v != int:
                        v = int(v)
                    self.I.append(v)
            elif(values[0] == "F"):
                values.pop(0)
                liste = list(values)
                for v in liste:
                    if v != int:
                        v = int(v)
                    self.F.append(v)
            elif(values[0] == "T"):
                tValues = []
                values.pop(0)
                for tValue in values:
                    tValues.append(tValue.replace("'", ""))
                if len(tValues) == 3:
                    tValues.append("#")
                self.T.append(tValues)

        if len(self.I) == 0:
            self.I.append(0)
    
    def createAutomate(self):
        if len(self.C) != 0:
            self.automate.comment = self.C
        if len(self.M) != 0:
            self.automate.meta = self.M
        
        #Ajouter les etats dans automate
        for t in self.T:
            etat = Etat()
            etat.numero = int(t[0])
            if etat.numero in self.I:
                etat.isInit = True
            if etat.numero in self.F:
                etat.isFinit = True
            self.automate.addEtat(etat)
        for t in self.T:
            etat = Etat()
            etat.numero = int(t[2])
            if etat.numero in self.I:
                etat.isInit = True
            if etat.numero in self.F:
                etat.isFinit = True
            self.automate.addEtat(etat)

        #Ajouter les transactions dans automate
        for t in self.T:
            etatEntree = self.automate.getEtat(int(t[0]))
            etatSortie = self.automate.getEtat(int(t[2]))
            entree = t[1]
            if len(t) == 4:
                sortie = t[3]
            else:
                sortie = "#"
            trans = Transition(etatEntree, etatSortie, entree, sortie)
            self.automate.transitions.append(trans)

        #Ajouter les entréers et les sorties dans l'Automate()
        entrees = []
        for t in self.T:
            if not t[1] in entrees:
                entrees.append(t[1])
        self.automate.entrees = entrees

        sorties = []
        for t in self.T:
            if not t[3] in sorties:
                sorties.append(t[3])
        self.automate.sorties = sorties

    def checkInputs(self, entry):
        isValid = True
        values = list(entry)
        for value in values:
            if not value in self.automate.entrees:
                isValid = False
                break
        return isValid

    def analyseLexical(self):        
        #On va analyser chaque donnée entrée
        while True:
            print("Veuillez saisir les phrases à lire :")
            print("(Chaque phrase est terminée par ENTREE. La lecture des phrases est terminée par ###)")
            inputs = []
            
            #si l'automate n'a pas des transitions qu'on fais rien
            if(len(self.automate.transitions) == 0):
                print("="*50)
                print("                     ATTENTION")
                print("Cette automate n'a pas de transactions. \nVeuillez choisir un autre automate")
                print("="*50)
                break
            else:
                #Récuper les entrées pour l'analyse après
                while True:
                    entry = input()
        
                    if entry == "###":
                        break
                    else : 
                        x = re.search("[a-zA-Z0-9_]", entry)
                        if x:
                            if self.checkInputs(entry):
                                inputs.append(entry)
                            else:
                                print("Entrée non valide")
                        else :
                            print("Entrée non valide")
                
                #Prendre le premier état initial
                pos = self.automate.getFirstEtatInit()

                #Analyse ligne par ligne
                for ligne in inputs:
                    outputs = ""
                    print("Traitement des phrases lues : " + ligne )

                    #Analyse mot par mot
                    for c in ligne:
                        #Récupere les transitions correspondance à l'état actuel
                        transition = self.automate.getTransition(pos, c)
                        if len(transition) == 0:
                            print("Etat courant: " + str(pos.numero) + ", Entrée: " + c + ", Transaction non trouvée")
                        else:
                            sortie = " Transaction trouvée"
                            if transition[0].sortie != "#":
                                sortie = "Sortie: " + transition[0].sortie +  sortie
                                outputs = outputs + transition[0].sortie
                            print("Etat courant: " + str(pos.numero) + ", Entrée: " + c + ", " + sortie)
                            pos = transition[0].etatSortie

                    if pos.isFinit:
                        print("Entrée acceptante")
                    else :
                        print("Entrée non acceptante")

                    if len(outputs) == 0:
                        print("La sortie de cette phrase est : NULL")
                    else :
                        print("La sortie de cette phrase est : " + outputs)
                    print("-- Fin de phrase --")
                print("Fin de traitement")
                break
            
