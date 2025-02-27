from repository import PanelSetRep



class PanelSetServ:
    def __init__(self):
        self.panel_rep = PanelSetRep()

    def load_all(self):
        return self.panel_rep.load_all()