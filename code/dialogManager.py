from settings import SETTINGS
from dialogUi import DialogUi
from dialog import Dialog


class DialogManager:
    def __init__(self, screen, keyboard, controller):
        self.Screen = screen
        self.keyboard = keyboard
        self.controller = controller

        self.Ui = DialogUi(screen)

        self.Dialog = None
        self.skip = True
        self.timer = 0
        self.skip_time = 800

        self.dialogSource = None

        self.reading = False

    def open_dialog(self, player, src):
        self.Dialog = Dialog(player, src)
        self.Dialog.load_dialog()
        self.Dialog.update_tags()
        self.Dialog.format_text()
        self.dialogSource = src
        self.reading = True

    def close_dialog(self):
        self.Dialog.dialogOutput
        self.reading = False

    def update(self):
        self.Ui.render_box()
        self.Dialog.render_text(self.Screen, 140, 575)
        self.check_inputs()

    def check_auto_skip(self):
        if not self.Dialog.writing:
            self.timer += self.Screen.deltaTime
            if self.timer >= self.skip_time:
                self.timer = 0
                if not self.Dialog.next_text():
                    self.close_dialog()

    def check_inputs(self):
        if self.skip:
            if self.keyboard.key_pressed(self.controller.keybinds["interact"]):
                self.keyboard.remove_key(self.controller.keybinds["interact"])
                if not self.Dialog.next_text():
                    self.close_dialog()
        elif not self.skip:
            self.check_auto_skip()

        self.Dialog.txt_spd = SETTINGS.TEXT_SPEED
        if self.keyboard.key_pressed(self.controller.keybinds["run"]):
            self.Dialog.txt_spd = 1
