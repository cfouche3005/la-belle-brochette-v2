import random
class Plateforme :
    def __init__(self, coor):
        self.coordonnees = coor

    def get_coor(self):
        return self.coordonnees
    def apparition_plateforme(self):
        x1= self.coordonnees[0]
        x2 = random.randint(-1, 1)
        y1 = self.coordonnees[1]
        y2 = random.randint(-1, 1)
        self.coordonnees = (x1 + x2, y1 + y2)

    def set_y(self,y):
        self.coor =(self.coordonnees[0], y )

    def set_y(self,x):
        self.coor =(x, self.coordonnees[1] )

class Voitures (Plateforme) :
    def __init__(self, coor):
        Plateforme.__init__(self, coor)

class Trottoir (Plateforme) :
    def __init__(self, coor):
        Plateforme.__init__(self, coor)

class Environnement:
    def __init__(self, n_plateformes, n_escaliers, n_portes, n_PU):
        self.n_plateforme= n_plateformes
        self.n_escaliers = n_escaliers
        self.n_portes = n_portes
        self.n_PU = n_PU

    for a in range(n_voitures):
        self.voitures.append(plateformes(random.randint(0, self.width - 1), random.randint(0, self.height - 1)))