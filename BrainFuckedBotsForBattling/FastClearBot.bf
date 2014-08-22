(>)*9		Since the tape length is at least 10, the first 9 cells can be easily ignored
([			Find a non-zero cell
+++			Increment at first, since it could be a decoy
[-]			Set the cell to zero
]>			Move on to the next cell
)*21		Repeat this 21 times
