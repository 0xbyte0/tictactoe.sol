# tictactoe.sol

An optimized tic-tac-toe game.

This game is an **on-chain** tictactoe game, where minters  play against each other . The is just a project I created while learning bits manipulations.


## What is Tic-tac-toe

Tic-tac-toe is a 2 player game where players take turns to make a finite amount of moves until either all moves has been exhausted (its a draw) or a player has won. Here is a typical tic-tac-toe game.

```
# an empty game   # game where play x won     

[ ] [ ] [ ]       [x] [ ] [o]
[ ] [ ] [ ]       [ ] [x] [o]
[ ] [ ] [ ]       [o] [ ] [x]  # Win is diagonal

# a draw
[x] [x] [o]
[o] [x] [x]
[x] [o] [o]
```
From the example above, 2 players are represented using to letters `X` and `O` and each take turns to win and also prevent the other player from winning.

So here is how we'd store a game in bits

```
 21 bits for each game
 
 00 00 00 |
 00 00 00 |= first 18 bits [000000000000000000]
 00 00 00 |

 [00]     [0]    [00 00 00 00 00 00 00 00 00]
------  ------  ------------------------------
STATE   TURN              BOARD
```

## Making moves and turns

When a player chooses to make a move he'd choose which place to play the move and indicate that it's the next players turn. Each move would be represented by a number like so:

```
[0] [1] [2] | => { [8] [7] [6] [5] [4] [3] [2] [1] [0] }
[3] [4] [5] |    --------------------------------------
[6] [7] [8] |                     BOARD
```

So typically a game play would be:

Given that player1 is `X` and player2 is `O`

```
- player1 makes more 0
- player2 makes more 4
- player1 makes more 3
- player2 makes more 6
- player1 makes more 1
- player2 makes more 2


[x1] [x3] [o3]
[x2] [o1] [  ]
[o2] [  ] [  ]

player 2 won :)
```


## Winning

Now, players can make moves and switch turns but they'd keep playing if we don't stop them when a player has won or it's a draw. So a player's win can either be `HORIZONTAL`, `VERTICAL` or `DIAGONAL`. Representing these in the board would look like:

#### Horizontal

```
HORIZONTAL_MASK = 0x3f

11 11 11 |
00 00 00 | => 000000000000111111 = 0x3f
00 00 00 |    

These are the HORIZONTAL wins

1. x  x  x  2. | 0  0  0  3. | 0  0  0
   0  0  0     | x  x  x     | 0  0  0
   0  0  0     | 0  0  0     | x  x  x
   
For player 1
    H1. 10 10 10
        00 00 00 =   000000000000010101
        00 00 00
        
    H2. 00 00 00
        10 10 10 =   000000010101000000 : H1 << 6
        00 00 00
        
    H3. 00 00 00
        00 00 00 =   010101000000000000 : H2 << 6 or H1 << 12
        10 10 10
        
Note: HORIZONTAL_MASK / 3 == H1
```


#### Vertical

```
VERTICAL_MASK = 0x3f

00 00 11 |
00 00 11 | => 0b11000011000011 = 0x30C3
00 00 11 |


These are the VERTICAL wins
1. x  0  0  2. | 0  x  0  3. | 0  0  x
   x  0  0     | 0  x  0     | 0  0  x
   x  0  0     | 0  x  0     | 0  0  x
   
For player 1
    V1. 10 00 00
        10 00 00 =   000001000001000001
        10 00 00
        
    V2. 00 10 00
        00 10 00 =   000100000100000100 : V1 << 2
        00 10 00
        
    V3. 00 00 10
        00 00 10 =   010000010000010000 : V2 << 2 or V1 << 4
        00 00 10
        

Note: VERTICAL_MASK / 3 == V1
```

### Diagonal 

```
11 00 00 |
00 11 00 | => 0b110000001100000011 = 0x30303
00 00 11 |

    
00 00 11 |
00 11 00 | => 0b1100110011 = 0x3330
11 00 00 |


These are the DIAGONAL wins
1. x  0  0  2. | 0  0  x
   0  x  0     | 0  x  0 
   0  0  x     | x  0  0  
   
For player 1
    D1. 10 00 00
        00 10 00 =   010000000100000001
        00 00 10
        
    D2. 00 00 10
        00 10 00 =   000001000100010000
        10 00 00
        
BL_TO_TR_DIAGONAL_MASK / 3 == D1
BR_TO_TL_DIAGONAL_MASK / 3 == D2
```

## Installation

Python is required.

`pip install -r requirements.txt`

## Deploy Locally and Run Tests using [Brownie](https://eth-brownie.readthedocs.io/en/stable/)

`brownie run scripts/deploy.py`

`brownie test`
