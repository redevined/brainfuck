#!/usr/bin/env python

import sys, os
import argparse



# --- Classes ---



class Char () :
    
    def __init__ (self, i) :

        self.id = i


class Incrementor (Char) :

    def run (self) :

        global cell
        global pointer

        if cell[pointer] < int(0x110000) :
            cell[pointer] += 1
        else :
            cell[pointer] *= -1

        return self.id


class Decrementor (Char) :

    def run (self) :

        global cell
        global pointer

        if cell[pointer] > -1*int(0x110000) :
            cell[pointer] -= 1
        else :
            cell[pointer] *= -1

        return self.id


class Right (Char) :

    def run (self) :

        global cell
        global pointer

        pointer += 1

        if pointer >= len(cell) :

            cell = cell + [0]

        return self.id


class Left (Char) :

    def run (self) :

        global cell
        global pointer

        pointer -= 1

        if pointer < 0 :

            cell = [0] + cell
            pointer = 0

        return self.id


class Loop (Char) :

    def run (self) :

        global cell
        global pointer
        global loopdir

        try :

            end = loopdir[self.pos][1].id

            if cell[pointer] == 0 :
                return end
            else :
                return self.id

        except IndexError :

            print("--- Invalid use of loops ---")
            sys.exit()


class Endloop (Char) :
    
    def run (self) :

        global cell
        global pointer
        global loopdir

        if cell[pointer] == 0 :
            return self.id
        else :
            return loopdir[self.pos][0].id


class Output (Char) :

    def run (self) :

        global cell
        global pointer
        global output_string

        val = cell[pointer] % int(0x110000)
        
        if val > 31 :
            output_string += chr(val)

        return self.id


class Read (Char) :

    def run (self) :

        global cell
        global pointer
        global input_string
        global input_counter

        if input_counter < len(input_string) :
            cell[pointer] = ord(input_string[input_counter])
            input_counter += 1
        else :
            cell[pointer] = 0

        return self.id


class Debug (Char) :

    def run (self) :

        global cell
        global pointer
        global input_string
        global input_counter
        global output_string
        
        print
        print("--- DEBUG START ---")
        
        print(cell)
        pointstr = " "
        for e in range(pointer) :
            for i in range(len(str(cell[e]))) :
                pointstr += " "
            pointstr += "  "
        pointstr += "^"
        print(pointstr)
        
        if bool(input_string) :
            print("Input: " + input_string)
            print("      " + input_counter * " " + "^")
        
        print("Output: " + output_string)
        print("       " + len(output_string) * " " + "^")
        
        print("---  DEBUG END  ---")
        try :
            raw_input()
        except NameError :
            input()

        return self.id



# --- Functions ---



def scanner (source, debugging) :

    i = 0

    for line in source :

        for char in line :

            if char == "+" :
                i += 1
                yield Incrementor(i)

            elif char == "-" :
                i += 1
                yield Decrementor(i)

            elif char == ">" :
                i += 1
                yield Right(i)

            elif char == "<" :
                i += 1
                yield Left(i)

            elif char == "[" :
                i += 1
                yield Loop(i)

            elif char == "]" :
                i += 1
                yield Endloop(i)

            elif char == "." :
                i += 1
                yield Output(i)

            elif char == "," :
                i += 1
                yield Read(i)

            elif char == "#" and debugging :
                i += 1
                yield Debug(i)


def appender (last) :
        
	global loopdir
        
	try :

		if len(loopdir[last]) != 1 :
			return appender(last-1)
		else :
			return last

	except IndexError :
   
		return None

		

# --- Main Function ---



def main (argdir) :

    global cell
    cell = [0]

    global pointer
    pointer = 0

    global output_string
    output_string = ""

    global input_string
    input_string = argdir["input"]

    global input_counter
    input_counter = 0

    global loopdir
    loopdir = []

    flow = []
    
    if bool(argdir["code"]) :
		
        code = argdir["code"]		
	
    else :
	
        if "/" in argdir["file"] :
		
            code = open(argdir["file"])
            
        else :
		
            code = open(os.path.join(argdir["file"]))
 
    for element in scanner(code, argdir["debug"]) :
        
        if element.__class__.__name__ == "Loop" :

            pos = len(loopdir)

            loopdir.append([element])
            element.pos = pos

        elif element.__class__.__name__ == "Endloop" :

            pos = appender(len(loopdir)-1)

            try :

                loopdir[pos].append(element)
                element.pos = pos

            except TypeError :

                print("--- Invalid use of loops ---")
                sys.exit()

        flow.append(element)

    i = 0

    while i < len(flow) :

        i = flow[i].run()

    print(output_string)



parser = argparse.ArgumentParser(description = "Brainfuck interpreter script")

parser.add_argument("-c", "--code", help = "Define the Brainfuck code directly, you can only use either -c or -f")
parser.add_argument("-f", "--file", help = "Take Brainfuck code from a file, you can only use either -c or -f")
parser.add_argument("-i", "--input", help = "Define the input for your Brainfuck programm", default = "")
parser.add_argument("--debug", help = "If enabled, a '#' in your Brainfuck code will pause the programm and display debug information", action = "store_true")

args = parser.parse_args()

if bool(args.code) ^ bool(args.file) :

	if __name__ == "__main__" :
		main(vars(args))
    	
else :

	parser.error("Please make sure to use only one of the -c or -f flags")
