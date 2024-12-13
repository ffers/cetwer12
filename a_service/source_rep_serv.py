from repository import SourAnRep, SourDiffAnRep


class SourRepServ:
    def __init__(self, sour_an_rep: SourAnRep, sour_diff_rep: SourDiffAnRep):
        self.sour_an_rep = sour_an_rep
        self.sour_diff_rep = sour_diff_rep