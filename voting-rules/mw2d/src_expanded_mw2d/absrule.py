class Rule(object):

    def __call__(self, V, k):
        return self.find_winners(V, k)

    def find_winners(self, V, k):
        raise NotImplementedError()
