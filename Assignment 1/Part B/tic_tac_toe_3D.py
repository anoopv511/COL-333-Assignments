from magic_gen import *
from random import random
import os

class tic_tac_toe_3D:
    """
    Tic-Tac-Toe Game with Bot
    Attributes:  
        start (int): Player to start the game. 0 for "Human". Otherwise "Bot"  
        all_loc, center, faces, corners, edges (list): Cube positions
    """

    all_loc = list(set(itertools.permutations([0,0,0,1,1,1,2,2,2],3)))
    center = [(1,1,1)]
    faces = list(set(itertools.permutations([1,1,0])))+list(set(itertools.permutations([1,1,2])))
    corners = list(set(itertools.permutations([2,0,0])))+list(set(itertools.permutations([0,2,2])))+[(0,0,0)]+[(2,2,2)]
    edges = list(set(all_loc).difference(set(center+corners+faces)))

    def __init__(self,start: int):
        """
        Constructor
        Args:  
            start (int): Player to start the game. 0 for "Human". Otherwise "Bot"            
        """
        self.board = [[[0 for z in range(0,3)] for y in range(0,3)] for x in range(0,3)]
        self.magic_cube = odd(3)
        self.magic_sum = int(3*(3**3+1)/2)
        self.valid_magic_triplets = list(magic_sum_set_split(3)[0])
        self.start_player = 'H' if start == 0 else 'C'
        self.player = self.start_player
        self.move_count = 0
        self.finished = False

    def print_board(self,initial: int):
        """
        Print the Tic-Tac-Toe 3D Board
        Args:  
            initial: Flag to print the locations on the board
        Returns:  
            None
        """
        print("\n\33[94mTop View\33[0m\n")
        _ = [print("\33[95mLayer {}\t\t\t\33[0m".format(x), end="{0}".format("\t" if x != 3 else "\n\n")) for x in range(1,4)]
        for y in range(0,3):
            for x in range(0,3):
                for z in range(0,3):
                    c = '\33[92mX\33[0m' if self.board[x][y][z] == 1 else '\33[92mO\33[0m' if self.board[x][y][z] == 2 else ' ' if initial == 1 else '\33[91m{}\33[0m'.format(x*9+y*3+z+1)
                    print(" ", c, " |", end="") if z != 2 else print(" ", c, end=" \t\t")
            print("\n-----+-----+-----\t\t-----+-----+-----\t\t-----+-----+-----\n", end="") if y != 2 else print()
        print("\n\33[94mFront View\33[0m\n")
        _ = [print("\33[95mLayer {}\t\t\t\33[0m".format(x), end="{0}".format("\t" if x != 3 else "\n\n")) for x in range(1,4)]
        for x in range(0,3):
            for y in range(2,-1,-1):
                for z in range(0,3):
                    c = '\33[92mX\33[0m' if self.board[x][y][z] == 1 else '\33[92mO\33[0m' if self.board[x][y][z] == 2 else ' ' if initial == 1 else '\33[91m{}\33[0m'.format(x*9+y*3+z+1)
                    print(" ", c, " |", end="") if z != 2 else print(" ", c, end=" \t\t")
            print("\n-----+-----+-----\t\t-----+-----+-----\t\t-----+-----+-----\n", end="") if x != 2 else print()
        print("\n\33[94mLeft Side View\33[0m\n")
        _ = [print("\33[95mLayer {}\t\t\t\33[0m".format(x), end="{0}".format("\t" if x != 3 else "\n\n")) for x in range(1,4)]
        for x in range(0,3):
            for z in range(0,3):
                for y in range(0,3):
                    c = '\33[92mX\33[0m' if self.board[x][y][z] == 1 else '\33[92mO\33[0m' if self.board[x][y][z] == 2 else ' ' if initial == 1 else '\33[91m{}\33[0m'.format(x*9+y*3+z+1)
                    print(" ", c, " |", end="") if y != 2 else print(" ", c, end=" \t\t")
            print("\n-----+-----+-----\t\t-----+-----+-----\t\t-----+-----+-----\n", end="") if x != 2 else print()
        print("\n\33[94mDiagonal_1 View\33[0m\n")
        for x in range(0,3):
            for y,z in zip(range(2,-1,-1),range(0,3)):
                c = '\33[92mX\33[0m' if self.board[x][y][z] == 1 else '\33[92mO\33[0m' if self.board[x][y][z] == 2 else ' ' if initial == 1 else '\33[91m{}\33[0m'.format(x*9+y*3+z+1)
                print(" ", c, " |", end="") if y != 0 else print(" ", c)
            print("-----+-----+-----") if x != 2 else print()
        print("\n\33[94mDiagonal_2 View\33[0m\n")
        for x in range(0,3):
            for y,z in zip(range(0,3),range(0,3)):
                c = '\33[92mX\33[0m' if self.board[x][y][z] == 1 else '\33[92mO\33[0m' if self.board[x][y][z] == 2 else ' '  if initial == 1 else '\33[91m{}\33[0m'.format(x*9+y*3+z+1)
                print(" ", c, " |", end="") if y != 2 else print(" ", c)
            print("-----+-----+-----") if x != 2 else print()

    def add_extra_triplets(self):
        print_3D(self.magic_cube)
        print("Enter triplets in the format: triplet, triplet, ... [Use numbers only]")
        extra_triplets = [tuple(map(int,x.split())) for x in input().split(",")]
        valid_extra_triplets_repetition = [x for x in extra_triplets if len(x) == 3 and 0 < x[0] < 28 and 0 < x[1] < 28 and 0 < x[2] < 28 and x[0] != x[1] and x[1] != x[2] and x[2] != x[0]]
        valid_extra_triplets = []
        for x in valid_extra_triplets_repetition:
            if len(set(itertools.permutations(x)).intersection(set(valid_extra_triplets))) == 0:
                valid_extra_triplets.append(x)
        print("Valid Triplets - ", valid_extra_triplets)
        valid_magic_triplets_set = set(self.valid_magic_triplets)
        valid_extra_triplets_new = [x for x in valid_extra_triplets if len(set(itertools.permutations(x)).intersection(valid_magic_triplets_set)) == 0]
        self.valid_magic_triplets = self.valid_magic_triplets+valid_extra_triplets_new

    def checkFinish(self):
        """
        Checks for end of game
        Args:  
            None
        Returns:  
            None
        """
        X_loc = self.X_loc()
        X_magic_values = [self.magic_cube[x][y][z] for x, y, z in X_loc]
        X_points = len(set(itertools.permutations(X_magic_values,3)).intersection(set(self.valid_magic_triplets)))
        O_loc = self.O_loc()
        O_magic_values = [self.magic_cube[x][y][z] for x, y, z in O_loc]
        O_points = len(set(itertools.permutations(O_magic_values,3)).intersection(set(self.valid_magic_triplets)))
        print("X Points - {0}, O Points - {1}".format(X_points,O_points))
        if self.move_count == 20:
            if(X_points > O_points):
                print("\33[94mPlayer(X) -","Human" if self.start_player == 'H' else "Computer","Wins\33[0m")
            elif(O_points > X_points):
                print("\33[94mPlayer(O) -","Computer" if self.start_player == 'H' else "Human","Wins\33[0m")
            else:
                print("\33[94mDRAW GAME\33[0m")
            self.finished = True

    def move(self,loc: int) -> bool:
        """
        Places a piece in the specified location on the 3D board
        Args:  
            loc: Location on the 3D board (Valid Locations -> [1,27])
        Returns:  
            Move Flag. True if moved. False otherwise
        """
        if(loc < 1 or loc > 27):
            return False
        x = int((loc-1)/9)
        y = int(((loc-1)%9)/3)
        z = int(((loc-1)%9)%3)
        move_success = True if self.board[x][y][z] == 0 else False
        c = 1 if self.start_player == self.player else 2
        if(move_success):
            self.board[x][y][z] = c
            self.player = 'H' if self.player == 'C' else 'C'
            self.move_count = self.move_count+1
        return move_success

    def magic_loc(self,l: list):
        """
        Finds values from Magic Cube such that it is valid value that completes magic sum for some pair of magic values corresponding to given locations (valid -> collinear point)
        Args:  
            l: List of coordinates (Valid Coordinates -> x - [0,3), y - [0,3), z - [0,3))
        Returns:  
            List of values from Magic Cube that satisfy magic sum and are collinear with some pair of locations
        """
        pairs = list(itertools.combinations(l,2))
        triplets = []
        for p1, p2 in pairs:
            magic_p1 = self.magic_cube[p1[0]][p1[1]][p1[2]]
            magic_p2 = self.magic_cube[p2[0]][p2[1]][p2[2]]
            diff = self.magic_sum-(magic_p1+magic_p2)
            if 0 < diff < 28:
                triplets.append((magic_p1,magic_p2,diff))
        valid_triplets = [x for x in triplets if len(set(itertools.permutations(x)).intersection(set(self.valid_magic_triplets))) != 0]
        return [x[2] for x in valid_triplets]

    def avail_loc(self) -> list:
        """
        Finds available locations on the 3D board
        Args:  
            None
        Returns:  
            List of available locations on the 3D board
        """
        return list(map(lambda x: x[0]*9+x[1]*3+x[2]+1,[(x,y,z) for x in range(0,3) for y in range(0,3) for z in range(0,3) if self.board[x][y][z] == 0]))

    def X_loc(self) -> list:
        """
        Finds locations of 'X' on the 3D board
        Args:  
            None
        Returns:  
            List of locations of 'X' on the 3D board
        """
        return [(x,y,z) for x in range(0,3) for y in range(0,3) for z in range(0,3) if self.board[x][y][z] == 1]

    def O_loc(self) -> list:
        """
        Finds locations of 'O' on the 3D board
        Args:  
            None
        Returns:  
            List of locations of 'O' on the 3D board
        """
        return [(x,y,z) for x in range(0,3) for y in range(0,3) for z in range(0,3) if self.board[x][y][z] == 2]

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
        X_win_loc_poss = [(x,y,z) for val in X_valid_magic for x in range(0,3) for y in range(0,3) for z in range(0,3) if val == self.magic_cube[x][y][z]]
        X_win_loc = [(x,y,z) for x, y, z in X_win_loc_poss if self.board[x][y][z] == 0]
        O_loc = self.O_loc()
        O_valid_magic = self.magic_loc(O_loc)
        O_win_loc_poss = [(x,y,z) for val in O_valid_magic for x in range(0,3) for y in range(0,3) for z in range(0,3) if val == self.magic_cube[x][y][z]]
        O_win_loc = [(x,y,z) for x, y, z in O_win_loc_poss if self.board[x][y][z] == 0]
        return (X_win_loc,O_win_loc)

    def adjacent_loc(l: list) -> list:
        """
        Lists all possible adjacent locations (in all directions except along body diagonals) of the given point
        Args:  
            l: Coordinates of point to determine adjacent locations
        Returns:  
            List of all possible adjacent locations to given point
        """
        adjacent_loc_x_poss = [(l[0]+x,l[1]+y,l[2]+z) for x in [1,-1] for y, z in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]]
        adjacent_loc_y_poss = [(l[0]+x,l[1]+y,l[2]+z) for y in [1,-1] for z, x in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]]
        adjacent_loc_z_poss = [(l[0]+x,l[1]+y,l[2]+z) for z in [1,-1] for x, y in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]]
        adjacent_loc_poss = set(adjacent_loc_x_poss+adjacent_loc_y_poss+adjacent_loc_z_poss)
        adjacent_loc = [(x,y,z) for x, y, z in adjacent_loc_poss if -1 < x < 3 and -1 < y < 3 and -1 < z < 3]
        return adjacent_loc

    def best_score(self) -> tuple:
        """
        Scoring method to determine which is the best possible move for the bot.  
        This Scoring method includes 5 different types of scores -
        - **Adjacent Score**: Depends on how many face centers, edge centers, corners are around the point
        - **Positional Score**: Depends on where the point is located (face center, edge center or corner)
        - **Point Score**: Scored only if the point is finishing a magic tripet on the magic cube
        - **Finish Score**: Scored only if remaining moves are less than total win locations for the bot and the point is not blocking any opponent's triplet
        - **Win Score**: Depends on number of win locations created and number of lose locations left for future
        Args:  
            None
        Returns:  
            Coordinates of best move location
        """
        avail_loc = [(x,y,z) for x, y, z in tic_tac_toe_3D.all_loc if self.board[x][y][z] == 0]
        comp_val = 1 if self.start_player == 'C' else 2 
        human_val = 1 if self.start_player == 'H' else 2 
        comp_center = self.board[1][1][1] == comp_val
        comp_faces = [(x,y,z) for x, y, z in tic_tac_toe_3D.faces if self.board[x][y][z] == comp_val]
        comp_corners = [(x,y,z) for x, y, z in tic_tac_toe_3D.corners if self.board[x][y][z] == comp_val]
        comp_edges = [(x,y,z) for x, y, z in tic_tac_toe_3D.edges if self.board[x][y][z] == comp_val]
        human_center = self.board[1][1][1] == human_val
        human_faces = [(x,y,z) for x, y, z in tic_tac_toe_3D.faces if self.board[x][y][z] == human_val]
        human_corners = [(x,y,z) for x, y, z in tic_tac_toe_3D.corners if self.board[x][y][z] == human_val]
        human_edges = [(x,y,z) for x, y, z in tic_tac_toe_3D.edges if self.board[x][y][z] == human_val]
        X_win_locations_actual, O_win_locations_actual = self.win_loc()
        win_locations_actual = X_win_locations_actual if self.start_player == 'C' else O_win_locations_actual
        lose_locations_actual = X_win_locations_actual if self.start_player == 'H' else O_win_locations_actual
        loc_score = []
        for a in avail_loc:
            if self.move(9*a[0]+3*a[1]+a[2]+1):
                X_win_locations, O_win_locations = self.win_loc()
                win_locations = X_win_locations if self.start_player == 'C' else O_win_locations
                lose_locations = X_win_locations if self.start_player == 'H' else O_win_locations
                adjacent_loc_set = set(tic_tac_toe_3D.adjacent_loc(a))
                face_score = (25 if comp_center else 23)*(len(adjacent_loc_set.intersection(set(comp_faces))))
                corner_score = 23*(len(adjacent_loc_set.intersection(set(comp_corners))))
                edge_score = 24*(len(adjacent_loc_set.intersection(set(comp_edges))))
                adjacent_score = face_score+corner_score+edge_score
                positional_score = 5 if a in tic_tac_toe_3D.faces else 4 if a in tic_tac_toe_3D.edges else 3
                point_score = 1000*(1 if a in win_locations_actual else 0)
                finish_score = -1000 if (20-self.move_count)//2 <= len(win_locations) and lose_locations >= lose_locations_actual else 0
                win_score = 100*(len(win_locations)-3*len(lose_locations))
                score = win_score+adjacent_score+positional_score+finish_score
                loc_score.append((a,score))
                self.board[a[0]][a[1]][a[2]] = 0
                self.player = 'H' if self.player == 'C' else 'C'
                self.move_count = self.move_count-1
        list.sort(loc_score,key=lambda x: -x[1])
        # _ = [print(x," - ",("Face" if x[0] in tic_tac_toe_3D.faces else "Edge" if x[0] in tic_tac_toe_3D.edges else "Corner")) for x in loc_score]
        print("Best Score = ",loc_score[0])
        return loc_score[0][0]

    def computer_move(self):
        """
        Bot algorithm to make right move
        Args:  
            None
        Returns:  
            Position to place the piece (Valid Positions -> [1-27])
        """
        if(self.player != 'C'):
            return 0
        if(self.move_count == 0):
            return 14
        elif(self.move_count == 1):
            if(self.board[1][1][1] == 0):
                return 14
            else:
                rand_loc = int(random()*6)
                face_centers = [5,11,13,15,17,23]
                return face_centers[rand_loc]
        elif(self.move_count >= 2):
                best_loc = self.best_score()
                return best_loc[0]*9+best_loc[1]*3+best_loc[2]+1

def game():
    play = True
    while(play):
        start = int(not input("\33[94mTo start first Enter 0: \33[0m") == '0')
        piece = 'X' if start == 0 else 'O'
        game = tic_tac_toe_3D(start)
        game.print_board(0)
        extra = int(input("\33[93mFor adding extra triplets that contribute to score, Enter 0: \33[0m") == '0')
        if(extra):
            game.add_extra_triplets()
        while(not game.finished):
            if(game.player == 'H'):
                while(True):
                    try:
                        loc = int(input("\33[93mPlace {0} at location [1,9] \33[92m(Move Number - {1})\33[95m: \33[0m".format(piece,(game.move_count+1))))
                        if(not game.move(loc)):
                            print("\33[91mEnter valid location for {}\33[0m".format(piece))
                        else:
                            break
                    except (TypeError, ValueError):
                        print("\33[91mEnter proper input\33[0m")
                        continue
            else:
                print("\33[95mBot's Turn \33[92m(Move Number - {0})\33[95m: \33[0m".format(game.move_count+1))
                game.move(game.computer_move())
            try:
                loc_print = int(input("\33[93mEnter 0 to view locations on magic cube: \33[0m"))
            except (TypeError, ValueError):
                loc_print = 1
            game.print_board(loc_print)
            game.checkFinish()
        play = not (input("\33[93mEnter q to quit: \33[0m") == 'q')
        os.system("clear")

if __name__ == "__main__":
    try:
        game()
    except (KeyboardInterrupt, EOFError):
        print("\33[91m\nExiting Game\33[0m")
        exit