from animationManager import AnimationManager
from dialogManager import DialogManager
from battleUi import BattleUi
from battleAi import BattleAi
from damageCalcEngine import DamageCalcEngine
from damageCalcEnv import DamageCalcEnv


class BattleEngine:
    def __init__(self, screen, keyboard, cursor, controller, player):
        self.Screen = screen
        self.Cursor = cursor
        self.DialogManager = DialogManager(screen, keyboard, controller)
        self.AnimationManager = AnimationManager()
        self.DamageCalcEngine = None

        self.Player = player
        self.Opponent = None

        self.Ui = None
        self.Ai = None

        self.active_menu = None

        self.switchGameStateQuery = False

        self.logs = []

    def init_battle(self):
        self.active_menu = None
        self.Opponent = self.Player.Opponent
        self.Ui = BattleUi(self.Screen, self.Player, self.Opponent, self.build_battle_context(self.Player))
        self.Ai = BattleAi(self.Player, self.Opponent, self.build_battle_context(self.Opponent))
        self.Player.worldCompo = [pkmn.name for pkmn in self.Player.team]

    def end_battle(self):
        self.Player.get_back_world_comp()
        self.switchGameStateQuery = True

        if self.Opponent.get_trainer():
            if self.Opponent.lost():
                self.Player.npcsEncountered.append(self.Opponent.get_trainer().dbSymbol)
                self.Player.trainersDefeated.append(self.Opponent.get_trainer().dbSymbol)

    def update(self):
        self.Ui.render()
        self.Ui.render_main_menu()
        self.check_inputs()
        # self.start_round()

    def start_round(self):
        if self.Player.battle_choice:
            self.Opponent.battle_choice = self.Ai.select_option()

            prio_order = self.setup_prio()

            for contender in prio_order:
                if contender == self.Player:
                    if not contender.get_active_pkmn().is_ko():
                        if contender.battle_choice[0] == "attack":
                            contender.fight(contender.battle_choice[1],
                                            prio_order[prio_order.index(contender)-1].get_active_pkmn(),
                                            self.build_battle_context(contender))
                        elif contender.battle_choice[0] == "switch":
                            contender.switch(contender.battle_choice[1])
                    elif contender.get_active_pkmn().is_ko():
                        pass

            self.global_events_update()

            self.Player.battle_choice = None

    def setup_prio(self):
        return [self.Opponent, self.Player]

    def global_events_update(self):
        pass

    def check_inputs(self):
        if self.active_menu == "battle":
            self.Ui.render_battle_menu()
            for i in range(len(self.Player.get_active_pkmn().moveset)):
                if self.Ui.interactive_rect["move" + str(i)].collidepoint(self.Cursor.position):
                    self.Ui.render_move_info(self.Player.get_active_pkmn().moveset[i], 0, 0)
                    if self.Cursor.left_click:
                        self.Player.battle_choice = ("attack", self.Player.get_active_pkmn().moveset[i])

                        self.DamageCalcEngine = DamageCalcEngine(
                            DamageCalcEnv(
                                self.Player.get_active_pkmn(),
                                self.Opponent.get_active_pkmn(),
                                self.Player.battle_choice[1],
                                None))
                        self.DamageCalcEngine.collect_methods()

                        self.DamageCalcEngine.calcul_damage()

        elif self.active_menu == "team":
            self.Ui.render_team_menu()
            for i in range(len(self.Player.team)):
                if i:
                    if self.Ui.interactive_rect["pkmn" + str(i)].collidepoint(self.Cursor.position):
                        if self.Cursor.left_click:
                            self.Player.battle_choice = ("switch", self.Player.team[i])

        elif self.active_menu == "bag":
            pass

        elif self.active_menu == "run":
            self.end_battle()

        self.update_menu()

    def update_menu(self):
        if self.Cursor.left_click:
            if self.Ui.interactive_rect["battle"].collidepoint(self.Cursor.position):
                self.active_menu = "battle"
            elif self.Ui.interactive_rect["team"].collidepoint(self.Cursor.position):
                if len(self.Player.team) > 1:
                    self.active_menu = "team"
            elif self.Ui.interactive_rect["bag"].collidepoint(self.Cursor.position):
                self.active_menu = "bag"
            elif self.Ui.interactive_rect["run"].collidepoint(self.Cursor.position):
                self.active_menu = "run"
            elif self.Cursor.left_click:
                self.active_menu = None

    def build_battle_context(self, user):
        return {}
