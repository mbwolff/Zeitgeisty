#!/usr/bin/env python3
"""
Copyright (c) 2022 Mark Wolff <wolff.mark.b@gmail.com>
Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and
this notice are preserved. This file is offered as-is, without any warranty.
"""

formulas = {
    'equivalencies': [
        ["The real AAA is BBB.", 2],
		["AAA wouldn't be AAA without BBB.", 2],
		["The only AAA is BBB.", 2],
		["AAA is BBB made visible.", 2],
		["AAA is the poor person's BBB.", 2],
		["Little AAAs make big BBBs.", 2],
		["AAA is the shortest path from BBB to CCC.", 3],
		["AAA is the continuation of BBB by other means.", 2],
		["AAA is the father of BBB.", 2],
		["AAA is the mother of BBB.", 2],
		["AAA is the brother of BBB.", 2],
		["AAA is the sister of BBB.", 2],
		["AAA is the beginning of BBB.", 2],
		["AAA is the end of BBB.", 2],
		["AAA is a caricature of BBB.", 2],
		["AAA is an outline of BBB.", 2],
		["AAA is the enemy of BBB.", 2],
		["AAA is the test of BBB.", 2],
		["AAA is the proof of BBB.", 2],
		["AAA is the rule of BBB.", 2],
		["AAA is the recourse of BBB.", 2],
		["AAA is BBB of CCC.", 3],
		["AAA of BBB is CCC of DDD.", 4],
		["AAA of BBB is BBB of AAA.", 2],
		["AAA of BBB is AAA of CCC.", 3],
		["AAA of BBB is BBB of CCC.", 3]
    ],
    'parallelisms': [
		["Far from AAA, far from BBB.", 2],
		["With no AAA there is no BBB.", 2],
		["A time for AAA, a time for BBB.", 2],
		["As goes AAA, so goes BBB.", 2],
		["Those who ignore AAA ignore BBB.", 2],
		["Those who desire AAA desire BBB.", 2],
		["Neither AAA without BBB nor BBB without AAA.", 2]
    ],
    'strong_oppo': [ # these express parallelisms with a strong opposition
		["AAA is easy, BBB is difficult.", 2],
		["AAA is an amateur, BBB is a pro.", 2],
		["AAA is a sickness and BBB is the cure.", 2],
		["AAA is poetry, BBB is prose.", 2],
		["AAA touches the soul and BBB the body.", 2],
		["AAA is on the surface, BBB is at the core.", 2],
		["AAA dies when BBB is born.", 2],
		["AAA adds to our misery while BBB increases our joy.", 2],
		["AAA brings people together, BBB tears them apart.", 2],
		["God sends AAA, the devil sends BBB.", 2],
		["People love AAA and fear BBB.", 2],
		["You can easily do without AAA but not without BBB.", 2],
		["You can hide AAA but not BBB.", 2],
		["Everyone complains about AAA, no one complains about BBB.", 2],
		["You can easily go from AAA to BBB but you will not come back from BBB to AAA.", 2],
		["Hating AAA is nothing but the love of BBB.", 2],
		["People can put up with AAA but not with BBB.", 2],
		["You must not do with AAA what you can do with BBB.", 2]
    ],
    'mild_oppo': [ # these express parallelisms with a mild opposition
		["AAA has only one form, BBB has many.", 2],
		["AAA is given to everyone, BBB only to some.", 2],
		["A bit of AAA leads away from BBB but a lot brings it closer.", 2],
		["AAA is rare, BBB is even rarer.", 2],
		["AAA has no secrets that BBB cannot reveal.", 2],
		["AAA corrects our faults that BBB cannot correct.", 2],
		["When AAA leaves us, BBB is not far away.", 2],
		["AAA is born with BBB but AAA does not always die with BBB.", 2],
		["AAA will save us from BBB but who will save us from AAA?", 2],
		["AAA makes philosophers, BBB makes heroes, CCC makes sages.", 3],
		["AAA and BBB have their limits, CCC is inexhaustible.", 3],
		["AAA sometimes saves what BBB has lost.", 2]
    ],
    'comparisons': [
		["AAA and BBB, same struggle.", 2],
		["AAA makes up for the defect in BBB.", 2],
		["AAA is not in AAA but in BBB.", 2],
		["AAA deceives us more often than BBB.", 2],
		["AAA does not protect us from the stupidity of BBB.", 2],
		["The way to AAA passes through BBB.", 2],
		["AAA is far from BBB.", 2],
		["Nothing pleases AAA more than BBB.", 2],
		["You must not let go of AAA for BBB.", 2],
		["You can't really escape AAA except through BBB.", 2],
		["AAA softens BBB.", 2],
		["AAA will never abolish BBB.", 2],
		["AAA will never get rid of BBB.", 2],
		["What you will find the least of in AAA is BBB.", 2],
		["AAA is to BBB what BBB is to CCC.", 3],
		["AAA is more opposed to BBB than to CCC.", 3],
		["Happiness is in AAA not BBB.", 2],
		["AAA is structured like BBB.", 2],
		["In AAA there is more BBB than CCC.", 3],
		["There is not less of AAA in BBB than of CCC in DDD.", 4]
    ]
}
