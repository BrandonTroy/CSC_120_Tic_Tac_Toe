import os, sqlite3, json, datetime


# globals
board = [
    ['-', '-' , '-'],
    ['-', '-' , '-'],
    ['-', '-' , '-']
]
datetime_format = "%m/%d/%y %I:%M %p"


# functions
def set_board(new):
    """Update the global board to a new 2d array"""
    for row in range(len(new)):
        for col in range(len(new[row])):
            board[row][col] = new[row][col]


def clear_board():
    """Resets all elements of board to '-'"""
    for row in range(len(board)):
        for col in range(len(board[row])):
            board[row][col] = '-'


def print_board(board=board):
    """Displays a board"""
    for row in range(len(board)):
        print('#' * (6 * len(board[row]) + 1))
        print(('#' + ' '*5) * len(board[row]) + '#')
        for col in range(len(board[row])):
            print('# ', board[row][col], end='  ')
        print('#')
        print(('#' + ' '*5) * len(board[row]) + '#')
    print('#' * (6 * len(board[row]) + 1))


def get_mark(player_id):
    """Gets the player's mark from their id"""
    return ['X', 'O'][player_id - 1]


def check_mark(row, col):
    """Returns true if element at index row,col of board contains '-'"""
    return board[row][col] == '-'


def place_mark(row, col, player_id):
    """Sets the element at the row and column index of board to the mark of that player"""
    board[row][col] = get_mark(player_id)


def check_win(player_id):
    """Returns true if the player with the given id has 3 in a row of their mark"""
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


def test():
    """Unit tests for core gameplay functionality"""    
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


def play():
    """Plays a game of tic tac toe, returns results (winner, board)"""
    os.system('cls')
    print("How To Play:\n")
    print("Each player takes turns playing their piece with the goal of getting 3 in-a-row in any direction.")
    print("The board is numbered from left to right, with the top-left square being 1 and the bottom right being 9.")
    print("When you make a turn, the chosen square must not already be occupied by an X or an O.")
    
    clear_board()

    turn = 0
    player_id = 1
    winner = 0
    while True:
        print('\n')
        print_board()
        if turn == 9:
            print("It's a tie!")
            break
        print(f"Player #{player_id}: '{get_mark(player_id)}'")
        while True:
            try:
                choice = int(input("Your choice (1-9): "))
            except ValueError:
                print("[ERROR]: You must enter a valid number!")
                continue
            if not 1 <= choice <= 9:
                print("[ERROR]: Your selection must be between 1 and 9!")
                continue
            choice -= 1   # convert to index
            row, col = choice // 3, choice % 3
            if not check_mark(row, col):
                print("[ERROR]: That tile is already occupied!")
                continue
            break
        place_mark(row, col, player_id)
        if check_win(player_id):
            print('\n')
            print_board()
            print(f"Player #{player_id} wins!")
            winner = player_id
            break
        
        turn += 1
        player_id = 2 if player_id == 1 else 1
    
    input("\nPress [ENTER] to continue")
    return winner, board


def display_records():
    """fetches records from database file and displays them"""
    os.system('cls')
    connection = sqlite3.connect('records.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    connection.close()

    for (id, time, duration, winner, board) in games:
        print(f"Game #{id + 1}")
        print_board(json.loads(board))
        print(f"Outcome: {f'Player {winner}' if winner != 0 else 'DRAW'}")
        print("Time:", time)
        print("Duration:", duration, "seconds")
        print('\n')

    input("\nPress [ENTER] to return to menu")


def main():
    # connnect to database
    connection = sqlite3.connect('records.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS games 
                    (id INT PRIMARY KEY NOT NULL, time TEXT, duration INT, winner INT, board TEXT)''')
    cursor.execute("SELECT * FROM games")
    current_id = len(cursor.fetchall())
    
    # game loop
    while True:
        os.system('cls')
        print_board([list("TIC"), list("TAC"), list("TOE")])
        print("Input the number of an option below to select it.\n")
        print("[1] Play")
        print("[2] View Game History")
        print("[3] Quit")
        
        choice = input("\n>> ")
        if choice == '1':
            start = datetime.datetime.now()
            winner, board = play()
            duration = datetime.datetime.now() - start
            cursor.execute(f"INSERT INTO games VALUES ({current_id}, '{start.strftime(datetime_format)}', {duration.seconds}, {winner}, '{json.dumps(board)}')")
            connection.commit()
            current_id += 1
        elif choice == '2':
            display_records()
        elif choice == '3':
            print("\nThanks for playing!")
            break
        
    connection.close()



if __name__ == '__main__':
    main()