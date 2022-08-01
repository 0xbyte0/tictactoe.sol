from brownie import accounts
from brownie import TictactoeA as Tictactoe

"""
21 bits for each game

00 00 00 |
00 00 00 |= first 18 bits [000000000000000000]
00 00 00 |

[00]     [0]    [00 00 00 00 00 00 00 00 00]
------  ------  ------------------------------
 STATE   TURN              BOARD
"""

def test_newgame():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()
    game_board = tictactoe_game.getGame()

    assert game_board == 0x100000


def test_move():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()
    tictactoe_game.move(0, {"from": playerOne})

    """
    Note: Metadata not included

    10 00 00
    00 00 00
    00 00 00

    Note: metadata included

    binary => 0b101000000000000000001 
    hex    => 0x140001
    """
    gameBoard = tictactoe_game.getGame()

    assert gameBoard == 0x140001  

    tictactoe_game.move(2, {"from": playerTwo})

    """
    Note: Metadata not included
  
    10 00 01
    00 00 00
    00 00 00

    Note: metadata included
              
    binary => 0b100000000000000100001 
    hex    => 0x100021
    """
    gameBoard = tictactoe_game.getGame()

    assert gameBoard == 0x100021  

def test_horizontal_win():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()

    """
    10 10 10 |
    00 00 00 | = 000000000000010101
    00 00 00 |

    -----------------------------
    x  x  x
    0  0  0
    0  0  0
    """

    tictactoe_game.move(0, {"from": playerOne})
    tictactoe_game.move(3, {"from": playerTwo})
    tictactoe_game.move(1, {"from": playerOne})
    tictactoe_game.move(5, {"from": playerTwo})
    game_state = tictactoe_game.move(2, {"from": playerOne})
    game_state.wait(1)

    assert tictactoe_game.checkState(0) == 1

def test_vertical_win():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()

    """
    10 00 00 |
    10 00 00 | = 000001000001000001
    10 00 00 |

    -----------------------------
    x  0  0
    x  0  0
    x  0  0
    """

    tictactoe_game.move(0, {"from": playerOne})
    tictactoe_game.move(1, {"from": playerTwo})
    tictactoe_game.move(3, {"from": playerOne})
    tictactoe_game.move(4, {"from": playerTwo})
    game_state = tictactoe_game.move(6, {"from": playerOne})
    game_state.wait(1)

    assert tictactoe_game.checkState(0) == 1

def test_bl_tr_diagonal_win():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()

    """
    00 00 10 |
    00 10 00 | = 010000000100010000
    10 00 00 |

    -----------------------------
    0  0  x
    0  x  0
    x  0  0
    """

    tictactoe_game.move(2, {"from": playerOne})
    tictactoe_game.move(1, {"from": playerTwo})
    tictactoe_game.move(4, {"from": playerOne})
    tictactoe_game.move(3, {"from": playerTwo})
    game_state = tictactoe_game.move(6, {"from": playerOne})
    game_state.wait(1)

    assert tictactoe_game.checkState(0) == 1

def test_br_tl_diagonal_win():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()

    """
    10 00 00 |
    00 10 00 | = 000001000100000001
    00 00 10 |

    -----------------------------
    0  0  x
    0  x  0
    x  0  0
    """

    tictactoe_game.move(0, {"from": playerOne})
    tictactoe_game.move(1, {"from": playerTwo})
    tictactoe_game.move(4, {"from": playerOne})
    tictactoe_game.move(3, {"from": playerTwo})
    game_state = tictactoe_game.move(8, {"from": playerOne})
    game_state.wait(1)

    assert tictactoe_game.checkState(0) == 1

def test_draw():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()

    """
    10 01 01 |
    01 10 10 | = 100101010110101001
    10 10 01 |

    -----------------------------
    x  o  o
    o  x  x
    x  x  o
    """

    tictactoe_game.move(0, {"from": playerOne})
    tictactoe_game.move(1, {"from": playerTwo})
    tictactoe_game.move(4, {"from": playerOne})
    tictactoe_game.move(2, {"from": playerTwo})
    tictactoe_game.move(5, {"from": playerOne})
    tictactoe_game.move(3, {"from": playerTwo})
    tictactoe_game.move(6, {"from": playerOne})
    tictactoe_game.move(8, {"from": playerTwo})
    game_state = tictactoe_game.move(7, {"from": playerOne})
    game_state.wait(1)

    assert tictactoe_game.checkState(0) == 2

def test_still_playing():
    playerOne, playerTwo, *_ = accounts

    tictactoe_game = Tictactoe.deploy(playerTwo, {"from": playerOne})
    tictactoe_game.newGame()

    """
    10 01 01 |
    01 10 10 | = 100101010110101001
    10 10 01 |

    -----------------------------
    x  o  o
    o  x  x
    x  x  o
    """

    tictactoe_game.move(0, {"from": playerOne})
    tictactoe_game.move(1, {"from": playerTwo})
    tictactoe_game.move(4, {"from": playerOne})
    tictactoe_game.move(2, {"from": playerTwo})
    game_state = tictactoe_game.move(7, {"from": playerOne})
    game_state.wait(1)

    assert tictactoe_game.checkState(0) == 0
