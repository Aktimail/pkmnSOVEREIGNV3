from damageCalcEngine import DamageCalcEngine


class BattleEngine:
    def __init__(self, battle_env):
        self.battleEnv = battle_env
        self.DamageCalcEngine = DamageCalcEngine()

        self.active_menu = None

        self.switchGameStateQuery = False

    def set_priority_ranking(self):
        pass

    def process_turn(self, side):
        pass
