#!/usr/bin/env python

from __future__ import print_function
import argparse


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
	
	def __init__(self) :
		self.values = [0]
		self.pointer = 0
	
	def inc(self, cpos) :
		self.values[self.pointer] += 1
		return cpos + 1
	
	def dec(self, cpos) :
		self.values[self.pointer] -= 1
		return cpos + 1
	
	def rshift(self, cpos) :
		self.pointer += 1
		if self.pointer >= len(self.values) :
			self.values.append(0)
		return cpos + 1
	
	def lshift(self, cpos) :
		self.pointer -= 1
		if self.pointer < 0 :
			self.values.insert(0, 0)
			self.pointer = 0
		return cpos + 1
	
	def loop(self, cpos) :
		if self.values[self.pointer] == 0 :
			return self.loops[cpos] + 1
		else :
			return cpos + 1
	
	def endloop(self, cpos) :
		if self.values[self.pointer] == 0 :
			return cpos + 1
		else :
			return self.loops.reverse()[cpos] + 1
	
	def write(self, cpos) :
		s = chr(self.values[self.pointer]) if self.values[self.pointer] in [9, 10, 13] + range(32, 127) else ""
		print(s, end="")
		return cpos + 1
	
	def read(self, cpos) :
		try :
			val = ord(self.inpt.next())
		except StopIteration :
			val = 0
		self.values[self.pointer] = val
		return cpos + 1
	
	def debug(self, cpos) :
		print()
		print(self)
		raw_input("Continue ->\n")
		return cpos + 1
	
	def __str__(self) :
		s = map(str, self.values)
		s[self.pointer] = "\033[92m" + s[self.pointer] + "\033[0m"
		return "[ " + " | ".join(s) + " ]"
			


def parseArguments() :
	
	parser = argparse.ArgumentParser(description = "Brainfuck interpreter, written in Python 2.7")

	parser.add_argument("-f", "--file", help = "Take Brainfuck code from a file, you can only use either -c or -f")
	parser.add_argument("-c", "--code", help = "Define the Brainfuck code directly, you can only use either -c or -f")
	parser.add_argument("-i", "--input", help = "Define the input for your Brainfuck programm", default = "")
	parser.add_argument("--debug", help = "If enabled, a '#' in your Brainfuck code will pause the programm and display debug information", action = "store_true")

	args = vars(parser.parse_args())
	
	if args["file"] :
		args["code"] = open(args["file"]).read()
	del(args["file"])
	
	return args


def main(prog) :
	
	mem = Memory()
	
	controller = {
		"+": mem.inc, "-": mem.dec,
		">": mem.rshift, "<": mem.lshift,
		"[": mem.loop, "]": mem.endloop,
		".": mem.write, ",": mem.read
	}
	if prog["debug"] :
		controller["#"] = mem.debug
	
	code = [char for char in prog["code"] if char in controller]
	
	mem.loops = Loops( char for char in enumerate(code) if char[1] in "[]" )
	mem.inpt = (char for char in prog["input"])
	
	pos = 0
	
	while pos < len(code) :
		
		pos = controller[code[pos]](pos)
	
	print()


if __name__ == "__main__" :
	args = parseArguments()
	try :
		main(args)
	except Exception :
		raise SyntaxError("Invalid syntax")


