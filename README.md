### Goals
Learn some principles of likelihood-based estimation by simulating some data from a hidden 
Markov model and then trying to estimate the parameters governing the simulation.

#### Overview
You will have 4 colored cups (blue, green, orange, and purple) which contain beads.
Most (but probably not *all*) of the beads in each cup will have the same color as the cup.
The data you will generate will be a series of bead colors.
We will use dice and coins as randomization devices.

You will randomly choose an "active" cup to start with.
For each data point you randomly drawing a bead from the active cup, record the bead color, and
    make a random choice about whether or not a new cup will be selected as the "active" cup.




## Set up
#### A. Assign roles to group members
Each group will consist of 4 people:
  1. one person to roll the dice,
  2. one to draw the beads from the cup,
  3. one to record the cup color for each draw, and 
  4. one to record the bead color for each draw
  
#### B. Choose a "contamination" parameter *C*
  1. Flip a coin. 
  2. Record the true value of the contamination parameter, *C*, for your simulation
   as *C=1* if you got a "head" and record *C=2* if you got a "tails".
  
#### C. Choose the bead colors for each cup
Each cup will initially hold 3 beads with a color that matches the cup color.
We are going to bring each cup up to a total of 5 beads, in a way that may "contaminate"
 some of the cups by adding beads of a non-matching color to each cup.
 
  1. If *C=1* for your simulation, add an extra bead of the matching color to each
  cup. 
  1. Roll the 6-sided dice and use the table below to select pairs of colors that
    will be mingled together.
  2. For the "1st pair" of colors you selected, get the pair of cups of the selected
   pair of color and some spare beads of those 2 colors. 
    Perform the following steps *C* times for *each* of the cups:
       1. Flip the coin. 
       1. If the coin shows a "head" add a bead of the same color to that cup
       1. If the coin shows a "tail" add a bead of the non-matching ("paired") color 
       to that cup.
  3. Repeat step 4 for the "2nd pair" of colors.
  

**Table for selecting color pairs**

| Roll    | 1st pair     | 2nd pair      |
|:-------:|:------------:|:-------------:|
| 1 or 2  | Blue+Green   | Orange+Purple |
| 3 or 4  | Blue+Orange  | Green+Purple  |
| 5 or 6  | Blue+Purple  | Green+Orange  |

#### C. Choose a switching rate parameter, *S*
  1. Roll a 6-sided dice
  2. Use the table to figure out your cup switch parameter (**record as your value
  for S**) and  learn the procedure that
    you will use during the simulation to decide whether or not you will randomly
    select a new cup

| Roll    | *S*     | You'll choose a new cup when...|
|:-------:|:------------:|:-------------:|
| 1 or 2  | *S=1/4*   | You roll a "1" on a 4-sided dice |
| 3 or 4  | *S=1/2*  | You get a "Head" on a coin toss  |
| 5 or 6  | *S=3/4*  | You do **not** roll a "1" on a 4-sided dice  |

#### D. Randomly choose an "active" cup
Roll the 4 sided dice and choose the cup color with that number as your
initial "active" cup

### Simulate the data
We'll simulate a data set of XX bead colors, but we'll also keep track 
    of the cup color for each of the XX draws.
We want to see if we can learn the correct values of *S* and *C* from 
    the bead color data.

Repeat the following XX times:

  1. Randomly choose a bead from the "active" cup.
       1. record the bead color,
       2. record the cup color
  2. **Return** the bead to the cup (we are sampling with replacement)
  3. Use the switch procedure from step "Setup C" to decide whether or not to
     attempt a switch. *If (and only if)* the procedure indicates that you should
     try a switch, roll the 4-sided dice and use the result to set the next "active"
     cup. 

