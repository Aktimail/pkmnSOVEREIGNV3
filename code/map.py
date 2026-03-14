from npc import NPC
from dynamicTile import DynamicTile


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

    def add_entity(self, env, entity):
        if entity in self.Group:
            return
        self.Group.add(entity)
        self.Group.change_layer(entity, env.entityLayer)
        entity.reset_move()
        if type(entity) is NPC:
            env.npcs.append(entity)

    def add_dynamic_tile(self, env, dbsymbol, x, y, layer=None):
        tile = DynamicTile(dbsymbol, x, y)
        if tile in self.Group:
            return
        layer = env.entityLayer if layer is None else layer
        self.Group.add(tile)
        self.Group.change_layer(tile, layer)
        env.dynamicsTiles.append(tile)

    def remove_dynamic_tile(self, env, tile):
        self.Group.remove(tile)
        env.dynamicsTiles.remove(tile)
