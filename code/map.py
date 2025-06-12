class Map:
    def __init__(self, dbsymbol):
        self.dbSymbol = dbsymbol

        self.TmxData = None
        self.MapLayer = None
        self.Group = None

    def update(self, player):
        self.Group.update()
        self.Group.center(player.rect.center)

    def render(self, screen):
        self.Group.draw(screen.display)
