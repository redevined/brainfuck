#!/usr/bin/env python

import itertools
from subprocess import check_output as capture


def generateScoreboard(owners, scores) :
	
	bots_len = max(map(len, owner.keys())) - 3
	owners_len = max(map(len, owner.values()))
	
	s = "    +-{}---{}--- Score -+\n".format(" Owner ".center(owners_len, "-"), " Bot ".center(bots_len, "-"))
	
	for score, bot in sorted(zip(scores.values(), scores.keys())) :
		s += "    | {} | {} - {}   |\n".format(owners[bot].center(owners_len), bot.rsplit(".", 1)[0].center(bots_len), score.rjust(3))
	
	s += "    +" + "-"*(bots_len+owners_len+15) + "+\n"
	
	return s


def main() :
	
	bots = dict( line.split(" ") for line in open("botlist.txt").readlines() )
	scores = { key: 0 for key in bots }
	
	for fighters in itertools.combinations(bots, 2) :
		
		cmd = ["python", "Arena.py", "bots/" + fighters[0], "bots/" + fighters[1], "-c", "--no-color"]
		results = [ capture(cmd).split("\n") for i in range(10) ]
		score = [len([True for match in results if fighter.rsplit(".", 1)[0] in match[-2]]) for fighter in fighters]
		
		for fig, sco in zip(fighters, score) :
			scores[fig] += sco
		
		total = "===== {} vs. {} finished with {}:{} =====".format(*list(fighters) + score)
		
		log = open("logs/{}_vs_{}.log".format(*[f.rsplit(".", 1)[0] for f in fighters]), "w")
		for res in results :
			log.write("\n".join(res) + "\n\n\n")
		log.write(total)
		log.close()
		
		print total
	
	scoreboard = generateScoreboard(bots, scores)
	open("SCOREBOARD.md", "w").write(scoreboard)


if __name__ == "__main__" :
	
	main()


