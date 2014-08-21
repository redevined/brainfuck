#!/usr/bin/env python

import sys, re


def applyDecs(declarations, code) :
	
	def concat(li, c) :
		if re.match(r"\w", c) and re.match(r"\w+", li[-1]) :
			li[-1] += c
			return li
		else :
			return li + [c]
	
	closure_decs = [dec for dec in declarations if re.match(r"\w+=\{.+\}", dec)]
	var_decs = [dec for dec in declarations if re.match(r"\w+=-?\d+", dec)]
	cell_decs = [dec for dec in declarations if re.match(r"\w+=\[\d+\]", dec)]
	cell_vars = dict()
		
	for stmt in closure_decs :
		var, closure = stmt.split("=")
		code = code.replace(var, closure)
	
	for stmt in var_decs :
		var, value = stmt.split("=")
		value = int(value)
		code = code.replace(var, "+"*value if value >= 0 else "-"*abs(value))
	
	for stmt in cell_decs :
		key, value = stmt.split("=")
		cell_vars[key] = int(value[1:-1])

	code = list(code)
	code[0] = [code[0]]
	code = reduce(concat, code)
	
	if cell_vars :
		cell = 0
		
		for var in code :
			
			if var in cell_vars :
				diff = cell_vars[var] - cell
				cell = cell_vars[var]
				
				check = lambda t : ( ">"*diff if diff >= 0 else "<"*abs(diff) ) if t == var else t
				code = [check(c) for c in code]
		
			elif var == ">" :
				cell += 1
		
			elif var == "<" :
				cell -= 1
	
	return str().join(code)


def getPars(code) :
	
	opened = 0
	
	for i in range(len(code)) :
		
		if code[i] == "(" :
			if opened == 0 :
				first = i
			opened += 1
		
		elif code[i] == ")" :
			opened -= 1
			if opened == 0 :
				return first, i


def main(prog) :
	
	code = open(prog).read()
	
	if "//" in code :
		dec, code = code.split("//", 2)
		dec = dec.replace(" ", "").replace(";", "\n").split()
		
		code = applyDecs(dec, code)
	
	code = [char for char in code if char in "+-><[],.#()*0123456789"] + ["EOF"]
	
	while "(" in code :
		pars = getPars(code)
	
		if code[pars[1]+1] == "*" :
			d = pars[1] + 1
			factor = ""
		
			while code[d+1].isdigit() :
				d += 1
				factor += code[d]
		
			del(code[pars[1]:d+1], code[pars[0]])
			code[pars[0]:pars[1]-1] *= int(factor)
		
		else :
			del(code[pars[1]], code[pars[0]])
	
	code = str().join(char for char in code if char in "+-><[],.#")
	
	return code	


if __name__ == "__main__" :
	try :
		print main(sys.argv[1])
	except Exception :
		raise SyntaxError("Invalid syntax")


