from abstractOpponent import AbstractOpponent


class TrainerOpponent(AbstractOpponent):
    def __init__(self, trainer):
        self.Trainer = trainer

    def get_active_pkmn(self):
        return self.Trainer.get_active_pkmn()

    def get_trainer(self):
        return self.Trainer

    def lost(self):
        return self.Trainer.lost()

    def fight(self, move, target, context):
        self.Trainer.fight(move, target, context)
