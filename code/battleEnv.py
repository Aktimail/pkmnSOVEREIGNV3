class BattleEnv:
    def __init__(self, side):
        self.side = side
        self.records = []
        self.field = []
        self.weather = None
