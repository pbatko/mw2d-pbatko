

class ElectionResult:

    def __init__(self, election_instance, committee, rule_class):
        # type: (ElectionInstance, list[int], rules.rule_approval.ApprovalBasedRuleBase) -> None

        # fundamental data
        self.rule_class = rule_class
        self.election_instance = election_instance
        self.committee = committee

        # secondary data
        self.committee_size = len(self.committee)

        self.candidates_2d = self.election_instance.C
        self.voters_2d = self.election_instance.V
        self.committee_2d = [self.candidates_2d[_c] for _c in committee]

        self.number_of_candidates = len(self.candidates_2d)
        self.number_of_voters = len(self.voters_2d)

        self.voter_preferences = election_instance.P

        pass

    pass