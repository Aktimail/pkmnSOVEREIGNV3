class AbstractOpponent:
    def get_active_pkmn(self): ...
    def get_trainer(self): ...
    def lost(self): ...
    def attack(self, move, target, context): ...
