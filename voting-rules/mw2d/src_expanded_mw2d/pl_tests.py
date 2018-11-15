#!/usr/bin/env python
import sys

sys.path.insert(0, './PrefLib-Tools/preflibtools')
# sys.path.insert(0, './PrefLib-Tools/preflibtools/preflibtools')
import preflibtools.generate_profiles as genpr
import preflibtools.io as io

nvoter = 7
cmap = genpr.gen_cand_map(3)
rmaps, rmapscounts = genpr.gen_impartial_culture_strict(nvoter, cmap)
print rmapscounts
print rmaps

outf = open("test.soc", 'w')
io.write_map(cmap, nvoter, genpr.rankmap_to_voteset(rmaps, rmapscounts), outf)
outf.close()
