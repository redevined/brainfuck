brainfuck
=========

A Brainfuck interpreter, written in Python.

Brainfuck is an esoteric programming language with an extremely minimalistic syntax. It is considered Turing complete.
You can find a deeper explanation along with several examples on [Wikipedia](http://en.wikipedia.org/wiki/Brainfuck "Brainfuck on Wikipedia").

__Important note on implementation:__ This implementation supports arbitrary high cell values and a dynamically growing memory tape. Therefore there's no wrapping for cells or the tape!

Usage
-----

`python ./brainfuck.py [-h] [-c CODE|-f FILE] [-i INPUT] [--debug CHAR]`

* `-h`      Display a help message and exits.  
* `-c`      Pass your code as a command-line argument.
* `-f`      The programm takes the code from an external file with text-based format.
* `-i`      Define the input for your program.
* `--debug` If enabled, a '#' in your brainfuck code will pause to running programm and display useful debugging information. You can change the token by additionaly providing a single character.


Python has to be installed in order to use it. To do so (Ubuntu):  
> `sudo apt-get install python`

Creating a useful alias:  
> `echo "alias brainfuck='python ~/replace/with/your/directory/brainfuck.py '" >> ~/.bash_aliases`

With this one you can use:  
> `brainfuck [-h] [-c CODE|-f FILE] [--debug]`


Feel free to modify this code, report bugs, give advices to enhance it or ask questions about the source code (obviously I'm not *that* good at commenting my code).
