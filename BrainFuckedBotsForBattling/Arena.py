#!/usr/bin/env python

from __future__ import print_function
import re, random, argparse


class Memory(object) :
	
	def __init__(self, size, no_color) :
		self.values = [0] * size
		self.values[0], self.values[-1] = 128, 128
		self.pointers = [0, size-1]
		self.loops = []
		self.no_color = no_color
	
	def __str__(self) :
		s = list(map(str, self.values))
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
			return self.loops[c][1][cpos] + 1
		else :
			return cpos + 1
	
	def endloop(self, c, cpos) :
		if self.values[self.pointers[c]] == 0 :
			return cpos + 1
		else :
			return self.loops[c][0][cpos] + 1
	
	def defer(self, c, cpos) :
		return cpos + 1



class Code(object) :
	
	def __init__(self, prog, raw) :
		self.code = [ char for char in (prog if raw else open(prog).read()) if char in "+-><[].()*0123456789" ]
		self.pos = 0
		self.parens = self.matchBraces("(", ")")
		self.counters = {}
	
	def __str__(self) :
		return str().join(self.code)
	
	def __getitem__(self, index) :
		if index < len(self.code) :
			return self.code[index]
		else :
			return "."
	
	def __setitem__(self, index, val) :
		self.code[index] = val
	
	def matchBraces(self, opn, cls) :
		braces = {}
		rbraces = lambda : dict(zip(braces.values(), braces.keys()))
		scope = 0
		for (i, char) in enumerate(self.code) :
			if char == opn :
				scope -= 1
				braces[i] = scope
			elif char == cls :
				ia = rbraces()[scope]
				braces[ia] = i
				scope += 1
		return rbraces(), braces
		
	def get(self, pos) :
		t = self[pos]
		if t == "(" :	
			if not pos in self.counters :
				m = [ it for it in re.compile(r"\)\*(\d+)").finditer(str(self)) if it.start() == self.parens[1][pos] ][0]
				c = int(m.group(1))
				self.counters[pos] = [c, m.end()]
			if self.counters[pos][0] > 0 :
				self.counters[pos][0] -= 1
				return self.get(pos+1)
			else :
				end = self.counters[pos][1]
				del(self.counters[pos])
				return self.get(end)
		elif t == ")" :
			return self.get(self.parens[0][pos])
		else :
			self.pos = pos
			return t



def parseArguments() :
	
	parser = argparse.ArgumentParser(description = "Arena program for the BrainFuckedBotsForBattling contest")

	parser.add_argument("programs",
		help = "BF program files or code (with -r)",
		nargs = 2)
	parser.add_argument("-n", "--names",
		help = "The names of the two competing programs, defaults to file names",
		nargs = 2)
	parser.add_argument("-s", "--memory-size",
		help = "Select the size of the memory tape, defaults to random number in [10, 30]",
		type = int,
		default = random.randint(10, 30))
	parser.add_argument("-t", "--timeout",
		help = "The number of cycles to complete before the game is considered a draw",
		type = int,
		default = 10000)
	parser.add_argument("-r", "--raw",
		help = " Provide programs directly as source code instead of filenames",
		action = "store_true")
	parser.add_argument("--no-color",
		help = "Disable colored output",
		action = "store_true")

	args = parser.parse_args()
	
	if not args.names :
		args.names = [name.rsplit("/")[-1].rsplit(".", 1)[0] for name in args.programs]
	
	return vars(args)



def finished(mem, c, clear = [[False, False]]) :
	
	timeout = c >= args["timeout"]
	
	win = [clear[0][t] and mem.values[t*-1] == 0 or mem.pointers[t] not in range(len(mem.values)) for t in (1, 0)]
	better = [abs(mem.values[t*-1]) > abs(mem.values[t-1]) for t in (0, 1)]
	
	clear[0] = [mem.values[t] == 0 for t in (0, -1)]
	
	if all(win) or timeout and not any(better) :
		if not args["no_color"] :
			print("\n===== \033[93mDraw\033[0m game =====")
		else :
			print("\n===== Draw game =====")
		return True
	
	for i in (0, 1) :
		if win[i] or timeout and better[i] :
			if not args["no_color"] :
				print("\n===== \033[{}m{}\033[0m won the battle after {} cycles =====".format(91+i, args["names"][i], c))
			else :
				print("\n===== {} won the battle after {} cycles =====".format(args["names"][i], c))
			return True
	
	return False



def main(params) :
	
	# Initialize the memory tape
	mem = Memory(params["memory_size"], params["no_color"])
	
	# Interface between code and memory
	controller = {
		"+": mem.inc, "-": mem.dec,
		">": mem.rshift, "<": mem.lshift,
		"[": mem.loop, "]": mem.endloop,
		".": mem.defer
	}
	
	# Get the code of the programs (and convert extended Brainfuck to Brainfuck if necessary)
	codes = [ Code(prog, params["raw"]) for prog in params["programs"] ]
	
	# Find matching loops and create dictionaries inside the memory instance
	mem.loops = [code.matchBraces("[", "]") for code in codes]
	
	print("===== Starting battle of <{1}> vs <{2}> with memory tape size: {0} =====\n".format(params["memory_size"], *params["names"]))
	
	# Get ready to rumble!
	cycle = 0
	print(str(mem)) 
	
	# Loop while none of the finishing conditions is  reached
	while not finished(mem, cycle) :
		
		for code in codes :
			code.instr = code.get(code.pos)
			
		for code in codes[::-2*(codes[1].instr in "[]")+1] :
			code.pos = controller[code.instr](codes.index(code), code.pos)
		
		# Increment cycle counter
		cycle += 1
		print(str(mem))



def tournament(data) :
	
	data["memory_size"] = random.randint(10, 30)
	args.update(data)
	
	print.__init__()
	main(args)
	
	return print



if __name__ == "__main__" :
	
	args = parseArguments()
	
	try :
		main(args)
	
	except Exception :
		raise SyntaxError("Invalid syntax")

elif __name__ == "Arena" :
	
	class captureOutput(list) :
	
		def __call__(self, msg) :
			self.append(msg)
	
	args = {
		"timeout" : 10000,
		"raw" : True,
		"no_color" : True
	}
	
	debug = print
	print = captureOutput()


