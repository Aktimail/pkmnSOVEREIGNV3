class Cursor:
    def __init__(self):
        self.position = (0, 0)
        self.left_click = False
        self.right_click = False

    def left_click_down(self):
        self.left_click = True

    def left_click_up(self):
        self.left_click = False

    def right_click_down(self):
        self.left_click = True

    def right_click_up(self):
        self.left_click = False

    def update_position(self, position):
        self.position = position

    def reset(self):
        self.position = (0, 0)
        self.left_click = False
        self.right_click = False
