from damageCalcEngine import DamageCalcEngine


class BattleEngine:
    def __init__(self, battle_data):
        self.battleData = battle_data
        self.DamageCalcEngine = DamageCalcEngine()

        self.active_menu = None

        self.switchGameStateQuery = False

    def set_priority_ranking(self):
        return [self.battleData.get_player(), self.battleData.get_opponent()]

    def calcul_damage(self, ignore_crit=False, const_r=False):
        self.DamageCalcEngine.calcul_damage(ignore_crit=ignore_crit, const_r=const_r)
