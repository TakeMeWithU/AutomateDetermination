class Etat:
    def __init__(self):
        self.numero = 0
        self.isInit = False
        self.isFinit = False

    def toString(self):
        return "Etat: " + str(self.numero) + ", isInit: " + str(self.isInit) + ", isFinit: " + str(self.isFinit) + ";"