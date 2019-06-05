### Goals
Use dice to simulate the tip character states of a character evolving under
the HKY model.
This is a set of instructions for the [dice simulation by John Huelsenbeck](https://molevol.mbl.edu/images/1/1a/WoodsHole2012_1.pdf)

#### Simulating a *U(0,1)* draw
Whenever the instructions call for a Uniform(0,1) variable
  you can either:

  * call `runif(1)` if `R`, or
  * roll the 10 sided dice twice. The record the first number as the tenths place
  and the second number as the hundreths place. 
  So if you rolled a `1` and a `6`, you'd say that your *u=0.16*  for that
  random number draw.



#### Randomly choose a root base
See https://mtholder.github.io/reveal/john-huelsenbeck-dice.html#/4 for a 
graphical depiction

   1. Draw a random number
   2. Choose a base:
       * A if *u < 0.4*,
       * C if *0.4 ≤ u < 0.7*,
       * G if *0.7 ≤ u < 0.*,
       * T otherwise

