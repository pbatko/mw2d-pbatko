# EJR example

from profile import *
from preference import *
import rule_approval

num_cand = 6
prof = Profile(num_cand)
prof.add_preference(DichotomousPreference([0, 4, 5], num_cand))
prof.add_preference(DichotomousPreference([0], num_cand))
prof.add_preference(DichotomousPreference([1, 4, 5], num_cand))
prof.add_preference(DichotomousPreference([1], num_cand))
prof.add_preference(DichotomousPreference([2, 4, 5], num_cand))
prof.add_preference(DichotomousPreference([2], num_cand))
prof.add_preference(DichotomousPreference([3, 4, 5], num_cand))
prof.add_preference(DichotomousPreference([3], num_cand))
com_size = 4

rule_approval.allrules(prof, com_size)
