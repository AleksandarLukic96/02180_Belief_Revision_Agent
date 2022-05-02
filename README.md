# 02180_Belief_Revision_Agent
A repository for the implementation of a belief revision agent in 02180 Introduction to AI

In this repository you will find an implementation of a belief revision agent written in python.
Belief revision is a concept in which logical sentences are structured in belief bases where their logical relations are maintained or updated according to new sentences/beliefs. The most well known paradigm in the field is the AGM framework, which is the one that has been implemented in this project.

## **Belief_base.py**
This file holds the implementation of the belief base object along with the function implementation the AGM operations; expansion(add), contraction and revision. To check if the belief base entails or satisfies a sentence the two functions _satisfiable()_ and _entails()_ can be used.  The file also holds a print-function to show all the sentences in the belief base in the terminal. 

## **CNF.py**
The function _to\_cnf()_ takes a first order logical sentence as input and converts it into conjunctive normal form, CNF. The function then returns a list of cluses in the CNF. The remaining functions are implemented to make up the CNF algorithm:
- Replacing bi-implications with implications
- Replacing implications with negations
- Removing negations
- Distribute clauses

More on this algorithm in section 7.5 in Russel, Norvig.

## **inference.py**
In this file, the DPLL algorithm is implemented. The DPLL algoirthm is a recursive backtracking algorithm used to determine the satisfiability of a sentence in CNF. If there exists a model where the sentence is satisfiable given a belief base. 

## **utils.py**
This file holds functions used to read and handle sentences expressed as strings. These functions then interpret the symbols as such:

**The logic syntax used is the following:**
- or: |
- and: &
- implies: ->
- biimplication: <->
- not: -
- "( )"Parentheses are assumed to be used everywhere where two different operators appear, except for the not operator

## **main.py**

## **/tests**
This subfolder holds the test cases to show the validity of the implementation as well as testing key aspects and functionalities.

### **AGM.py**
In this file the 5 AGM postulates: Success, Inclusion, Vacuity, Consistency and Extensionality, are proven for the implemntation.

### **Sunflower.py**
This test implements the flower variation of the mastermind game from the exercise session of week 10 in the course.

### **test_cases.py**
These test cases are made to show how the belief base are translated into CNF.
The CNF form is neccesary to execute the DPLL algorithm.

## **/mastermind**
This subfolder holds the implementation for the game Master Mind. 
When running the _main.py_-file, the user can choose to play the game against the implemented AI.

### **Feedback.py**
For the AI to be able to make qualified guesses, the _Feedback.py_-file implements the rules, how the AI reads the feedback logically as sentences which are then stored in the AIs belief base. Using the belief base the AI can then determine its next guess.  

### **Master_mind.py**
This file runs a set number of Master Mind games in which the AI has to guess the correct answer from a randomly generated pattern. The average playing time and guesses used are then printed in the terminal by the end.

### **User_playing_master_mind.py**
This file implements the Master Mind game, where the AI tries to guess the player's pattern. If the AI guesses correctly and the player answers with all green pins, "g g g g", the game simply stops. 

## **main.py**

# **How to create a belief base or play Master Mind:** ##
## Setup:
1. Download the folder from a zip-file or the git-repository: https://github.com/AleksandarLukic96/02180_Belief_Revision_Agent and save it on the computer.

2. Open your choice of terminal, ex. Command Prompt (cmd.exe) and change directory to where you have saved the folder.
```
> cd 02180_Belief_Revision_Agent
```

3. Now run the file _main.py_.
```
> main.py
```

The commands for using the program are now printed in the terminal along with the instructions and explanation for each command.

## Create and adjust a belief base
Start by creating a belief base by using the command:
```
> CREATE {NAME}
```
Now whenever we want to expand, contract or revise we can refer to this created belief base wiht name {NAME}. 

The sentences which are written in the terminal must follow the first order logic syntax. We can then expand the belief base with a sentence using the syntax:
```
> EXPAND {NAME} {SENTENCE} {WEIGHT}
```

When the sentence is then expanded into the belief base, it will be stored in first order logic form as well as CNF. This can be seen when printing a non-empty belief base:  
```
Your input: CREATE BASE
Your input: EXPAND BASE p->q 100
Your input: PRINT BASE
Belief | Certainty:
p->q   | 100


Belief in CNF  | Certainty:
q|-p           | 100
Your input:
```
When revisioning the belief base, the sentence is checked and if it contradicts an old belief, the latter is removed from the belief base:
```
Your input: EXPAND BASE p->q 10
Your input: REVISION BASE -p->-q 10
Your input: REVISION BASE p->-q 10
Your input: REVISION BASE -p->q 10
Removes sentence p->q
```

We can also check whether a belief base entails a sentence: 
```
Your input: ENTAILS BASE p->q
The belief base: BASE entails the sentence: p->q
```

or if the belief base satisfy a sentence:
```
The belief base: BASE satisfy the sentence: p->q
Your input:
```

## Play Master Mind
In this game of Master Mind, the AI is trying to guess the players 4 pins made up of 6 possible colors. When the AI states a guess, the player has to then respond help the AI get closer to the correct pattern by indicating which pin the AI has guessed correctly(g for green), which pin has a color that is not part of the players 4 pins(r for red) or if a pin has a color which is present in the 4 pins, but not on the guessed one(O for orange). 
To play with the AI, simply write "MASTER MIND":
```
Your input: MASTER MIND
You are playing master mind with 6 colours and 4 pegs
Make a code of the following colors: ['r', 'g', 'y', 'b', 'w', 'p']
Remember your solution and provide feedback to the computers guesses:

The computers guess number 1:
r on 1
w on 2
r on 3
r on 4

Give your response of 4 chararcters (r, g or o):
```
When the AI has guessed the correct pattern, it will simply not write anything more:

```
Thinking...
The computers guess number 7:
r on 1
r on 2
r on 3
r on 4

Give your response of 4 chararcters (r, g or o): g g g g
Thinking...
Your input:
```
