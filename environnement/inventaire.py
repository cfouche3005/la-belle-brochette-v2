class Inventaire:
    def __init__(self):
        self.pistolet = None
        self.km = None
        self.crayon = None

    def max_pistolet(self, pistolet):
        if self.pistolet == 0:
            print("perso peut prendre un pistolet")
        elif self.pistolet == 1:
            print("perso ne peut pas prendre un pistolet")


