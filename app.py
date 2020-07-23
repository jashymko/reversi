"""
- Skip turn if no moves can be made
    - End game if neither player can make a move
- Fix your hardcoding
"""

import pygame

WIDTH = 540
HEIGHT = 540
P_COLORS = (None, (0, 0, 0), (255, 255, 255))

grid = [[0] * 8 for _ in range(8)]
turn = 1    #1 & 2
mouse_held = False
overlapping_moves = []


def init_game():
    global screen, possible_moves

    pygame.init()
    pygame.display.set_caption("Reversi")
    pygame.display.set_icon(pygame.image.load("icon.png"))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    grid[3][3], grid[3][4], grid[4][3], grid[4][4] = 2, 1, 1, 2

    possible_moves = find_moves()

    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        handle_events()
        draw_all()


def opp():
    return 3 - turn


def scan(opp_row, opp_column, direction):
    row_change, column_change = direction[0], direction[1]
    row, column = opp_row + row_change, opp_column + column_change

    opp_found = False
    while 0 <= row <= 7 and 0 <= column <= 7:   # Search in given direction for valid move
        if grid[row][column] == turn:
            break
        elif grid[row][column] == 0 and not opp_found:
            break
        elif grid[row][column] == 0 and opp_found:
            return ((column, row), direction)
        elif grid[row][column] == opp():
            opp_found = True
        row += row_change
        column += column_change
    return

def find_moves():
    possible_moves = []
    for row in range(8):
        for column in range(8):
            if grid[row][column] == turn:
                dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))   # Check every direction on each of player's pieces for potential connection
                for direction in dirs:
                    move = scan(row, column, direction)
                    if move:
                        possible_moves.append(move)
    return possible_moves


def change_turn():
    global overlapping_moves, turn, possible_moves
    overlapping_moves = []
    turn = opp()
    possible_moves = find_moves()


def handle_events():
    import time
    global grid, mouse_held, possible_moves, overlapping_moves, turn

    # Mouse Events, turn action on mouseup
    pressed = False
    for button in pygame.mouse.get_pressed():
        if button:
            pressed = True
    if pressed and not mouse_held:
        mouse_held = True
    elif mouse_held and not pressed:    # Mouseup
        mouse_held = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = 8*mouse_x // WIDTH
        mouse_y = 8*mouse_y // HEIGHT
        possible_moves = find_moves()
        for move in possible_moves:
            if move[0] == (mouse_x, mouse_y):
                overlapping_moves.append(move)  # Find move(s) in possible_moves,
        for move in overlapping_moves:          # fill in cells with player's chips
            row_change, column_change = move[1][0], move[1][1]
            column, row = mouse_x, mouse_y
            while grid[row][column] != turn:
                grid[row][column] = turn
                row -= row_change
                column -= column_change
            grid[mouse_y][mouse_x] = 0
        if overlapping_moves:
            grid[mouse_y][mouse_x] = turn
            change_turn()
        elif not possible_moves:    # Skip turn on click if no moves are possible
            change_turn()


def draw_all():
    # Draw Board
    pygame.draw.rect(screen, (0, 128, 0), (0, 0, WIDTH, HEIGHT))
    for i in range(9):
        pygame.draw.line(screen, (0, 0, 0), (i * WIDTH/8, 0), (i * WIDTH/8, HEIGHT))
        pygame.draw.line(screen, (0, 0, 0), (0, i * HEIGHT/8), (WIDTH, i * HEIGHT/8))

    # Draw Disks
    for row in range(8):
        for column in range(8):
            cell = grid[row][column]
            if cell:
                pygame.draw.circle(screen, P_COLORS[cell], (int((column + 0.5) * WIDTH/8), int((row + 0.5) * HEIGHT/8)), min(WIDTH, HEIGHT)/16 - 2)

    #Draw Move Markers
    for move in possible_moves:
        column, row = move[0]
        pygame.draw.circle(screen, P_COLORS[turn], (int((column + 0.5) * WIDTH/8), int((row + 0.5) * HEIGHT/8)), min(WIDTH, HEIGHT)/128)

    pygame.display.update()

init_game()