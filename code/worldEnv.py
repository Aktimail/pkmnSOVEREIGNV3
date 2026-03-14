from entityDestinations import entitiesDestinations


class WorldEnv:
    def __init__(self):
        self.tilesTypes = {}
        self.dynamicsTiles = []

        self.gridMap = {}
        self.collisions = []
        self.spawns = []
        self.switches = []
        self.npcs = []
        self.items = []
        self.wildPkmnSpawn = []
        self.destination = None
        self.gate = None
        self.entityLayer = 0

    def clear(self):
        self.tilesTypes.clear()
        self.dynamicsTiles.clear()
        self.collisions.clear()
        self.spawns.clear()
        self.switches.clear()
        self.npcs.clear()
        self.items.clear()
        self.wildPkmnSpawn.clear()
        entitiesDestinations.clear()
