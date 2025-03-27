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
        self.coordonnees =(self.coordonnees[0], y )

    def set_x(self,x):
        self.coordonnees =(x, self.coordonnees[1] )

class Voitures(Plateforme) :
    def __init__(self, coor):
        Plateforme.__init__(self, coor)

class Trottoir(Plateforme) :
    def __init__(self, coor):
        Plateforme.__init__(self, coor)

class Banc(Plateforme) :
    def __init__(self, coor):
        Plateforme.__init__(self, coor)


class Elt_Sol:
    def __init__(self, x):
        self.coordonnees = (x, 0)

    def get_coor(self):
        return self.coordonnees

    def apparition_elt_sol(self):
        x1= self.coordonnees[0]
        x2 = random.randint(-1, 1)
        self.coordonnees = (x1 + x2, 0)

    def set_x(self,x):
        self.coordonnees =(x, 0)

class Escaliers (Elt_Sol):
    def __init__(self, coor):
        Elt_Sol.__init__(self, coor)

class Portes (Elt_Sol):
    def __init__(self, coor):
        Elt_Sol.__init__(self, coor)


class PU:
    def __init__(self, plateformes, sol):
        if plateformes and random.choice([True, False]):
            plateforme = random.choice(plateformes)
            self.coordonnees = plateforme.get_coor()
        else:
            x = random.randint(0, sol - 1) #sol est ici le sol du jeu
            self.coordonnees = (x, 0)

    def get_coor(self):
        return self.coordonnees

class Pistolet(PU):
    def __init__(self, plateformes, sol):
        PU.__init__(self, plateformes, sol)

class Crayon(PU):
    def __init__(self, plateformes, sol):
        PU.__init__(self, plateformes, sol)

class Kit_Med(PU):
    def __init__(self, plateformes, sol):
        PU.__init__(self, plateformes, sol)


class Environnement:
    def __init__(self, width, height, n_escaliers, n_portes, n_pistolets, n_crayon, n_KM, n_voitures, n_trottoirs):
        self.width = width
        self.height = height
        self.voitures = []
        self.escaliers = []
        self.portes = []
        self.trottoirs = []
        self.KM = []
        self.pistolets = []
        self.crayons = []

        for a in range(n_trottoirs):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.trottoirs.append(Trottoir(coor))
        for b in range(n_voitures):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.voitures.append(Voitures(coor))
        for c in range(n_escaliers):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.escaliers.append(Escaliers(coor))
        for d in range(n_portes):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.portes.append(Portes(coor))

        for e in range(n_crayon):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.crayons.append(PU(coor))
        for f in range(n_KM):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.KM.append(PU(coor))
        for g in range(n_pistolets):
            coor = (random.randint(0, width - 1), random.randint(0, height - 1))
            self.pistolets.append(PU(coor))

