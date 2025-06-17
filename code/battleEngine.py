from animationManager import AnimationManager
from dialogManager import DialogManager
from battleUi import BattleUi
from battleAi import BattleAi


class BattleEngine:
    def __init__(self, screen, keyboard, cursor, controller, player):
        self.Screen = screen
        self.Cursor = cursor
        self.DialogManager = DialogManager(screen, keyboard, controller)
        self.AnimationManager = AnimationManager()

        self.Player = player
        self.Opponent = None

        self.Ui = None
        self.Ai = None

        self.active_menu = None

        self.switch_game_state_query = False

    def init_battle(self):
        self.active_menu = None
        self.Opponent = self.Player.Opponent
        self.Ui = BattleUi(self.Screen, self.get_battle_data())
        self.Ai = BattleAi(self.get_battle_data())
        self.Player.worldCompo = [pkmn.name for pkmn in self.Player.team]

    def end_battle(self):
        if self.Opponent.lost():
            self.Player.npcs_encountered.append(self.Opponent.dbSymbol)
            self.Player.trainers_defeated.append(self.Opponent.dbSymbol)
        self.Player.get_back_world_comp()
        self.switch_game_state_query = True

    def update(self):
        self.Ui.render()
        self.Ui.render_main_menu()
        self.check_inputs()

    def init_round(self):
        pass

    def check_priority(self):
        return [self.Player, self.Opponent]

    def global_effects_update(self):
        pass

    def check_inputs(self):
        if self.active_menu == "battle":
            self.Ui.render_battle_menu()
            for i in range(len(self.Player.get_lead().moveset)):
                if self.Ui.interactive_rect["move" + str(i)].collidepoint(self.Cursor.position):
                    self.Ui.render_move_info(self.Player.get_lead().moveset[i], 0, 0)
                    if self.Cursor.left_click:
                        self.Player.fight(self.Player.get_lead().moveset[i], self.get_battle_data())

        elif self.active_menu == "team":
            self.Ui.render_team_menu()
            for i in range(len(self.Player.team)):
                if i:
                    if self.Ui.interactive_rect["pkmn" + str(i)].collidepoint(self.Cursor.position):
                        if self.Cursor.left_click:
                            self.Player.switch(i)

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

    def get_battle_data(self):
        return {
            "player": self.Player,
            "opponent": self.Opponent
        }
