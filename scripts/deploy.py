from brownie import accounts, Tictactoe

def format_game(game):
    out = ""
    for x in range(1, 22):
        if x < 19:
            out += str((game >> (x-1)) & 0x1)
            if x % 6 == 0:
                out += "\n"
            elif x % 2 == 0:
                out += " "
        
    return out
    
def deploy_game():
    playerOne, playerTwo, *_ = accounts
    tictactoe = Tictactoe.deploy(playerTwo, {"from": playerOne})

    tictactoe.newGame()

    tictactoe.move(0, {"from": playerOne})
    tictactoe.move(1, {"from": playerTwo})
    tictactoe.move(3, {"from": playerOne})
    tictactoe.move(4, {"from": playerTwo})
    game_state = tictactoe.move(6, {"from": playerOne})
    game_state.wait(1)

def main():
    deploy_game()