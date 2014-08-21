#!/usr/bin/env python

import sys, random
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
	
	def __init__(self, size) :
		self.values = [0] * size
		self.values[0], self.values[-1] = 128, 128
		self.pointers = [0, len(self.values)-1]
		self.loops = []
	
	def __str__(self) :
		s = map(str, self.values)
		p = self.pointers
		if p[0] == p[1] :
			s[p[0]] = "\033[93m" + s[p[0]] + "\033[0m"
		else :
			s[p[0]] = "\033[91m" + s[p[0]] + "\033[0m"
			s[p[1]] = "\033[92m" + s[p[1]] + "\033[0m"
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
		return cpos + 1
	
	def lshift(self, c, cpos) :
		self.pointers[c] -= 1 - 2*c
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


def finished(mem, i, clear = [[False, False]]) :
	
	timeout = i >= 100000
	
	win = [clear[0][t] and mem.values[t*-1] == 0 or mem.pointers[t] not in range(len(mem.values)) for t in (1, 0)]
	better = [abs(mem.values[t*-1]) > abs(mem.values[t-1]) for t in (0, 1)]
	
	clear[0] = [mem.values[t] == 0 for t in (0, -1)]
	
	if all(win) or timeout and not any(better) :
		print "\033[93mDraw\033[0m game."
		return True
	
	elif win[0] or timeout and better[0] :
		print "\033[91mBot1\033[0m won the battle!"
		return True
	
	elif win[1] or timeout and better[1] :
		print "\033[92mBot2\033[0m won the battle!"
		return True
	
	else :
		return False


def main(progs, convert) :
	
	mem = Memory(random.randint(10, 30))
	
	controller = {
		"+": mem.inc, "-": mem.dec,
		">": mem.rshift, "<": mem.lshift,
		"[": mem.loop, "]": mem.endloop,
		".": mem.defer
	}
	
	getCode = lambda c : convertToBF.main(c) if convert else open(c).read()
	codes = [ [char for char in getCode(prog) if char in controller] for prog in progs ]
	
	mem.loops = [Loops( char for char in enumerate(code) if char[1] in "[]" ) for code in codes]
	
	cycle = 0
	pos = [0, 0]
	print mem
	
	while not finished(mem, cycle) :
		
		order = (0, 1)
		instr = [codes[i][pos[i]] if pos[i] < len(codes[i]) else "." for i in order]
		
		if instr[1] in "[]" :
			order = (1, 0)
		for i in order :
			pos[i] = controller[instr[i]](i, pos[i])
		
		print mem
		cycle += 1


if __name__ == "__main__" :
	
	try :
		main(sys.argv[1:3], "-c" in sys.argv) #TODO
	
	except Exception :
		raise SyntaxError("Invalid syntax")


