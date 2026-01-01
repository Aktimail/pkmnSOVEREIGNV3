from entity import Entity


class BattleDataBase:
    def __init__(self):
        self.logs = {}
        self.turn = 0
        self.next_turn()

    def compile_player_turn(self, player, **values):
        self.logs[self.turn][player.dbSymbol] = values

    def next_turn(self):
        self.turn += 1
        self.logs[self.turn] = {}

    def get_turn(self):
        return self.turn

    def get_logs(self):
        return self.logs

    def get_player_logs(self, player):
        i = 1
        player_logs = {}
        for turn in self.logs.values():
            if turn[player.dbSymbol]:
                player_logs[i] = turn[player.dbSymbol]
                i += 1
        return player_logs

    def get_turn_logs(self, turn):
        return self.logs[turn]

    def get_actual_turn_logs(self):
        if self.turn in self.logs:
            return self.logs[self.turn]
        return self.logs[self.turn-1]

    def get_last_x_turns_logs(self, x=-1):
        if x == -1:
            x = len(self.logs)
        last_turns_logs = self.logs.copy()
        if self.turn in last_turns_logs:
            del last_turns_logs[self.turn]
        result = {}
        limit = max(0, len(last_turns_logs)-x)
        for i in range(len(last_turns_logs), limit, -1):
            result[i] = last_turns_logs[i]
        return result

    def get_pkmn_logs(self, pkmn, successive):
        result = {}
        for i, turn in self.logs.items():
            for player in turn.values():
                if player["activePkmn"] == pkmn:
                    result[i] = player
        return result

    def get_pkmn_last_move(self, pkmn):
        pass

    def get_active_pkmn_on_field_counter(self, player):
        counter = 1
        actual_pkmn = self.get_actual_turn_logs()[player.dbSymbol]["activePkmn"]
        last_turns_logs = self.get_last_x_turns_logs()
        for turn in last_turns_logs.values():
            if turn[player.dbSymbol]["activePkmn"] == actual_pkmn:
                counter += 1
            else:
                return counter
        return counter

    def get_weather(self):
        pass

    def get_global_field(self):
        pass

    def get_side_effects(self):
        pass

    def is_first_to_move(self, pkmn):
        pass

    def got_hit_this_round(self, pkmn):
        pass

    def move_counter(self, pkmn, move, successive=False, successfull=False):
        pass


BDB = BattleDataBase()
Bob = Entity(None, "bob", 0, 0)
Bob.dbSymbol = "Bob"
Baobab = Entity(None, "baobab", 0, 0)
Baobab.dbSymbol = "Baobab"

BDB.compile_player_turn(Bob, activePkmn="haxorus", action="fight", move="tackle")
BDB.compile_player_turn(Baobab, activePkmn="garchomp", action="switch", switchPkmn="palkia")
BDB.next_turn()
BDB.compile_player_turn(Bob, activePkmn="pikachu", action="fight", move="dragon_claw")
BDB.compile_player_turn(Baobab, activePkmn="palkia", action="switch", switchPkmn="pikachu")
BDB.next_turn()
BDB.compile_player_turn(Bob, activePkmn="haxorus", action="fight", move="raaarr")
BDB.next_turn()
print(BDB.logs)
print(BDB.get_pkmn_logs("haxorus"))

