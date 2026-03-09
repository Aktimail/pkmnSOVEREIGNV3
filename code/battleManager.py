from animationManager import AnimationManager
from dialogManager import DialogManager
from battleEnv import BattleEnv
from battleEngine import BattleEngine
from battleUi import BattleUi
from battleAi import BattleAi


class BattleManager:
    def __init__(self, screen, keyboard, cursor, controller, player):
        self.Screen = screen
        self.Cursor = cursor
        self.DialogManager = DialogManager(screen, keyboard, controller)
        self.AnimationManager = AnimationManager()

        self.Player = player
        self.Opponent = None

        self.Engine = None
        self.Ui = None
        self.Ai = None

        self.activeMenu = None

        self.switchGameStateQuery = False

    def config_battle(self):
        self.Opponent = self.Player.Opponent
        self.Engine = BattleEngine(BattleEnv)
        self.Ui = BattleUi(self.Screen, BattleEnv)
        self.Ai = BattleAi(BattleEnv)
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
        self.check_inputs()

    def check_inputs(self):
        if self.activeMenu == "battle":
            self.Ui.render_battle_menu()
            for i in range(len(self.Player.get_active_pkmn().moveset)):
                if self.Ui.interactive_rect["move" + str(i)].collidepoint(self.Cursor.position):
                    self.Ui.render_move_info(self.Player.get_active_pkmn().moveset[i], 0, 0)
                    if self.Cursor.left_click:
                        self.Player.battle_choice = ("attack", self.Player.get_active_pkmn().moveset[i])

        elif self.activeMenu == "team":
            self.Ui.render_team_menu()
            for i in range(len(self.Player.team)):
                if i:
                    if self.Ui.interactive_rect["pkmn" + str(i)].collidepoint(self.Cursor.position):
                        if self.Cursor.left_click:
                            self.Player.battle_choice = ("switch", self.Player.team[i])

        elif self.activeMenu == "bag":
            pass

        elif self.activeMenu == "run":
            self.end_battle()

        self.update_menu()

    def update_menu(self):
        if self.Cursor.left_click:
            if self.Ui.interactive_rect["battle"].collidepoint(self.Cursor.position):
                self.activeMenu = "battle"
            elif self.Ui.interactive_rect["team"].collidepoint(self.Cursor.position):
                if len(self.Player.team) > 1:
                    self.activeMenu = "team"
            elif self.Ui.interactive_rect["bag"].collidepoint(self.Cursor.position):
                self.activeMenu = "bag"
            elif self.Ui.interactive_rect["run"].collidepoint(self.Cursor.position):
                self.activeMenu = "run"
            else:
                self.activeMenu = None

    def trigger_round(self):
        self.Ai.eval_strategy()
        self.Engine.set_priority_ranking()
