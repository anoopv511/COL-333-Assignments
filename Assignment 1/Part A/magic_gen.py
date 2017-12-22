import itertools

def print_2D(l: list) -> None:
    """
    Print 2D list
    Args:  
        l: 2D list
    Returns:  
        None
    """
    _ = [print(r) for r in l]
    return

def validate_magic_square(l: list) -> bool:
    """
    Validates Magic Square based on standard Magic Square rules
    Args:  
        l: Magic Square to be validated
    Returns:  
        Valid Magic Sqaure Flag. True for Valid. False otherwise
    """
    valid = True
    size = len(l)
    size_check = [isinstance(l[x],list) and len(l[x]) == size for x in range(0,size)]
    if(sum(size_check) != size):
        print("\33[91mImproper sized Magic Square\33[0m\n-----------")
        print_2D(l)
        print("-----------")
        return False
    magic_sum = int(size*(size**2+1)/2)
    row_sum = [sum(l[x]) for x in range(0,size)]
    if(sum([magic_sum == row_sum[x] for x in range(0,size)]) != size):
        print("\33[91mAll rows don't have Magic Sum ({})\33[0m".format(magic_sum))
        print(row_sum)
        valid = False
    col_sum = [sum([l[x][y] for x in range(0,size)]) for y in range(0,size)]
    if(sum([magic_sum == col_sum[x] for x in range(0,size)]) != size):
        print("\33[91mAll columns don't have Magic Sum ({})\33[0m".format(magic_sum))
        print(col_sum)
        valid = False
    diag_1_sum = sum([l[x][x] for x in range(0,size)])
    diag_2_sum = sum([l[size-1-x][x] for x in range(0,size)])
    if(magic_sum != diag_1_sum):
        print("\33[91mDiagonal sum ({}) starting from top left is not equal to Magic Sum ({})\33[0m".format(diag_1_sum,magic_sum))
        valid = False
    if(magic_sum != diag_2_sum):
        print("\33[91mDiagonal sum ({}) starting from top right is not equal to Magic Sum ({})\33[0m".format(diag_2_sum,magic_sum))
        valid = False
    return valid

def double_even(n: int) -> list:
    """
    Magic Square for sizes divisible by 4
    Args:  
        n: Size of Magic Square (divisible by 4)
    Returns:  
        2D list obeying Magic Square Rules
    """
    square = []
    for x in range(1,n+1):
        square.append([])
        for y in range(0,n):
            if(y < n/2):
                square[x-1].append(n*y+x)
            else:
                square[x-1].append(n*y+n+1-x)
    def swap(r: list,order=0) -> None:
        for x in range(0,int(n/2)):
            if(r[x]%2 == order%2):
                r[x], r[n-1-x] = r[n-1-x], r[x]
    _ = [swap(square[x],int(x >= n/2)) for x in range(0,n)]
    square[n-1][int(n/2-1)], square[int(n/2)][int(n/2-1)] = square[int(n/2)][int(n/2-1)], square[n-1][int(n/2-1)]
    square[n-1][int(n/2)], square[int(n/2)][int(n/2)] = square[int(n/2)][int(n/2)], square[n-1][int(n/2)]
    return square

def single_even(n: int) -> list:
    """
    Magic Square for sizes divisible by 2 but not by 4
    Args:  
        n: Size (> 2) of Magic Square (divisible by 2 but not by 4 )
    Returns:  
        2D list obeying Magic Square Rules
    """
    square = []
    for x in range(1,n-1):
        square.append([])
        for y in range(0,n):
            if(y < n/2):
                square[x-1].append((n-2)*y+x)
            else:
                square[x-1].append(n*y+n+1-x+(n-1-y)*2)
    def swap(r: list,order=0) -> None:
        for x in range(0,int(n/2)):
            if(r[x]%2 == order%2):
                r[x], r[n-1-x] = r[n-1-x], r[x]
    _ = [swap(square[x],int(x >= n/2-1)) for x in range(0,n-2)]
    square.extend([[],[]])
    for x in range(int(n/2),n):
        square[int(n/2-1)], square[x] = square[x], square[int(n/2-1)]
    for x in range(int(n/2),n):
        square[int(n/2-1)], square[x] = square[x], square[int(n/2-1)]
    square[int(n/2-1)] = [int((n/2+1)*n-x) for x in range(0,int(n/2))]
    square[int(n/2-1)].extend([int((n/2-1)*n+x) for x in range(n,int(n/2),-1)])
    square[int(n/2)] = [int((n/2-1)*n+x) for x in range(1,int(n/2+1))]
    square[int(n/2)].extend([int((n/2+1)*n-x) for x in range(n-1,int(n/2-1),-1)])
    for x in range(1,int(n/2),2):
        square[int(n/2-1)][x], square[int(n/2)][x] = square[int(n/2)][x], square[int(n/2-1)][x],
    for x in range(int(n/2+2),n-2,2):
        square[int(n/2-1)][x], square[int(n/2)][x] = square[int(n/2)][x], square[int(n/2-1)][x],
    square[int(n/2-2)][int(n/2-2)], square[int(n/2+1)][int(n/2-2)] = square[int(n/2+1)][int(n/2-2)], square[int(n/2-2)][int(n/2-2)]
    square[int(n/2-2)][int(n/2+1)], square[int(n/2+1)][int(n/2+1)] = square[int(n/2+1)][int(n/2+1)], square[int(n/2-2)][int(n/2+1)]
    return square

def odd(n: int) -> list:
    """
    Magic Square for odd sizes
    Args:  
        n: Size (> 1) of Magic Square (odd)
    Returns:   
        2D list obeying Magic Square Rules
    """
    square = [[0 for y in range(0,n)] for x in range(0,n)]
    y = n//2
    x = n-1
    for i in range(1,n**2+1):
        square[x][y] = i
        n_x = x+1 if x < n-1 else 0
        n_y = y+1 if y < n-1 else 0
        if(square[n_x][n_y] != 0):
            n_x = x-1 if x > 0 else n-1
            n_y = y
        x = n_x
        y = n_y
    return square

def magic_square_algo(n: int) -> list:
    """
    Magic Square for given size
    Args:  
        n: Size of Magic Square
    Returns:  
        2D list obeying Magic Square Rules
    """
    if(n == 2 or n < 1):
        print("\33[91mMagic Square with order {} does not exist\33[0m".format(n))
        return []
    if(n%2 == 1):
        return odd(n)
    elif(n%4 == 2):
        return single_even(n)
    elif(n%4 == 0):
        return double_even(n)

def magic_sum_set_split(n: int) -> list:
    """
    Splits all possible combinations of n numbers from [1,n**2] which add upto magic sum of magic square of order n into collinear set and non-collinear set with respect to magic square of order n
    Args:  
        n: Order of Magic Square (Do not set n >= 7 because the size of non-collinear points grows very fast and takes up lot of memory (> 6 GB))
    Returns:  
        Tuple of collinear and non-collinear points lists
    """
    square = magic_square_algo(n)
    if n > 6:
        print("\33[91mFor n greater than 6, memory usage is greater 6 GB and takes time for evaluation. \nNot evaluating\33[0m")
        return []
    n_tuple_list = list(itertools.combinations([x for x in range(1,n**2+1)],n))
    sum_n_tuple_list = [sum(x) for x in n_tuple_list]
    magic_sum = int(n*(n**2+1)/2)
    magic_sum_set = set([n_tuple_list[x] for x in range(0,len(n_tuple_list)) if sum_n_tuple_list[x] == magic_sum])
    collinear_magic_sum_set = set()
    collinear_magic_sum_set.update([tuple(square[x]) for x in range(0,n)])
    collinear_magic_sum_set.update([tuple(square[x][y] for x in range(0,n)) for y in range(0,n)])
    collinear_magic_sum_set.add(tuple(square[x][x] for x in range(0,n)))
    collinear_magic_sum_set.add(tuple(square[n-1-x][x] for x in range(0,n)))
    non_collinear_magic_sum_list = [x for x in magic_sum_set if len(set(itertools.permutations(x)).intersection(collinear_magic_sum_set)) == 0]
    return collinear_magic_sum_set, non_collinear_magic_sum_list

if __name__ == "__main__":
    bye = False
    while(not bye):
        n = int(input("\33[94mEnter order of Magic Square to be printed: \33[0m"))
        print_2D(magic_square_algo(n))
        bye = input("\33[93mEnter q to quit: \33[0m") == 'q'