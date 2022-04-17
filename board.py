board = [
    ['-', '-' , '-'],
    ['-', '-' , '-'],
    ['-', '-' , '-']
]



def set_board(new):
    for row in range(len(new)):
        for col in range(len(new[row])):
            board[row][col] = new[row][col]


def clear_board():
    for row in range(len(board)):
        for col in range(len(board[row])):
            board[row][col] = '-'


def print_board():
    for row in range(len(board)):
        print('#' * (6 * len(board[row]) + 1))
        print(('#' + ' '*5) * len(board[row]) + '#')
        for col in range(len(board[row])):
            print('# ', board[row][col], end='  ')
        print('#')
        print(('#' + ' '*5) * len(board[row]) + '#')
    print('#' * (6 * len(board[row]) + 1))


def get_mark(player_id):
    return ['X', 'O'][player_id - 1]


def check_mark(row, col):
    return board[row][col] == '-'


def place_mark(row, col, player_id):
    board[row][col] = get_mark(player_id)


def check_win(player_id):
    mark = get_mark(player_id)
    # check rows
    for row in board:
        if all(m == mark for m in row):
            return True
    # check columns
    for col in range(len(board[0])):
        if all(row[col] == mark for row in board):
            return True
    # check diagonals
    if all(m == mark for m in [board[i][i] for i in range(min(len(board), len(board[0])))]):
        return True 
    if all(m == mark for m in [board[i][len(board[0])-1-i] for i in range(len(board))]):
        return True
    return False


def main():
    print('print_board():')
    print_board()
    
    print('\ncheck_mark():')
    print(check_mark(0, 0) == True)
    place_mark(0, 0, 1)
    print(check_mark(0, 0) == False)
    place_mark(0, 0, 2)
    print(check_mark(0, 0) == False)
    clear_board()

    print('\nplace_mark():')
    place_mark(0, 0, 1)
    print(board[0][0] == 'X')
    place_mark(0, 0, 2)
    print(board[0][0] == 'O')
    clear_board()

    print('\ncheck_win')
    print(check_win(1) == False and check_win(2) == False)
    set_board([
        ['X', 'X', 'X'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ])
    print(check_win(1) == True)
    set_board([
        ['X', '-', '-'],
        ['X', '-', '-'],
        ['X', '-', '-']
    ])
    print(check_win(1) == True)
    set_board([
        ['X', '-', '-'],
        ['-', 'X', '-'],
        ['-', '-', 'X']
    ])
    print(check_win(1) == True)
    



if __name__ == '__main__':
    main()