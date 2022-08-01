// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

/*
* /        /      | /      \ /        /      \  /      \ /        /      \ /        |
* $$$$$$$$/$$$$$$/ /$$$$$$  |$$$$$$$$/$$$$$$  |/$$$$$$  |$$$$$$$$/$$$$$$  |$$$$$$$$/ 
*    $$ |    $$ |  $$ |  $$/    $$ | $$ |__$$ |$$ |  $$/    $$ | $$ |  $$ |$$ |__    
*    $$ |    $$ |  $$ |         $$ | $$    $$ |$$ |         $$ | $$ |  $$ |$$    |   
*    $$ |    $$ |  $$ |   __    $$ | $$$$$$$$ |$$ |   __    $$ | $$ |  $$ |$$$$$/    
*    $$ |   _$$ |_ $$ \__/  |   $$ | $$ |  $$ |$$ \__/  |   $$ | $$ \__$$ |$$ |_____ 
*    $$ |  / $$   |$$    $$/    $$ | $$ |  $$ |$$    $$/    $$ | $$    $$/ $$       |
*    $$/   $$$$$$/  $$$$$$/     $$/  $$/   $$/  $$$$$$/     $$/   $$$$$$/  $$$$$$$$/ 
*/

/// @title An optimized tic-tac-toe game
/// @author 0xosas
/// @author Modified from (https://github.com/0xosas/tictactoe.sol/blob/master/contracts/Tictactoe.sol)
contract TictactoeA {

    error Unauthorized();

    uint256 gameBoard = 0;
    uint256 internal constant HORIZONTAL_MASK = 0x3F;
    uint256 internal constant VERTICAL_MASK = 0x30C3;
    uint256 internal constant BR_TO_TL_DIAGONAL_MASK = 0x30303;
    uint256 internal constant BL_TO_TR_DIAGONAL_MASK = 0x3330;

    address internal playerOne;
    address internal playerTwo;

    constructor(address _playerTwo) {
        require(_playerTwo != address(0));
        playerOne = msg.sender;
        playerTwo = _playerTwo;
    }

    modifier isPlayer(address _player){
        if(_player != playerOne && _player != playerTwo) 
            revert Unauthorized();
        _;
    }

    modifier isTurn(address _player){
        require((gameBoard >> 18 & 0x1) == playerId(_player), "Not your turn");
        _;
    }

    modifier moveIsValid(uint256 _move) {
        uint p1 = _move << 1;
        uint p2 = p1 + 1;

        require(!(((gameBoard >> p1) & 1) == 1 || ((gameBoard >> p2) & 1) == 1) ,"invalid move");
        require(_move < 9 ,"invalid move");
        _;
    }

    function playerId(address playerAddr) internal view returns(uint256) {
        return playerAddr == playerOne ? 0 : 1;
    } 

    function newGame() external isPlayer(msg.sender) returns (uint256){
        assembly {
            let _gameBoard := sload(gameBoard.slot)
            let newGameBoard := mload(0x40)

            switch _gameBoard
            case 0 { mstore(newGameBoard, or(_gameBoard, shl(20, 1))) }
            default { mstore(newGameBoard, or(shl(21, _gameBoard), shl(20, 1))) }

            sstore(gameBoard.slot, mload(newGameBoard))
            return (newGameBoard, 32)
        }
    }


    function getGame() external view returns (uint256){
        return gameBoard;
    }

    function move(uint256 _move) isPlayer(msg.sender) isTurn(msg.sender) moveIsValid(_move) external returns (uint256) {
        
        require(gameBoard >> 19 & 1 == 0 && gameBoard >> 20 & 1 == 1, "Game has ended");

        uint256 _playerId = playerId(msg.sender);
        
        bytes4 sig = bytes4(keccak256("checkState(uint256)"));

        assembly {
            let gb := sload(gameBoard.slot)
            gb := xor(gb, shl(add(shl(1, _move), _playerId), 1))
            gb := xor(gb, shl(18, 1))

            let ptr := mload(0x40)
            mstore(ptr, sig)
            mstore(add(ptr, 0x04), _playerId)

            let success := staticcall(gas(), 4, ptr, 0x24, 0, 0)

            if iszero(success) { revert (0,0) }
            
            let gameState := mload(ptr)

            switch gameState
            case 1 {
                sstore(gameBoard.slot, xor(gb, shl(add(19, _playerId), 1)))
            }
            default { sstore(gameBoard.slot, gb) }
            return (ptr, 0x20)
        }
    }
    
    function checkState(uint256 _playerId) public view returns (uint256){
        assembly {
            let gb := sload(gameBoard.slot)

            // Let the state be the start of the free memory.
            let state := mload(0x40)
            
            for { let i := 0 } lt(i, 3) { i := add(i, 1)} {
                
                switch i
                case 0 {
                    if eq(and(gb, HORIZONTAL_MASK), shl(_playerId, div(HORIZONTAL_MASK, 3))) {
                        mstore(state, 1)
                        return(state, 32)
                    }
                }
                default {   
                    if eq(and(gb, shl(shl(i, 3), HORIZONTAL_MASK)), shl(shl(i, 3), shl(_playerId, div(HORIZONTAL_MASK, 3)))) {
                        mstore(state, 1)
                        return(state, 32)
                    }
                }
            }

            for { let i := 0 } lt(i, 3) { i := add(i, 1)} {
                
                switch i
                case 0 {
                    if eq(and(gb, VERTICAL_MASK), shl(_playerId, div(VERTICAL_MASK, 3))) {
                        mstore(state, 1)
                        return(state, 32)
                    }
                }
                default {   
                    if eq(and(gb, shl(shl(i, 1), VERTICAL_MASK)), shl(shl(i, 1), shl(_playerId, div(VERTICAL_MASK, 3)))) {
                        mstore(state, 1)
                        return(state, 32)
                    }
                }
            }

            if eq(and(gb, BR_TO_TL_DIAGONAL_MASK), shl(_playerId, div(BR_TO_TL_DIAGONAL_MASK, 3))) {
                mstore(state, 1)
                return (state, 32)
            }

            if eq(and(gb, BL_TO_TR_DIAGONAL_MASK), shl(_playerId, div(BL_TO_TR_DIAGONAL_MASK, 3))) {
                mstore(state, 1)
                return (state, 32)
            }

            /// Checks if all fields has been played
            
            for { let i := 0 } lt(i, 9) { i := add(i, 1) } {
                if iszero(or(and(gb, 1), and(gb, 2))) {
                    mstore(state, 0)
                    return (state, 32)
                }
                
                gb := shr(2, gb)
            }
        }

        return 2;
    }

}