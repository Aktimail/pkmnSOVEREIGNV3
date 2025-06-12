import pygame

from screen import Screen
from keyboard import Keyboard
from cursor import Cursor
from controller import Controller

from worldEngine import WorldEngine
from battleEngine import BattleEngine
from player import Player


class Game:
    def __init__(self):
        self.Screen = Screen()

        self.Keyboard = Keyboard()
        self.Cursor = Cursor()
        self.Controller = Controller()

        self.Player = Player(
            self.Screen,
            "Red",
            "hero_01",
            760, 700,
            self.Keyboard,
            self.Controller
        )
        self.WorldEngine = WorldEngine(
            self.Screen,
            self.Keyboard,
            self.Controller,
            self.Player
        )
        self.BattleEngine = BattleEngine(
            self.Screen,
            self.Keyboard,
            self.Cursor,
            self.Controller,
            self.Player
        )

        self.WorldEngine.switch_map("Saint-Rémy")

        self.gameState = self.WorldEngine

        self.running = True

    def run(self):
        while self.running:
            self.check_query()
            self.Screen.update()
            self.gameState.update()
            self.inputs_handler()

    def check_query(self):
        if self.gameState.switch_game_state_query:
            if not self.gameState.DialogManager.reading and not self.gameState.AnimationManager.playing:

                self.gameState.switch_game_state_query = False

                if self.gameState == self.WorldEngine:
                    self.gameState = self.BattleEngine
                    self.gameState.init_battle()

                elif self.gameState == self.BattleEngine:
                    self.gameState = self.WorldEngine

    def inputs_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.Keyboard.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.Keyboard.remove_key(event.key)

            if event.type == pygame.MOUSEMOTION:
                self.Cursor.position = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.Cursor.left_click = True
                elif event.button == 3:
                    self.Cursor.right_click = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.Cursor.left_click = False
                elif event.button == 3:
                    self.Cursor.right_click = False
