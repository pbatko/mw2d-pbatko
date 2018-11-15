#!/usr/bin/env python
from rule_proportional_new import STV, STV2, GreedyCC, GreedyCC2, GreedyM, GreedyM2
from rule_proportional_new import AlgoP, AlgoP2, RangingCC, RangingCC2
from rule_proportional_new import CCILP, CCILP2, PAV, PAV2, PAVtopk, PAVtopk2, MonroeILP, MonroeILP2
from rule_weakly_separable_new import SNTV, SNTV2, Bloc, Bloc2, KBorda, KBorda2, TApproval, TApproval2
from preference import OrdinalPreference
from profile import Profile
import winner_new as winner
import plib2mw2d
import sys

pr = Profile(3)
preferences = [OrdinalPreference(1, [0, 1, 2]), OrdinalPreference(1, [0, 1, 2])]
pr.add_preferences(preferences)

pr2 = Profile(5)
preferences2 = [
    OrdinalPreference(1, [0, 2, 1, 3, 4])
    , OrdinalPreference(1, [0, 1, 2, 4, 3])
    , OrdinalPreference(1, [0, 1, 2, 4, 3])
    , OrdinalPreference(1, [4, 3, 2, 1, 0])
    , OrdinalPreference(1, [4, 2, 0, 1, 3])
]
pr2.add_preferences(preferences2)


def run_test(profile, k):
    r = STV()
    print r(profile.raw_voters(), k)
    r2 = STV2()
    print r2(profile, k)

    gcc = GreedyCC()
    print gcc(profile.raw_voters(), k)
    gcc2 = GreedyCC2()
    print gcc2(profile, k)

    gm = GreedyM()
    print gm(profile.raw_voters(), k)
    gm2 = GreedyM2()
    print gm2(profile, k)

    ap = AlgoP()
    print ap(profile.raw_voters(), k)
    ap2 = AlgoP2()
    print ap2(profile, k)

    apr = RangingCC()
    print apr(profile.raw_voters(), k)
    apr2 = RangingCC2()
    print apr2(profile, k)

    ilpCC = CCILP()
    print ilpCC(profile.raw_voters(), k)
    ilpCC2 = CCILP2()
    print ilpCC2(profile, k)

    pav = PAV()
    print pav(profile.raw_voters(), k)
    pav2 = PAV2()
    print pav2(profile, k)

    pavtopk = PAVtopk()
    print pavtopk(profile.raw_voters(), k)
    pavtopk2 = PAVtopk2()
    print pavtopk2(profile, k)

    mILP = MonroeILP()
    print mILP(profile.raw_voters(), k)
    mILP2 = MonroeILP2()
    print mILP2(profile, k)

    kb = KBorda()
    print kb(profile.raw_voters(), k)
    kb2 = KBorda2()
    print kb2(profile, k)

    bloc = Bloc()
    print bloc(profile.raw_voters(), k)
    bloc2 = Bloc2()
    print bloc2(profile, k)

    sntv = SNTV()
    print sntv(profile.raw_voters(), k)
    sntv2 = SNTV2()
    print sntv2(profile, k)

    tapp = TApproval(3)
    print tapp(profile.raw_voters(), k)
    tapp2 = TApproval2(3)
    print tapp2(profile, k)


if __name__ == '__main__':
    k = int(sys.argv[1])
    V = None
    cand_num = 0
    if len(sys.argv) > 2:
        tmp_pref_filename = 'pref.out.tmp'
        plib2mw2d.convert_preferences(sys.argv[2], tmp_pref_filename)
        tmp_pref_file = open(tmp_pref_filename, 'r')
        cand_num, n, C, V = winner.readData(tmp_pref_file, k)
        tmp_pref_file.close()
    preferences = pr2
    if V:
        ordinal_prefs = [OrdinalPreference(1, vote) for vote in V]
        print V
        preferences = Profile(cand_num)
        preferences.add_preferences(ordinal_prefs)
    run_test(preferences, k)
