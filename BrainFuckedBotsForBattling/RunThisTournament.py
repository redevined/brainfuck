#!/usr/bin/env python

import itertools, os
import Arena


def generateScoreboard(owners, scores) :
	
	bots_len = max(map(len, owners.keys())) - 3
	owners_len = max(map(len, owners.values()))
	
	s = "    | {} | {}   Score |\n".format("Owner".center(owners_len), "Bot".center(bots_len))
	s += "    |-" + "-"*owners_len + "-|-" + "-"*bots_len + "---------|\n"
	
	for score, bot in sorted(zip(scores.values(), scores.keys()))[::-1] :
		s += "    | {} | {} -  {}  |\n".format(owners[bot].ljust(owners_len), bot.rsplit(".", 1)[0].ljust(bots_len), str(score).ljust(3))
	
	return s


def main() :
	
	bots = dict( line.strip("\n").split(" ") for line in open("botlist.txt").readlines() )
	code = { bot: open(os.path.join("bots", bot)).read() + " " for bot in bots }
	scores = { bot: 0 for bot in bots }
	
	for fighters in itertools.combinations(bots, 2) :
		
		cmd = {
			"programs" : [code[f] for f in fighters],
			"names" : [f.rsplit(".", 1)[0] for f in fighters]
		}
		results = [ Arena.tournament(cmd)[:] for _ in range(10) ]
		score = [len([True for r in results if f.rsplit(".", 1)[0] in r[-1]]) for f in fighters]
		
		for fig, sco in zip(fighters, score) :
			scores[fig] += sco
		
		total = "===== {} vs. {} finished with {}:{} =====".format(*list(fighters) + score)
		
		### Uncomment below to generate logs		
#		log = open(os.path.join("logs", "{}_vs_{}.log".format(*[f.rsplit(".", 1)[0] for f in fighters])), "w")
#		for res in results :
#			log.write("\n".join(res) + "\n\n\n")
#		log.write(total)
#		log.close()
		
		print(total)
	
	scoreboard = generateScoreboard(bots, scores)
	open("SCOREBOARD.md", "w").write(scoreboard)


if __name__ == "__main__" :
	
	main()


