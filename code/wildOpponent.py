from abstractOpponent import AbstractOpponent


class WildOpponent(AbstractOpponent):
    def __init__(self, pokemon):
        self.Pokemon = pokemon

    def get_active_pkmn(self):
        return self.Pokemon

    def get_trainer(self):
        return

    def lost(self):
        return self.Pokemon.is_ko()

    def fight(self, move, target, context):
        self.Pokemon.attack(move, target, context)
