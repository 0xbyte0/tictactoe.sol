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

    gameBoard = tictactoe.newGame()
    print(format_game(gameBoard))

def main():
    deploy_game()