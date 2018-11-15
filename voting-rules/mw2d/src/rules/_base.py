import operator
import random as stdrandom


# profiling:
# import cProfile
#
# def seqVarPhragmen(V, k):
#     # cProfile.run('seqVarPhragmen2(V, k)')
#     # seqMaxPhragmen(V, k)
#     # cProfile.runctx('seqMaxPhragmen(V, k)', globals=globals(), locals=locals())
#     cProfile.runctx('seqVarPhragmen2(V, k)', globals=globals(), locals=locals())

# import rules.ordinal

class RandomUtils:

    def chooseOne(self, list):
        # type: (list) -> object
        idx = stdrandom.randint(0, len(list) - 1)
        return list[idx]

    def keyOfMaxFromDict(self, dictionary, max_key):
        iteritems = dictionary.items()
        stdrandom.shuffle(iteritems)
        return max(iteritems, key=max_key)[0]

    def keyOfMaxValueFromDict(self, dictionary):
        iteritems = dictionary.items()
        stdrandom.shuffle(iteritems)
        return max(iteritems, key=operator.itemgetter(1))[0]

    def keyOfMinValueFromDict(self, dictionary):
        iteritems = dictionary.items()
        stdrandom.shuffle(iteritems)
        return min(iteritems, key=operator.itemgetter(1))[0]

    def random(self):
        return stdrandom.random()

    def randint(self, a, b):
        return stdrandom.randint(a, b)

    def shuffle(self, c):
        return stdrandom.shuffle(c)

    pass


class RandomUtils_Const(RandomUtils):

    def chooseOne(self, list):
        # type: (list) -> object
        return list[0]

    pass


############################################################################################



class ApprovalBasedRules:

    __rule_classes = []

    @classmethod
    def add(cls, rule_class):
        if not rule_class.excluded:
            cls.__rule_classes.append(rule_class)

    @classmethod
    def getList(cls):
        # type: () -> list[ApprovalBasedRuleBase]
        return list(cls.__rule_classes)

    @classmethod
    def getByNames(clazz, names):
        rules_list = clazz.getList()

        def getRuleByShortName(name):
            gen = (rule for rule in rules_list if rule.getShortName() == name)
            ruleOpt = next(gen, None)
            if ruleOpt is None:
                raise Exception("Could not find rule: '{0}'".format(name))
            return ruleOpt

        rules = [getRuleByShortName(name) for name in names]
        return rules



class ApprovalBasedRuleBase:
    """ Base class for all approval-based rules

        Features and purposes:
        * automatically register each subclass as new voting rule
        * define a common API for all approval-based rules
    """

    excluded = False

    randomUtils = RandomUtils()

    @classmethod
    def apply(clazz, V, number_of_candidates, k):
        # type: (list[list[int]], int, int) -> list[int]
        raise NotImplementedError()

    @classmethod
    def getName(cls):
        return cls.__name__

    @classmethod
    def getShortName(cls):
        long_name = cls.__name__
        idx = long_name.rfind(".")
        return long_name[idx + 1:]

    pass


############################################################################################