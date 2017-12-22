from magic_gen import *
from random import random
import itertools
import os

class tic_tac_toe:
    """
    Tic-Tac-Toe Game with Bot
    Attributes:  
        start (int): Player to start the game. 0 for "Human". Otherwise "Bot"
    """
    def __init__(self,start: int):
        """
        Constructor
        Args:  
            start (int): Player to start the game. 0 for "Human". Otherwise "Bot"            
        """
        self.board = [[0 for y in range(0,3)] for x in range(0,3)]
        self.magic_square = odd(3)
        self.magic_sum = int(3*(3**2+1)/2)
        self.valid_magic_triplets = magic_sum_set_split(3)[0]
        self.start_player = 'H' if start == 0 else 'C'
        self.player = self.start_player
        self.move_count = 0
        self.finished = False

    def print_board(self,initial: int):
        """
        Print the Tic-Tac-Toe Board
        Args:  
            initial: Flag to print the locations on the board
        Returns:  
            None
        """
        for x in range(0,3):
            for y in range(0,3):
                c = '\33[92mX\33[0m' if self.board[x][y] == 1 else '\33[92mO\33[0m' if self.board[x][y] == 2 else ' ' if initial == 1 else '\33[92m{}\33[0m'.format(x*3+y+1)
                print(" ", c, " |", end="") if y != 2 else print(" ", c)
            print("-----+-----+-----") if x != 2 else print()

    def checkFinish(self):
        """
        Checks for end of game
        Args:  
            None
        Returns:  
            None
        """
        X_loc = self.X_loc()
        X_magic_values = [self.magic_square[x][y] for x, y in X_loc]
        X_win = len(set(itertools.permutations(X_magic_values,3)).intersection(self.valid_magic_triplets)) > 0
        O_loc = self.O_loc()
        O_magic_values = [self.magic_square[x][y] for x, y in O_loc]
        O_win = len(set(itertools.permutations(O_magic_values,3)).intersection(self.valid_magic_triplets)) > 0
        if(X_win):
            print("\33[94mPlayer(X) -","Human" if self.start_player == 'H' else "Computer","Wins\33[0m")
            self.finished = True
        if(O_win):
            print("\33[94mPlayer(O) -","Computer" if self.start_player == 'H' else "Human","Wins\33[0m")
            self.finished = True
        if self.move_count == 9 and not X_win and not O_win:
            print("\33[94mDRAW GAME\33[0m")
            self.finished = True

    def move(self,loc: int) -> bool:
        """
        Places a piece in the specified location on the board
        Args:  
            loc: Location on the board (Valid Locations -> [1,9])
        Returns:  
            Move Flag. True if moved. False otherwise
        """
        if(loc < 1 or loc > 9):
            return False
        x = int((loc-1)/3)
        y = int((loc-1)%3)
        move_success = True if self.board[x][y] == 0 else False
        c = 1 if self.start_player == self.player else 2
        if(move_success):
            self.board[x][y] = c
            self.player = 'H' if self.player == 'C' else 'C'
            self.move_count = self.move_count+1
        return move_success

    def magic_loc(self,l: list):
        """
        Finds values from Magic Square such that it is valid value that completes magic sum for some pair of magic values corresponding to given locations (valid -> collinear point)
        Args:  
            l: List of coordinates (Valid Coordinates -> x - [0,3), y - [0,3))
        Returns:  
            List of values from Magic Square that satisfy magic sum and are collinear with some pair of locations
        """
        pairs = list(itertools.combinations(l,2))
        triplets = []
        for p1, p2 in pairs:
            magic_p1 = self.magic_square[p1[0]][p1[1]]
            magic_p2 = self.magic_square[p2[0]][p2[1]]
            diff = self.magic_sum-(magic_p1+magic_p2)
            if 0 < diff < 10:
                triplets.append((magic_p1,magic_p2,diff))
        valid_triplets = [x for x in triplets if len(set(itertools.permutations(x)).intersection(self.valid_magic_triplets)) != 0]
        return [x[2] for x in valid_triplets]

    def avail_loc(self) -> list:
        """
        Finds available locations on the board
        Args:  
            None
        Returns:  
            List of available locations on the board
        """
        return list(map(lambda x: x[0]*3+x[1]+1,[(x,y) for x in range(0,3) for y in range(0,3) if self.board[x][y] == 0]))

    def X_loc(self) -> list:
        """
        Finds locations of 'X' on the board
        Args:  
            None
        Returns:  
            List of locations of 'X' on the board
        """
        return [(x,y) for x in range(0,3) for y in range(0,3) if self.board[x][y] == 1]

    def O_loc(self) -> list:
        """
        Finds locations of 'O' on the board
        Args:  
            None
        Returns:  
            List of locations of 'O' on the board
        """
        return [(x,y) for x in range(0,3) for y in range(0,3) if self.board[x][y] == 2]

    def win_loc(self) -> tuple:
        """
        Finds win locations for both players
        Args:  
            None
        Returns:  
            Tuple of win locations for both players (in the order (X,O))
        """
        X_loc = self.X_loc()
        X_valid_magic = self.magic_loc(X_loc)
        X_win_loc_poss = [(x,y) for val in X_valid_magic for x in range(0,3) for y in range(0,3) if val == self.magic_square[x][y]]
        X_win_loc = [(x,y) for x, y in X_win_loc_poss if self.board[x][y] == 0]
        O_loc = self.O_loc()
        O_valid_magic = self.magic_loc(O_loc)
        O_win_loc_poss = [(x,y) for val in O_valid_magic for x in range(0,3) for y in range(0,3) if val == self.magic_square[x][y]]
        O_win_loc = [(x,y) for x, y in O_win_loc_poss if self.board[x][y] == 0]
        return (X_win_loc,O_win_loc)

    def computer_move(self) -> int:
        """
        Bot algorithm to make right move
        Args:  
            None
        Returns:  
            Position to place the piece (Valid Positions -> [1-9])
        """
        if(self.player != 'C'):
            return 0
        if(self.move_count == 0):
            return 5
        elif(self.move_count == 1):
            if(self.board[1][1] == 0):
                return 5
            else:
                rand_loc = int(random()*4)
                corners = [1,3,7,9]
                return corners[rand_loc]
        elif(self.move_count >= 2):
            X_win_locations, O_win_locations = self.win_loc()
            win_locations = X_win_locations if self.start_player == 'C' else O_win_locations
            lose_locations = X_win_locations if self.start_player == 'H' else O_win_locations
            if(len(win_locations) > 0):
                win_x = win_locations[0][0]
                win_y = win_locations[0][1]
                return win_x*3+win_y+1
            elif(len(lose_locations) > 0):
                block_x = lose_locations[0][0]
                block_y = lose_locations[0][1]
                return block_x*3+block_y+1
            else:
                avail_loc = self.avail_loc()
                avail_corners = [x for x in [1,3,7,9] if x in avail_loc]
                avail_mids = [x for x in [2,4,6,8] if x in avail_loc]
                if(self.move_count%2 == 0):
                    X_loc = self.X_loc()
                    X_valid_magic = list(self.magic_loc(X_loc))
                    if(len(X_valid_magic) == 0):
                        return avail_corners[int(random()*len(avail_corners))]
                    elif(len(X_valid_magic) == 1):
                        curr_corner = X_loc[0] if X_loc[0] != (1,1) else X_loc[1]
                        rand_loc = int(random())+1.1
                        horiz = False if 2 in self.board[curr_corner[0]] else True
                        rand_loc_x = (curr_corner[0]+rand_loc)%3 if not horiz else curr_corner[0]
                        rand_loc_y = (curr_corner[1]+rand_loc)%3 if horiz else curr_corner[1]
                        return rand_loc_x*3+rand_loc_y+1
                    else:
                        return avail_loc[int(random()*len(avail_loc))]
                else:
                    O_loc = self.O_loc()
                    O_valid_magic = list(self.magic_loc(O_loc))
                    if(self.board[1][1] == 1):
                        if(len(O_valid_magic) == 0):
                            return avail_corners[int(random()*len(avail_corners))]
                        else:
                            return avail_loc[int(random()*len(avail_loc))]
                    else:
                        if(len(avail_corners) == 2):
                            return avail_mids[int(random()*4)]
                        elif(len(avail_mids) == 2):
                            return avail_corners[int(random()*4)]
                        else:
                            X_loc = list(map(lambda x: x[0]*3+x[1]+1,self.X_loc()))
                            rand_loc = 8 if set([1,6]).issubset(X_loc) or set([3,4]).issubset(X_loc) else 4 if set([3,8]).issubset(X_loc) or set([9,2]).issubset(X_loc) else 2 if set([9,4]).issubset(X_loc) or set([7,6]).issubset(X_loc) else 6
                            if(self.board[int((rand_loc-1)/3)][int((rand_loc-1)%3)] != 0):
                                rand_loc = avail_loc[int(random()*len(avail_loc))]
                            return rand_loc

def game():
    play = True
    while(play):
        start = int(not input("\33[94mTo start first Enter 0: \33[0m") == '0')
        piece = 'X' if start == 0 else 'O'
        game = tic_tac_toe(start)
        game.print_board(0)
        while(not game.finished):
            if(game.player == 'H'):
                while(True):
                    try:
                        loc = int(input("\33[93mPlace {} at location [1,9]: \33[0m".format(piece)))
                        if(not game.move(loc)):
                            print("\33[91mEnter valid location for {}\33[0m".format(piece))
                        else:
                            break
                    except (TypeError, ValueError):
                        print("\33[91mEnter proper input\33[0m")
                        continue
            else:
                print("\33[95mBot's Turn: \33[0m")
                game.move(game.computer_move())
            game.print_board(1)
            game.checkFinish()
        play = not (input("\33[93mEnter q to quit: \33[0m") == 'q')
        os.system("clear")

if __name__ == "__main__":
    try:
        game()
    except (KeyboardInterrupt, EOFError):
        print("\33[91m\nExiting Game\33[0m")
        exit