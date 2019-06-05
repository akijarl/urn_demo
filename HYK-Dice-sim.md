### Goals
Use dice to simulate the tip character states of a character evolving under
the HKY model.
This is a set of instructions for the [dice simulation by John Huelsenbeck](https://molevol.mbl.edu/images/1/1a/WoodsHole2012_1.pdf)

#### Simulating a *U(0,1)* draw
Whenever the instructions call for a Uniform(0,1) variable
  you can either:

  * call `runif(1)` if `R`, or
  * roll the 10 sided dice twice. Record the first number as the tenths place
  and the second number as the hundreths place. 
  So if you rolled a `1` and a `6`, you'd say that your *u=0.16*  for that
  random number draw.



#### Randomly choose a root base
See https://mtholder.github.io/reveal/john-huelsenbeck-dice.html#/4 for a 
graphical depiction

   1. Draw a random Uniform(0,1) variable, *u*
   2. Choose a base:
       * A if *u < 0.4*,
       * C if *0.4 ≤ u < 0.7*,
       * G if *0.7 ≤ u < 0.9*,
       * T otherwise

#### Simulate the descendant state for each branch
See the simulation tree at 
https://mtholder.github.io/reveal/john-huelsenbeck-dice.html#/6

Once you know the ancestor state for a branch you can use the following recipe
   to generate a descendant state for that branch.
So a valid order of branches to sweep over would be 6, 5, 4, 3, 2, and 1 on the figure of the tree.

For each branch:
  1. start keeping track of your position on the branch by writing down *p=0* to
  indicate that you are in the starting point of the branch.
  2. Set the current base to the ancestral base.
  3. Find the element on the diagonal for the row that represents the ancestral
    base for the branch. This will be the only negative number in the row. This
    represents the rate of leaving that base. 
    We'll call the flux out of the base λ.
  4. Draw a waiting time, *t*:
      1. draw a random Uniform(0,1) variable, *u*
      2. calculate *t = log(u)/λ*
  5. Set the current position by adding *t* to *p* (so *p = p + t*)
  6. If the new value of *p* is longer than the branch length shown on the tree, then
    no additional substitution occured. 
      1. Write down your current base as the descendant base.
      2. **Stop** and move to the next branch.
  7. If *p* is less than the branch length, 
      1. choose a new base to be the current base (see below)
      2. **go back to step 3** of this recipe and continue.

#### Choosing a new base.
The new base should be drawn in proportion to the rate of moving into each of the destination
  bases.
The 3 positive rates in each row add up to the absolute value of the negative flux.
So we can get the probability of each destination base given that there is a substitution
by dividing each positive number by the absolute value of the diagonal element:

|   | A  | C  | G  | T  |
|---|---|---|---|---|
|  A |   |  0.2144 | 0.7144 | 0.07110    |
|  C |  0.364    |       |   0.182    |   0.454  | 
|  G | 0.833  | 0.125  |   | 0.041  |
|  T |  0.190 |   0.714 |  0.096  |   |

and the cumulative probabilities are:

|   | A  | C  | G  | T  |
|---|---|---|---|---|
|  A |   | 0.2144 | 0.9288 | 1.0    |
|  C |  0.364 | |  0.546 | 1.000   | 
|  G | 0.833  | 0.958  |   | 1.0  |
|  T |  0.190 |   0.904 |  1.0  |   |


Use a similar method that you used when choosing a root base to convert these cumulative probabilities into the destination base for each substitution.
