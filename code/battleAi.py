import random


class BattleAi:
    def __init__(self, player, opponent, battle_data):
        self.Opponent = opponent
        self.Player = player
        self.battleData = battle_data

    def select_option(self):
        if self.consider_switch():
            self.select_pokemon()
        elif self.consider_object():
            self.select_object()
        else:
            return "attack", random.choice(self.select_move())

    def consider_switch(self):
        pass

    def consider_object(self):
        pass

    def select_move(self):
        potential_move = []
        for move in self.Opponent.get_active_pkmn().moveset:
            f = 1
            for t in self.Player.get_active_pkmn().type:
                f *= move.type.factors[t.name]
            if f >= 2:
                potential_move.append(move)
        if not potential_move:
            return self.Opponent.get_active_pkmn().moveset
        return potential_move

    def select_pokemon(self):
        pass

    def select_object(self):
        pass
