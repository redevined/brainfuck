#!/usr/bin/env python

import sys, random, argparse
import convertToBF


class Loops(dict) :
	
	def __init__(self, brackets) :
		scope = 0
		for (i, b) in brackets :
			if b == "[" :
				scope += 1
				self[i] = scope
			elif b == "]" :
				ia = self.reverse()[scope]
				self[ia] = i
				scope -= 1
	
	def reverse(self) :
		return dict(zip(self.values(), self.keys()))



class Memory :
	
	def __init__(self, size, no_color) :
		self.values = [0] * size
		self.values[0], self.values[-1] = 128, 128
		self.pointers = [0, size-1]
		self.loops = []
		self.no_color = no_color
	
	def __str__(self) :
		s = map(str, self.values)
		p = self.pointers
		if not self.no_color :
			if p[0] == p[1] :
				s[p[0]] = "\033[93m" + s[p[0]] + "\033[0m"
			else :
				s[p[0]] = "\033[91m" + s[p[0]] + "\033[0m"
				s[p[1]] = "\033[92m" + s[p[1]] + "\033[0m"
		else :
			s[p[0]] = ">" + s[p[0]]
			s[p[1]] = s[p[1]] + "<"
		return "[ " + " | ".join(s) + " ]"
	
	def inc(self, c, cpos) :
		self.values[self.pointers[c]] += 1
		if self.values[self.pointers[c]] > 128 :
			self.values[self.pointers[c]] = -127
		elif self.values[self.pointers[c]] < -127 :
			self.values[self.pointers[c]] = 128
		return cpos + 1
	
	def dec(self, c, cpos) :
		self.values[self.pointers[c]] -= 1
		if self.values[self.pointers[c]] > 128 :
			self.values[self.pointers[c]] = -127
		elif self.values[self.pointers[c]] < -127 :
			self.values[self.pointers[c]] = 128
		return cpos + 1
	
	def rshift(self, c, cpos) :
		self.pointers[c] += 1 - 2*c
		if self.pointers[c] >= len(self.values) :
			self.pointers[c] = -len(self.values)
		return cpos + 1
	
	def lshift(self, c, cpos) :
		self.pointers[c] -= 1 - 2*c
		if self.pointers[c] >= len(self.values) :
			self.pointers[c] = -len(self.values)
		return cpos + 1
	
	def loop(self, c, cpos) :
		if self.values[self.pointers[c]] == 0 :
			return self.loops[c][cpos] + 1
		else :
			return cpos + 1
	
	def endloop(self, c, cpos) :
		if self.values[self.pointers[c]] == 0 :
			return cpos + 1
		else :
			return self.loops[c].reverse()[cpos] + 1
	
	def defer(self, c, cpos) :
		return cpos + 1



def parseArguments() :
	
	parser = argparse.ArgumentParser(description = "Arena program for the BrainFuckedBotsForBattling contest")

	parser.add_argument("programs",
		help = "The names of the two competing programs",
		nargs = 2)
	parser.add_argument("-c", "--convert",
		help = "Convert advanced syntax Bf-programs to regular Brainfuck",
		action = "store_true")
	parser.add_argument("-m", "--memory-size",
		help = "Select the size of the memory tape, defaults to random number in [10, 30]",
		type = int,
		default = random.randint(10, 30))
	parser.add_argument("-t", "--timeout",
		help = "The number of cycles to complete before the game is considered a draw",
		type = int,
		default = 10000)
	parser.add_argument("--no-color",
		help = "Disable colored output",
		action = "store_true")

	args = parser.parse_args()
	
	return vars(args)



def finished(mem, c, clear = [[False, False]]) :
	
	timeout = c >= args["timeout"]
	
	win = [clear[0][t] and mem.values[t*-1] == 0 or mem.pointers[t] not in range(len(mem.values)) for t in (1, 0)]
	better = [abs(mem.values[t*-1]) > abs(mem.values[t-1]) for t in (0, 1)]
	
	clear[0] = [mem.values[t] == 0 for t in (0, -1)]
	
	if all(win) or timeout and not any(better) :
		if not args["no_color"] :
			print "\n===== \033[93mDraw\033[0m game ====="
		else :
			print "\n===== Draw game ====="
		return True
	
	for i in (0, 1) :
		if win[i] or timeout and better[i] :
			if not args["no_color"] :
				print "\n===== \033[{}m{}\033[0m won the battle after {} cycles =====".format(91+i, args["programs"][i].rsplit("/")[-1].rsplit(".", 1)[0], c)
			else :
				print "\n===== {} won the battle after {} cycles =====".format(args["programs"][i].rsplit("/")[-1].rsplit(".", 1)[0], c)
			return True
	
	return False



def main(params) :
	
	# Initialize the memory tape
	mem = Memory(params["memory_size"], params["no_color"])
	
	# Dictionary for translating Brainfuck code instructions into actions on the memory
	controller = {
		"+": mem.inc, "-": mem.dec,
		">": mem.rshift, "<": mem.lshift,
		"[": mem.loop, "]": mem.endloop,
		".": mem.defer
	}
	
	# Get the code of the programs (and convert extended Brainfuck to Brainfuck if necessary)
	getCode = lambda c : convertToBF.main(c) if params["convert"] else open(c).read()
	codes = [ [char for char in getCode(prog) if char in controller] for prog in params["programs"] ]
	
	# Find matching loops and create dictionary inside the memory instance
	mem.loops = [Loops( char for char in enumerate(code) if char[1] in "[]" ) for code in codes]
	
	print "===== Starting battle of <{1}> vs <{2}> with memory tape size: {0} =====\n".format(params["memory_size"], *[name.rsplit("/")[-1].rsplit(".", 1)[0] for name in params["programs"]])
	
	# Get ready to rumble!
	cycle = 0
	pos = [0, 0]
	print mem
	
	# Loop while none of the finishing conditions is  reached
	while not finished(mem, cycle) :
		
		# Get the next instructions
		order = (0, 1)
		instr = [codes[i][pos[i]] if pos[i] < len(codes[i]) else "." for i in order]
		
		# Revert instructions order if second instruction is a loop (checks for 0s have to be executed before increments/decrements)
		for i in order[::-2*(instr[1] in "[]")+1] :
			
			# Execute action on the tape and calculate new position of the instructions pointer
			pos[i] = controller[instr[i]](i, pos[i])
		
		# Increment cycle counter
		cycle += 1
		print mem



if __name__ == "__main__" :
	
	args = parseArguments()
	
	try :
		main(args)
	
	except Exception :
		raise SyntaxError("Invalid syntax")


