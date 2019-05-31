### Goals
Learn some principles of likelihood-based estimation by simulating some data from a hidden 
Markov model and then trying to estimate the parameters governing the simulation.

#### Overview
You will have 2 colored cups (1 green and 1 orange) which contain beads.
Initially each cup will have 4 beads that match the cups color.
You will add 4 new beads using a random process described below.
This process may "contaminate" the cups such that the beads are not perfect
  predictors of the cup color.


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
  1. Roll the 4-sided dice. 
  2. Write down the number. This will be the true value of the contamination parameter, *C*.

  
#### C. Choose the bead colors for each cup
Each cup will initially hold 4 beads with a color that matches the cup color.
We are going to bring each cup up to a total of 8 beads, in a way that may "contaminate"
 some of the cups by adding beads of a non-matching color to each cup.
 
  1. Do the following procedure *C* times (where *C* is the number you rolled in part B):
    1. roll the 6-sided dice. If you roll an odd number put an orange bead into the orange cup; 
      if your roll was an even number put a green bead into the orange cup.
    2. Repeat the dice rolling procedure for the green cup.
  2. Bring each cup up to 8 total beads by adding beads that match the cup color to each
    cup. (if your *C=4* you will already have 8 beads in each cup, so you are done).
  


#### C. Choose a switching rate parameter, *S*
  1. Roll a 6-sided dice
  2. Use the table to figure out your cup switch parameter (**record as your value
  for s**) and to learn the procedure that
    you will use during the simulation to decide whether or not you will randomly
    select a new cup

| Roll    | *s*      | You'll choose a new cup when...|
|:-------:|:--------:|:-------------:|
| 1 or 2  | *s=1/4*  | You roll a "1" on a 4-sided dice |
| 3 or 4  | *s=1/2*  | You get a "Head" on a coin toss  |
| 5 or 6  | *s=3/4*  | You do **not** roll a "1" on a 4-sided dice  |


#### D. Randomly choose an "active" cup
Use a dice to choose which cup will be the active cup (odd roll = orange cup.
even roll = green cup).

### E. Simulate the data
We'll simulate a data set of 10 bead colors, but we'll also keep track 
    of the cup color for each of the 10 draws.
We want to see if we can learn the correct values of *S* and *C* from 
    the bead color data.

Repeat the following 10 times:

  1. Randomly choose a bead from the "active" cup.
       1. record the bead color,
       2. record the cup color
  2. **Return** the bead to the cup (we are sampling with replacement)
  3. Use the switch procedure from step "Setup C" to decide whether or not to
     attempt a switch.
  4. *If (and only if)* the procedure indicates that you should
     attempt a cup-switch, roll the dice and use the "odd=orange and even=green" rule
     to pick a new cup.

### Discuss the following questions

**Question 1:** What is the *probability* that you change the cup color between
  two draws? (not the probability that you attempt cup-switch).

**Question 2:** Do you think that a maximum likelihood procedure would be
  able to prefer the correct value of *s* and *C* based on your sample of 10 draws?

**Question 3:** If you repeated step **E** many times and generated long series
  of bead colors each time...

**Q3A** Which parameter do you think that you would
  estimate more precisely using maximum likelihood: *s* or *C* ?

**Q3B** Do you think that you would be able to estimate the
  proportion of each bead color in each cup correctly?

**Q3C** As the length of your series of bead color got *really* long, do you 
  think that you'd be able to reject the alternative values
  of *s* and *C*?




