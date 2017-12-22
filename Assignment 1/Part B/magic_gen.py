import os
import itertools

def print_3D(l: list):
    """
    Print surfaces of 3D Cube - 11 surfaces (3 Top View, 3 Front View, 3 Left Side View, 2 Diagonal Planes - One along NW Normal and the other along NE Normal)
    Args:  
        l: 3D list - Assumed to be a Cube (No checks have been implemented)
    Returns:  
        None
    """
    size = len(l)
    print("\n\33[92mTop View\33[0m\n")
    _ = [print("\33[95mLayer {}\t\t\33[0m".format(x), end="{0}".format("\t" if x != size else "\n\n")) for x in range(1,size+1)]
    _ = [print(l[x][y][z], end="{}".format(", " if z != size-1 else " \t|\t " if x != size-1 else "\n")) for y in range(0,size) for x in range(0,size) for z in range(0,size)]
    print("\n\33[92mFront View\33[0m\n")
    _ = [print("\33[95mLayer {}\t\t\33[0m".format(x), end="{}".format("\t" if x != size else "\n\n")) for x in range(1,size+1)]
    _ = [print(l[x][y][z], end="{}".format(", " if z != size-1 else " \t|\t " if y != 0 else "\n")) for x in range(0,size) for y in range(size-1,-1,-1) for z in range(0,size)]
    print("\n\33[92mLeft Side View\33[0m\n")
    _ = [print("\33[95mLayer {}\t\t\33[0m".format(x), end="{}".format("\t" if x != size else "\n\n")) for x in range(1,size+1)]
    _ = [print(l[x][y][z], end="{}".format(", " if y != size-1 else " \t|\t " if z != size-1 else "\n")) for x in range(0,size) for z in range(0,size) for y in range(0,size)]
    print("\n\33[92mDiagonal_1 View\33[0m\n")
    _ = [print(l[x][y][z], end="{}".format(", " if z != size-1 else "\n")) for x in range(0,size) for y,z in zip(range(size-1,-1,-1),range(0,size))]
    print("\n\33[92mDiagonal_2 View\33[0m\n")
    _ = [print(l[x][y][z], end="{}".format(", " if z != size-1 else "\n")) for x in range(0,size) for y,z in zip(range(0,size),range(0,size))]
    print()
    return

def validate_magic_cube(l: list) -> bool:
    """
    Validates Magic Cube based on standard Magic Cube rules
    Args:  
        l: Magic Cube to be validated
    Returns:  
        Valid Magic Cube Flag. True for Valid. False otherwise
    """
    valid = True
    size = len(l)
    size_check = [isinstance(l[x],list) and isinstance(l[x][y],list) and len(l[x]) == size and len(l[x][y]) == size for x in range(0,size) for y in range(0,size)]
    if(sum(size_check) != size*size):
        print("\33[91mImproper sized Magic Cube\033[0m\n-----------")
        print_2D(l)
        print("-----------")
        return False
    magic_sum = int(size*(size**3+1)/2)
    row_sum = list(map(lambda c: sum(l[c[0]][c[1]][z] for z in range(0,size)),[(x,y) for x in range(0,size) for y in range(0,size)]))
    if(sum([magic_sum == row_sum[x] for x in range(0,size*size)]) != size*size):
        print("\33[91mAll rows don't have Magic Sum ({})\33[0m".format(magic_sum))
        print(row_sum," - Row Sum according to Left Side View of Cube")
        valid = False
    col_sum = list(map(lambda c: sum(l[c[0]][y][c[1]] for y in range(0,size)),[(x,z) for x in range(0,size) for z in range(0,size)]))
    if(sum([magic_sum == col_sum[x] for x in range(0,size*size)]) != size*size):
        print("\33[91mAll columns don't have Magic Sum ({})\33[0m".format(magic_sum))
        print(row_sum," - Column Sum according to Front View of Cube")
        valid = False
    ht_sum = list(map(lambda c: sum(l[x][c[0]][c[1]] for x in range(0,size)),[(y,z) for y in range(0,size) for z in range(0,size)]))
    if(sum([magic_sum == ht_sum[x] for x in range(0,size*size)]) != size*size):
        print("\33[91mAll pillars don't have Magic Sum ({})\33[0m".format(magic_sum))
        print(row_sum," - Pillar Sum according to Top View of Cube")
        valid = False
    diag_1_sum = sum(l[x][size-1-x][x] for x in range(0,size))
    diag_2_sum = sum(l[x][x][size-1-x] for x in range(0,size))
    diag_3_sum = sum(l[x][x][x] for x in range(0,size))
    diag_4_sum = sum(l[size-1-x][x][x] for x in range(0,size))
    if(magic_sum != diag_1_sum):
        print("\33[91mDiagonal sum ({}) starting from top left on NW Normal View (Diagonal_1 View) is not equal to Magic Sum ({})\33[0m".format(diag_1_sum,magic_sum))
        valid = False
    if(magic_sum != diag_2_sum):
        print("\33[91mDiagonal sum ({}) starting from top right on NW Normal View (Diagonal_1 View) is not equal to Magic Sum ({})\33[0m".format(diag_2_sum,magic_sum))
        valid = False
    if(magic_sum != diag_3_sum):
        print("\33[91mDiagonal sum ({}) starting from top left on NE Normal View (Diagonal_2 View) is not equal to Magic Sum ({})\33[0m".format(diag_3_sum,magic_sum))
        valid = False
    if(magic_sum != diag_4_sum):
        print("\33[91mDiagonal sum ({}) starting from top right on NE Normal View (Diagonal_2 View) is not equal to Magic Sum ({})\33[0m".format(diag_4_sum,magic_sum))
        valid = False
    return valid

def double_even(n: int) -> list:
    """
    Magic Cube for sizes divisible by 4
    Args:  
        n: Size of Magic Cube (divisible by 4)
    Returns:  
        3D list obeying Magic Cube Rules
    """
    bar = lambda x: n+1-x
    star = lambda x: min(x,bar(x,n))
    tilda = lambda x: 0 if 1 <= x <= n/2 else 1
    cube = [[[int((x-1)*n**2+(y-1)*n+z) if (x+y+z+tilda(x)+tilda(y)+tilda(z))%2 == 1 else int((bar(x)-1)*n**2+(bar(y)-1)*n+bar(z)) for z in range(1,n+1)] for y in range(1,n+1)] for x in range(1,n+1)]
    return cube

def single_even(n: int) -> list:
    """
    Magic Cube for sizes divisible by 2 but not by 4
    Args:  
        n: Size (> 2) of Magic Cube (divisible by 2 but not by 4 )
    Returns:  
        3D list obeying Magic Cube Rules
    """
    bar = lambda x: n+1-x
    star = lambda x: min(x,bar(x))
    tilda = lambda x: 0 if 1 <= x <= n/2 else 1
    t = int(n/2)
    u = lambda x,y,z: int((star(x)-star(y)+star(z))%t+1)
    v = lambda x,y,z: int(4*tilda(x)+2*tilda(y)+tilda(z)+1)
    d = [[7,3,6,2,5,1,4,0],[3,7,2,6,1,5,0,4],[0,1,3,2,5,4,6,7],[0,1,2,3,4,5,6,7],[7,6,5,4,3,2,1,0]]
    d_op = lambda a,b: d[0][b-1] if a == 1 else d[1][b-1] if a == 2 else d[2][b-1] if a == 3 else d[3][b-1] if 4 <= a <= t and  a%2 == 0 else d[4][b-1] if 4 <= a <= t and a%2 == 1 else 0
    m_t = odd(t)
    m_n = lambda x,y,z: int(m_t[star(x)-1][star(y)-1][star(z)-1]+d_op(u(x,y,z),v(x,y,z))*t**3)
    cube = [[[m_n(x,y,z) for z in range(1,n+1)] for y in range(1,n+1)] for x in range(1,n+1)]
    return cube

def odd(n: int) -> list:
    """
    Magic Cube for odd sizes
    Args:  
        n: Size (> 1) of Magic Cube (odd)
    Returns:   
        3D list obeying Magic Cube Rules
    """
    cube = [[[int((x-y+z-1)%n*n**2+(x-y-z)%n*n+(x+y+z-2)%n+1) for z in range(1,n+1)] for y in range(1,n+1)] for x in range(1,n+1)]
    return cube

def magic_cube_algo(n: int) -> list:
    """
    Magic Cube for given size
    Args:  
        n: Size of Magic Cube
    Returns:  
        3D list obeying Magic Cube Rules
    """
    if(n == 2 or n < 1):
        print("\33[91mMagic Cube with order {} does not exist\33[0m".format(n))
        return []
    if(n%2 == 1):
        return odd(n)
    elif(n%4 == 2):
        return single_even(n)
    elif(n%4 == 0):
        return double_even(n)

def magic_sum_set_split(n: int) -> list:
    """
    Splits all possible combinations of n numbers from [1,n**3] which add upto magic sum of magic cube of order n into collinear set and non-collinear set with respect to surfaces of magic cube of order n
    Args:  
        n: Order of Magic Cube (Do not set n >= 5 because the size of non-collinear points grows very fast and takes up lot of memory (> 6 GB))
    Returns:  
        Tuple of collinear and non-collinear points lists
    """
    cube = magic_cube_algo(n)
    if n > 4:
        print("\33[91mFor n greater than 4, memory usage is greater 6 GB and takes time for evaluation. \nNot evaluating\33[0m")
        return []
    n_tuple_list = list(itertools.combinations([x for x in range(1,n**3+1)],n))
    sum_n_tuple_list = [sum(x) for x in n_tuple_list]
    magic_sum = int(n*(n**3+1)/2)
    magic_sum_set = set([n_tuple_list[x] for x in range(0,len(n_tuple_list)) if sum_n_tuple_list[x] == magic_sum])
    collinear_magic_sum_set = set()
    collinear_magic_sum_set.update(list(map(lambda c: tuple(cube[c[0]][c[1]][z] for z in range(0,n)),[(x,y) for x in range(0,n) for y in range(0,n)])))
    collinear_magic_sum_set.update(list(map(lambda c: tuple(cube[c[0]][y][c[1]] for y in range(0,n)),[(x,z) for x in range(0,n) for z in range(0,n)])))
    collinear_magic_sum_set.update(list(map(lambda c: tuple(cube[x][c[0]][c[1]] for x in range(0,n)),[(y,z) for y in range(0,n) for z in range(0,n)])))
    collinear_magic_sum_set.update(list(tuple(cube[a][x][x] for x in range(0,3)) for a in range(0,3)))
    collinear_magic_sum_set.update(list(tuple(cube[a][n-1-x][x] for x in range(0,3)) for a in range(0,3)))
    collinear_magic_sum_set.update(list(tuple(cube[x][a][x] for x in range(0,3)) for a in range(0,3)))
    collinear_magic_sum_set.update(list(tuple(cube[x][a][n-1-x] for x in range(0,3)) for a in range(0,3)))
    collinear_magic_sum_set.update(list(tuple(cube[x][x][a] for x in range(0,3)) for a in range(0,3)))
    collinear_magic_sum_set.update(list(tuple(cube[n-1-x][x][a] for x in range(0,3)) for a in range(0,3)))
    collinear_magic_sum_set.add(tuple(cube[x][n-1-x][x] for x in range(0,n)))
    collinear_magic_sum_set.add(tuple(cube[x][x][n-1-x] for x in range(0,n)))
    collinear_magic_sum_set.add(tuple(cube[x][x][x] for x in range(0,n)))
    collinear_magic_sum_set.add(tuple(cube[n-1-x][x][x] for x in range(0,n)))
    non_collinear_magic_sum_list = [x for x in magic_sum_set if len(set(itertools.permutations(x)).intersection(collinear_magic_sum_set)) == 0]
    return collinear_magic_sum_set, non_collinear_magic_sum_list

if __name__ == "__main__":
    bye = False
    while(not bye):
        os.system("clear")
        n = int(input("\33[94mEnter order of Magic Cube to be printed: \33[0m"))
        print_3D(magic_cube_algo(n))
        bye = input("\33[93mEnter q to quit: \33[0m") == 'q'
