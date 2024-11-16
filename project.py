#BATTLESHIP
from enum import Enum
import re
from time import sleep
TIMEDELAY = 2.0 # delay in seconds
NUMSPACES = 15

def main():
    #by changing this enum, we can change the number of ships on the board
    class ships(Enum):
        __order__ = "CARRIER BATTLESHIP FRIGATE SUBMARINE PATROL_BOAT"

        #name - size
        CARRIER=5
        BATTLESHIP=4
        FRIGATE=3
        SUBMARINE=3
        PATROL_BOAT=2

    #HEALTH SETUP
    #hitting the ship will minus off from the health
    p1health = {}
    for ship in ships: p1health[ship.name] = ship.value
    p2health = {}
    for ship in ships: p2health[ship.name] = ship.value

    #SHIP COORD TRACKER
    p1tracker = {}
    p2tracker = {}

    #BOARD SETUP
    p1board = [ [None for _ in range(10)] for _ in range(10)]
    p2board = [ [None for _ in range(10)] for _ in range(10)]

    #SHIP SETUP
    setup(p1board, ships, p1tracker)
    print_separator()
    setup(p2board, ships, p2tracker)
    print_separator()

    #GAMEPLAY LOOP
    winner = 0
    while not winner:
        if turn(p2board, p2health, p2tracker): winner = 1
        if winner: break
        print_separator(True)
        if turn(p1board, p1health, p1tracker): winner = 2
        print_separator(True)

    print(f'Player {winner} wins!')

def print_separator(delay=False):
    if delay: sleep(TIMEDELAY)
    print("\n"*NUMSPACES)

def print_board(board, reveal=False):

    print('\n',end='   ')
    for i in range(65,75): print(chr(i), end=' ')
    print()

    for r in range(9):
        print(str(r+1), end='  ')
        for c in range(10):
            if board[r][c] in ('O','X','#'): print(board[r][c], end=' ')
            elif board[r][c] is not None and reveal: print(board[r][c][0], end=' ') #ship
            else: print('-', end=' ')
        print()

    print("10", end=' ')
    r = 9
    for c in range(10):
        if board[r][c] == 'O' or board[r][c] == 'X': print(board[r][c], end=' ')
        elif board[r][c] is not None and reveal: print(board[r][c][0], end=' ') #ship
        else: print('-', end=' ')
    print()


def get_coords(shipclass, size):
    valid = False
    while not valid:

        #ask for coords and remove spaces
        ask = input(f'Enter coordinates for your {shipclass} (size: {size}): ').upper().replace(' ','')

        if not re.match(r'^[A-J]([1-9]|10),[A-J]([1-9]|10)$', ask): print('Please follow this format: A5, E5\n')
        else:
            #validate coords
            # - coords give a straight line
            # - coords conform to ship size
            coord1,coord2 = ask.split(',')

            x1 = ord(coord1[0]) - 65
            x2 = ord(coord2[0]) - 65
            y1 = int(coord1[1:]) - 1
            y2 = int(coord2[1:]) - 1
            is_horizontal = y1==y2

            if x1>x2: x1,x2 = x2,x1
            if y1>y2: y1,y2 = y2,y1

            if not (x1==x2 or is_horizontal):
                #not straight line
                print('Please place your ship on a straight line!\n')

            elif is_horizontal:
                if x2-x1 + 1 == size: valid = True
                else: print(f'Your {shipclass} is {size} tiles long\n')

            else: #is vertical
                if y2-y1 + 1 == size: valid = True
                else: print(f'Your {shipclass} is {size} tiles long\n')

    return x1,y1,x2,y2,is_horizontal

def setup(board, ships, tracker):
    for ship in ships:
        print_board(board, True)
        valid = False
        while not valid:
            print('Coordinate format: <column letter><row number>, <column letter><row number>')
            x1, y1, x2, y2, is_horizontal = get_coords(ship.name, ship.value)
            valid = True
            if is_horizontal:
                for xi in range(x1, x2+1):
                    if board[y1][xi] is not None:
                        valid = False
                        print('Another ship has occupied this spot!')
                        break
            else:
                for yi in range(y1, y2+1):
                    if board[yi][x1] is not None:
                        valid = False
                        print('Another ship has occupied this spot!')
                        break

        #at this point in the code the coordinates are valid
        place_ships(board, ship.name, x1, y1, x2, y2, is_horizontal, tracker)

def place_ships(board, shipclass, x1, y1, x2, y2, is_horizontal, tracker):
    tracker[shipclass] = []
    if is_horizontal: # y1 == y2
            for xi in range(x1, x2+1):
                board[y1][xi] = shipclass
                tracker[shipclass].append((xi, y1))

    else: # x1 == x2
        for yi in range(y1, y2+1):
            board[yi][x1] = shipclass
            tracker[shipclass].append((x1, yi))

def get_coord():
    while True:
        try:
            target = input("Choose your target: ").upper()
            if not re.match(r"^[A-J](10|[1-9])$", target):
                raise ValueError("Target must be in the format: (row letter)(column number)")
            row = ord(target[0]) - ord("A")
            column = int(target[1:]) - 1
            return row, column
            # break
        except ValueError:
            print("Target must be in the format: (row letter)(column number)")

def turn(board, health, tracker):
    print_board(board)
    valid = False
    while not valid:
        #ask for grid square, check if chosen grid square is alr attacked
        x, y = get_coord()
        if board[y][x] not in ('X','O', '#'): valid = True
        else: print('You have already attacked this square! Choose another target.\n')

    if board[y][x] is None:
        print("Miss!")
        board[y][x] = 'O'
        return False

    else:
        shipclass = board[y][x]
        board[y][x] = 'X'

        health[shipclass] -= 1
        if health[shipclass] == 0:
            del health[shipclass]
            print(f'You have destroyed the enemy {shipclass.lower()}!')

            # set all tiles of that ship to # to indicate that it has blown up
            for shipx, shipy in tracker[shipclass]: board[shipy][shipx] = '#'
            del tracker[shipclass]

        else: print(f'You have hit the enemy {shipclass.lower()}!')

    #game end check
    return False if health else True

if __name__ == '__main__': main()
