BrainFuckedBotsForBattling - A Brainfuck Tournament
===================================================

All bots at the battle arena suddenly got brainfucked and no one can explain why. But who cares as long as they are still able to fight - although Brainfuck is the only language they understand anymore.

---

Scoreboard
----------

    |       Owner        |         Bot           Score |
    |--------------------|-----------------------------|
    | Sylwester          | BurlyBalder         -  356  |
    | Comintern          | CounterPunch        -  352  |
    | IstvanChung        | Bigger              -  341  |
    | AndoDaan           | BeatYouMate         -  332  |
    | MikaLammi          | WallE               -  317  |
    | ccarton            | AnybodyThere        -  303  |
    | Sparr              | SeeSawRush          -  302  |
    | kaine              | SternBot            -  289  |
    | PhiNotPi           | EvoBot2             -  288  |
    | PhiNotPi           | RandomOscillator    -  273  |
    | Sylwester          | TerribleThor        -  269  |
    | Nax                | TruthBot            -  267  |
    | DLosc              | LightfootPlodder    -  267  |
    | DLosc              | Plodder             -  265  |
    | PhiNotPi           | EvoBot1             -  263  |
    | MikaLammi          | PolarBear           -  236  |
    | Moop               | Alternator          -  232  |
    | TestBot            | DecoyBot            -  218  |
    | Geobits            | Backtracker         -  208  |
    | TestBot            | FastClearBot        -  202  |
    | Sylwester          | ReluctantRan        -  197  |
    | frederick          | 128Bot              -  195  |
    | IngoBuerk          | Geronimo            -  182  |
    | plannapus          | CleanUpOnAisleSix   -  158  |
    | PhiNotPi           | CloakingDeviceBot   -  157  |
    | flawr              | CropCircleBot       -  154  |
    | kaine              | BestOffense         -  141  |
    | PhiNotPi           | CantTouchThis       -  137  |
    | isaacg             | CleverAndDetermined -  135  |
    | DLosc              | ScaredyBot          -  125  |
    | AndoDaan           | GetOffMate          -  125  |
    | Moop               | StubbornBot         -  122  |
    | IngoBuerk          | Gambler             -  110  |
    | BetaDecay          | RussianRoulette     -  103  |
    | flawr              | DoNothingBot        -  103  |
    | mmphilips          | PacifistBot         -  101  |
    | SebastianLamerichs | Dumbot              -  99   |
    | SeanD              | DontUnderstand      -  76   |
    | Darkgamma          | TheRetard           -  69   |
    | frederick          | Dumberbot           -  62   |
    | proudHaskeller     | PatientBot          -  60   |
    | flawr              | MetaJSRandomBot     -  54   |
    | BetaDecay          | PrussianRoulette    -  28   |
    | frederick          | Dumbestbot          -  0    |

_Scores from 25.08.2014_

__EDIT1__: Fixed a bug in the convert script causing the interpreter to not ignore numbers in commented programs.

__EDIT2__: Since it caused an arcane runtime on my quite slow computer, I reduced the timeout limit from 100000 cycles to 10000 cycles. Not that anyone has turned the resultof a running game beyond this point anyway. If your bot has a strategy which requires a higher limit, please just start complaining ^^

__EDIT3__: Removed comments in bf programs, due to an unexpected result, should be fixed now. If anyone has a problem with removing his comments, please report. I haven't found the time to revise the interpreter for treating abbreviations himself, will do this in future round.

---

Description
-----------

This is a [Brainfuck](http://esolangs.org/wiki/Brainfuck) tournament inspired by [BF Joust](http://esolangs.org/wiki/BF_Joust). Two bots (Brainfuck programs) are fighting each other in an arena which is represented by a memory tape. Each cell can hold values from -127 up to 128 and wrap at their limits (so 128 + 1 = -127).

Valid instructions are similiar to regular Brainfuck, which means:

    + : Increment cell at your pointer's location by 1
    - : Decrement cell at your pointer's location by 1
    > : Move your memory pointer by 1 cell towards the enemy flag
    < : Move your memory pointer by 1 cell away from the enemy flag
    [ : Jump behind the matching ']'-bracket if the cell at your pointer's location equals 0
    ] : Jump behind the matching '['-bracket if the cell at your pointer's location is not 0
    . : Do nothing

The arena has a size of 10 to 30 cells which is pseudorandomly chosen each battle. At both ends is a 'flag' located which has an initial value of 128, while all other cells are zeroed. Your bot's goal is to zero the enemy's flag for 2 consecutive cycles before he zeroes your own flag.

Each bot starts at his own flag, which is cell [0] from his own perspective. The opponent is located on the other side of the tape.

	[ 128 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 128 ]
	   ^											 ^
	my bot										 other bot

Both bots execute their action simultaneously, this is considered one cycle. The game ends after 10000 cycles or as soon as one of the winning conditions is reached. If one of the programs reaches its end, it simply stops doing anthing until the end of the game, but can still win.

---

Winning conditions
------------------

Your bot wins under one of the following conditions:
* Your enemy's flag is zeroed before yours
* Your enemy moves his pointer out of the tape (executes `>` on your flag or `<` on his own)
* Your flag's value is more far away from 0 than the value of your opponent's flag after 10000 cycles

---

Rules
-----

Your post should contain a name for your bot and its code.

* You can use the following abbreviation syntax to make your code more readable:
 * E.g. `(+)*4` is the same as `++++`, this is valid for any instruction (also `[` and `]`)
* Every other character than `+-><[].` is a comment and therefore ignored, except `()*` for abbreviations

Bots which do not follow the rules will excluded from the tournament.

* Only basic Brainfuck is allowed, no other variants which supports procedures or arithmetic operations
* Your bot's source code should not contain unmatched brackets

You may inform yourself about [basic strategies](http://esolangs.org/wiki/BF_Joust_strategies) but do __not__ use another one's code for your own bot.

---

Scoring
-------

A bot's score is determined by the number of wins against all other bots.
An encounter between 2 bots consists of 10 matches with different memory tape lengths, which results in a maximum score of 10 points per encounter.
A draw results in no points for this match.

---

Control program
---------------

You can find the [control program](https://github.com/redevined/brainfuck/tree/master/BrainFuckedBotsForBattling) on github, along with the full logs from the battles.
The leaderboard will be posted here once it is generated.

Feel free to clone the repository and try your bot against the others on your own. Use `python Arena.py yourbot.bf otherbot.bf -c` to run a match. You can modify the conditions with the command-line flags `-m` and `-t`.

---

Example bots
------------

FastClearBot.bf

	(>)*9		Since the tape length is at least 10, the first 9 cells can be easily ignored
	([			Find a non-zero cell
	+++			Increment at first, since it could be a decoy
	[-]			Set the cell to zero
	]>			Move on to the next cell
	)*21		Repeat this 21 times

DecoyBot.bf

	>(+)*10		Set up a large defense in front of your flag
	>(-)*10		Set up another one with different polarity
	(>+>-)*3	Create some small decoys
	(>[-]		Move on and set the next cell to zero
	.			Wait one round, in case it is the enemy's flag
	)*21		Repeat this 21 times

The DecoyBot will win every match with a tape length greater than ten, since the FastClearBot can avoid the small decoys, but not the larger ones. The only situation in which the FastClearBot can win against DecoyBot, is when it is fast enough to reach the enemy's flag before his opponent has built up large decoys.
