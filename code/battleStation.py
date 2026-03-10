class BattleStation:
    def __init__(self, owner):
        self.owner = owner
        self.side = owner.battleSide
        self.party = owner.battleParty
        self.pkmnSlots = owner.battleSlots
