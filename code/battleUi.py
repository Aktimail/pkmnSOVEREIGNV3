import pygame


class BattleUi:
    def __init__(self, screen, player, opponent, battle_data):
        self.screen = screen
        self.Player = player
        self.Opponent = opponent
        self.battleData = battle_data

        self.font = pygame.font.Font("../assets/dialogs/PKMN RBYGSC.ttf", 15)

        self.background = pygame.transform.scale(
            pygame.image.load("../assets/graphics/battle/back_grass.png"), self.screen.get_size())

        self.player_hud = {}
        self.opp_hud = {}

        self.player_assets = {}
        self.opp_assets = {}

        self.main_menu_assets = {
            "battle": {
                "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 240)
            },
            "team": {
                "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 320)
            },
            "bag": {
                "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 400)
            },
            "run": {
                "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
                "size": (80, 80),
                "pos": (1200, 480)
            }
        }

        self.battle_asset = {
            "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
            "size": (190, 80),
            "pos": (1005, 240)
        }

        self.team_asset = {
            "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
            "size": (120, 80),
            "pos": (950, 320)
        }

        self.interactive_rect = {}

    def update_player_assets(self):
        self.player_assets = {
            "ground": {
                "image": pygame.image.load("../assets/graphics/battle/player_ground.png"),
                "size": (1024, 128),
                "pos": (-50, 442)
            },
            "pokemon": {
                "image": pygame.image.load(self.Player.get_active_pkmn().sprites["back"]),
                "size": (576, 576),
                "pos": (150, self.Player.get_active_pkmn().frontOffsetY * 7 + 49)
            }
        }

    def update_opp_assets(self):
        self.opp_assets = {
            "ground": {
                "image": pygame.image.load("../assets/graphics/battle/opponent_ground.png"),
                "size": (450, 200),
                "pos": (700, 225)
            },
            "pokemon": {
                "image": pygame.image.load(self.Opponent.get_active_pkmn().sprites["front"]),
                "size": (288, 288),
                "pos": (775, self.Opponent.get_active_pkmn().frontOffsetY * 3 + 50)
            }
        }

    def update_player_hud(self):
        self.player_hud = {
            "battlebar": {
                "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
                "size": (275, 80),
                "pos": (0, 480)
            },
            "pkmn_name": {
                "image": self.font.render(self.Player.get_active_pkmn().name, True, (0, 0, 0)),
                "size": None,
                "pos": (0, 480)
            },
            "pkmn_lvl": {
                "image": self.font.render("lvl " + str(self.Player.get_active_pkmn().level), True, (0, 0, 0)),
                "size": None,
                "pos": (195, 480)
            },
            "hp_bar": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "hp": {
                "image": self.get_hp_color(self.Player.get_active_pkmn()),
                "size": (int(self.Player.get_active_pkmn().currentHp /
                             self.Player.get_active_pkmn().globalStats["hp"] * 276), 12),
                "pos": (0, 0)
            },
            "pokeballs": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            }
        }

    def update_opp_hud(self):
        self.opp_hud = {
            "battlebar": {
                "image": pygame.image.load("../assets/graphics/battle/battlebar.png"),
                "size": (275, 60),
                "pos": (1005, 5)
            },
            "pkmn_name": {
                "image": self.font.render(self.Opponent.get_active_pkmn().name, True, (0, 0, 0)),
                "size": None,
                "pos": (1005, 5)
            },
            "pkmn_lvl": {
                "image": self.font.render("lvl " + str(self.Opponent.get_active_pkmn().level), True, (0, 0, 0)),
                "size": None,
                "pos": (1200, 5)
            },
            "hp_bar": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            },
            "hp": {
                "image": self.get_hp_color(self.Opponent.get_active_pkmn()),
                "size": (int(self.Opponent.get_active_pkmn().currentHp /
                             self.Opponent.get_active_pkmn().globalStats["hp"] * 276), 12),
                "pos": (0, 30)
            },
            "pokeballs": {
                "image": None,
                "size": (0, 0),
                "pos": (0, 0)
            }
        }

    def render(self):
        self.interactive_rect.clear()
        self.render_stage()
        self.render_hud()

    def render_hud(self):
        self.update_player_hud()
        self.update_opp_hud()
        for asset in self.player_hud.values():
            if asset["image"]:
                image = asset["image"]
                if asset["size"]:
                    image = pygame.transform.scale(image, asset["size"])
                self.screen.display.blit(image, asset["pos"])
        for asset in self.opp_hud.values():
            if asset["image"]:
                image = asset["image"]
                if asset["size"]:
                    image = pygame.transform.scale(image, asset["size"])
                self.screen.display.blit(image, asset["pos"])

    def render_stage(self):
        self.screen.display.blit(self.background, (0, 0))
        self.update_player_assets()
        self.update_opp_assets()
        for asset in self.player_assets.values():
            if asset["image"]:
                image = asset["image"]
                image = pygame.transform.scale(image, asset["size"])
                self.screen.display.blit(image, asset["pos"])
        for asset in self.opp_assets.values():
            if asset["image"]:
                image = asset["image"]
                image = pygame.transform.scale(image, asset["size"])
                self.screen.display.blit(image, asset["pos"])

    def render_main_menu(self):
        for asset in self.main_menu_assets:
            image = self.main_menu_assets[asset]["image"]
            image = pygame.transform.scale(image, self.main_menu_assets[asset]["size"])
            self.screen.display.blit(image, self.main_menu_assets[asset]["pos"])
            self.interactive_rect[asset] = pygame.Rect(self.main_menu_assets[asset]["pos"][0],
                                                       self.main_menu_assets[asset]["pos"][1],
                                                       self.main_menu_assets[asset]["size"][0],
                                                       self.main_menu_assets[asset]["size"][1])

    def render_battle_menu(self):
        for i in range(len(self.Player.get_active_pkmn().moveset)):
            image = self.battle_asset["image"]
            image = pygame.transform.scale(image, self.battle_asset["size"])
            asset_pos = (self.battle_asset["pos"][0], self.battle_asset["pos"][1] + i * 80)
            self.screen.display.blit(image, asset_pos)

            move_name = self.font.render(self.Player.get_active_pkmn().moveset[i].name, True, (0, 0, 0))
            move_type = self.font.render(self.Player.get_active_pkmn().moveset[i].type.name, True, (0, 0, 0))
            move_pp = self.font.render(
                str(self.Player.get_active_pkmn().moveset[i].pp) + " / " + str(self.Player.get_active_pkmn().moveset[i].maxPp),
                True, (0, 0, 0))

            self.screen.display.blit(move_name, (asset_pos[0], asset_pos[1]))
            self.screen.display.blit(move_type, (asset_pos[0], asset_pos[1] + 20))
            self.screen.display.blit(move_pp, (asset_pos[0] + 100, asset_pos[1] + 20))

            self.interactive_rect["move" + str(i)] = pygame.Rect(asset_pos[0],
                                                                 asset_pos[1],
                                                                 self.battle_asset["size"][0],
                                                                 self.battle_asset["size"][1])

    def render_team_menu(self):
        for i in range(len(self.Player.team)):
            x = 125 if i >= 3 or len(self.Player.team) <= 3 else 0
            y = 240 if i >= 3 else 0

            image = self.team_asset["image"]
            image = pygame.transform.scale(image, self.team_asset["size"])
            asset_pos = (self.team_asset["pos"][0] + x, self.team_asset["pos"][1] + i * 80 - y)
            self.screen.display.blit(image, asset_pos)

            pkmn_name = self.font.render(self.Player.team[i].name, True, (0, 0, 0))
            pkmn_hp = self.get_hp_color(self.Player.team[i])
            pkmn_hp = pygame.transform.scale(
                pkmn_hp,
                (int(self.Player.team[i].currentHp / self.Player.team[i].globalStats["hp"] * 100), 7)
            )

            self.screen.display.blit(pkmn_name, (asset_pos[0], asset_pos[1]))
            self.screen.display.blit(pkmn_hp, (asset_pos[0], asset_pos[1] + 20))

            self.interactive_rect["pkmn" + str(i)] = pygame.Rect(asset_pos[0],
                                                                 asset_pos[1],
                                                                 self.team_asset["size"][0],
                                                                 self.team_asset["size"][1])

    def render_pkmn_info(self, pkmn, x, y):
        pass

    def render_move_info(self, move, x, y):
        move_name = self.font.render(move.name, True, (0, 0, 0))
        move_pp = self.font.render(str(move.pp) + "/" + str(move.maxPp), True, (0, 0, 0))
        move_type = self.font.render(move.type.name, True, (0, 0, 0))
        move_category = self.font.render(move.category, True, (0, 0, 0))

        self.screen.display.blit(move_name, (x, y))
        self.screen.display.blit(move_type, (x, y + 30))
        self.screen.display.blit(move_pp, (x + 200, y))
        self.screen.display.blit(move_category, (x + 200, y + 30))

    def get_hp_color(self, pkmn):
        hp_bars = pygame.image.load("../assets/graphics/battle/hp.png")
        hp_bars = self.split_hp_bars(hp_bars)
        if pkmn.currentHp == pkmn.globalStats["hp"]:
            active_bar = hp_bars[-1]
        else:
            active_bar = hp_bars[int((pkmn.currentHp / pkmn.globalStats["hp"]) * 6)]
        return active_bar

    @staticmethod
    def split_hp_bars(image):
        all_images = []
        height = image.get_height() // 6
        for i in range(6):
            all_images.append(image.subsurface(pygame.Rect(0, i * height, image.get_width(), height)))
        return all_images
