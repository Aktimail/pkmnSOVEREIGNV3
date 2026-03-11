import csv
import pygame

from settings import SETTINGS


class Dialog:
    def __init__(self, player, src, speaker=None):
        self.Player = player
        self.src = src
        self.speaker = speaker

        self.txt_size = 32
        self.txt_color = (0, 0, 0)
        self.txt_gap = 50
        self.txt_spd = SETTINGS.TEXT_SPEED
        self.line_width = SETTINGS.DISPLAY_SIZE[0] - 280
        self.font = pygame.font.Font("../assets/dialogs/PKMN RBYGSC.ttf", self.txt_size)

        self.text = None

        self.txt_idx = 0
        self.txt_progression = 0
        self.line_idx = 0

        self.dialogOutput = self.check_output()

        self.writing = True

    def load_dialog(self):
        with open("../assets/dialogs/dialogs.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == self.src:
                    if self.check_condition(row[4]):
                        self.text = row[SETTINGS.LANGUAGE+1]

    def parse_tokens(self):
        if "<playerName>" in self.text:
            self.text = self.text.replace("<playername>", self.Player.name)
        if "<playerLead>" in self.text:
            self.text = self.text.replace("<playerLead>", self.Player.get_active_pkmn().name)

        if self.speaker:
            if "<speakerName>" in self.text:
                self.text = self.text.replace("<speakerName>", self.speaker.name)
            if "<speakerLead>" in self.text:
                self.text = self.text.replace("<speakerLead>", self.speaker.get_active_pkmn().name)
            if "<pkmnName>" in self.text:
                self.text = self.text.replace("<pkmnName>", self.speaker.name)
            if "<itemName>" in self.text:
                self.text = self.text.replace("<itemName>", self.speaker.dbSymbol)


    def format_text(self):
        space_width = self.font.render(" ", True, self.txt_color).get_width()
        form_txt = []
        self.text = self.text.split("<break>")
        for line in self.text:
            form_line = []
            line = line.split(" ")
            concat_txt = ""
            txt_width = 0
            for idx, word in enumerate(line):
                word_width = self.font.render(word, True, self.txt_color).get_width()
                txt_width += word_width
                if txt_width <= self.line_width:
                    concat_txt += word + " "
                    txt_width += space_width
                elif txt_width > self.line_width:
                    form_line.append(concat_txt)
                    concat_txt = word + " "
                    txt_width = word_width + space_width
                if idx == len(line) - 1:
                    form_line.append(concat_txt)
            form_txt.append(form_line)
        self.text = form_txt

    def next_text(self):
        if self.text:
            if self.txt_progression >= len(self.text[self.txt_idx][self.line_idx]):
                if self.line_idx < len(self.text[self.txt_idx]) - 1:
                    self.txt_progression = 0
                    self.line_idx += 1
                else:
                    self.line_idx = 0
                    self.txt_progression = 0
                    self.txt_idx += 1
                    if self.txt_idx >= len(self.text):
                        self.txt_idx = 0
                        return False
                    self.writing = True
            return True

    def check_condition(self, condition):
        if not condition:
            return True
        elif condition == "defeated":
            if self.src in self.Player.trainersDefeated:
                return True
        elif condition == "second":
            if self.src in self.Player.npcsEncountered:
                return True
        return False

    def check_output(self):
        return self.src
