import os
import re
from graphviz import Digraph
from Analyseurs.AnalyseurLexical import AnalyseurLexical
from AEF import Automate
from AEF.Etat import Etat
from Analyseurs.AEFND import AEFND

#Est un chiffre ?
def isDigit(entree): 
    regex = re.search("[^a-zA-Z]", entree)
    if regex:
        return True
    else:
        return False

#Récupere la liste des fichiers dans un répertoire
def getFiles(path):
    files = []
    for f in os.listdir(path):
        if ".descr" in f:
            files.append(f)
    files.sort()
    return files

#Recupere tous les données dans un fichier 
def get_data_one_file(path):
    data = []
    f = open(path, "r")

    for l in f.readlines():
        data.append(l.split("\n")[0])
    return data

#Généner tous les graphs à partir d'un répertoire
def generate_all_graphs(files, dirIn, dirOut):

    for file in files:
        data = get_data_one_file(dirIn+file)
        analyseur = AnalyseurLexical(data)
        analyseur.createAutomate()
        graph = analyseur.automate.generateGraph()
        graph.format = "png"
        graph.render(dirOut+file, view=False)
        print(graph.source)

#Afficher menu AEF
def menuAEF(files, directory):
    while True:
        i = 1
        #Afficher la liste des automates
        print("--------Menu Automate--------")
        for f in files:
            print(str(i) + " - " + f)
            i += 1
        print(str(i) + " - Retour au menu précédent.")
        print("Veullez choisir un fichier:")
        entree = input()
        #Vérifier si input est valide
        if isDigit(entree):
            entree = int(entree)
            if entree in range(1, i+1):
                if entree == i:
                    break
                else: 
                    data = get_data_one_file(directory+files[entree-1])
                    analyseur = AnalyseurLexical(data)
                    analyseur.createAutomate()
                    analyseur.automate.showInfo()
                    analyseur.analyseLexical()
            else: 
                print("La saisie n'est pas valide. \nVeuillez réessayer!\n")
        else:
            print("La saisie n'est pas valide. \nVeuillez réessayer!\n")


def menuAEFND(files, directory):
    while True:
        i = 1
        #Afficher la liste des automates
        print("--------Menu Automate--------")
        for f in files:
            print(str(i) + " - " + f)
            i += 1
        print(str(i) + " - Retour au menu précédent.")
        print("Veullez choisir un fichier:")
        entree = input()
        #Vérifier si input est valide
        if isDigit(entree):
            entree = int(entree)
            if entree in range(1, i+1):
                if entree == i:
                    break
                else :
                    fileName = files[entree-1]
                    data = get_data_one_file(directory+fileName)
                    analyseur = AnalyseurLexical(data)
                    analyseur.createAutomate()
                    #transformer de AEFND à AEFD
                    nonDer = AEFND(analyseur.automate)
                    nonDer.automate.showInfo()
                    nonDer.determiniser()
                    nonDer.automate.showInfo()
                    while True:
                        print("----------Analyse AEFND----------")
                        print("1 - Analyse d'entrée")
                        print("2 - Générer l'automate en descr et en png")
                        print("3 - Retour au menu précédent")
                        print("Veullez choisir une option:")
                        entree = input()
                        if isDigit(entree):
                            entree = int(entree)
                            if entree in range(1, 3):
                                if entree == 1:
                                    analyseur.automate = nonDer.automate
                                    analyseur.automate.showInfo()
                                    analyseur.analyseLexical()
                                if entree == 2:
                                    graph = analyseur.automate.generateGraph()
                                    graph.format = "png"
                                    graph.render("Grpah_Deters/"+fileName, view=False)
                                    print(graph.source)
                                if entree == 3:
                                    break
                            else:
                                print("La saisie n'est pas valide. \nVeuillez réessayer!\n")
                        else: 
                            print("La saisie n'est pas valide. \nVeuillez réessayer!\n")

            else: 
                print("La saisie n'est pas valide. \nVeuillez réessayer!\n")
        else:
            print("La saisie n'est pas valide. \nVeuillez réessayer!\n")

def Moteur():
    moteursPath = "data/Test_Moteur/"
    detersPath = "data/Test_Determinisation/"
    Moteurs = getFiles(moteursPath)
    Deters = getFiles(detersPath)
    menu = ["Generer les graphes.", "Automate AEF.", "AEFND"]

    while True:
        i = 1
        print("--------Menu Principal--------")
        for m in menu:
            print(str(i) + " - " + m)
            i += 1
        print(str(i) + " - Quitter" )
        print("Veullez choisir une option:")
        entree = input()
        if isDigit(entree):
            entree = int(entree)
            if entree in range(1, i+1):
                if entree == 1:
                    generate_all_graphs(Moteurs, moteursPath, "Graph_Moteurs/")
                    generate_all_graphs(Deters, detersPath, "Graph_Non_Deters/")
                if entree == 2:
                    menuAEF(Moteurs, moteursPath)
                if entree == 3:
                    menuAEFND(Deters, detersPath)
                if entree == i:
                    break
            else:
                print("La saisie n'est pas valide. \nVeuillez réessayer!\n")
        else:
            print("La saisie n'est pas valide. \nVeuillez réessayer!\n")

Moteur()