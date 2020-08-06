"""
- Minimax
- Make it look pretty
"""
import pygame
from reversi import Reversi
from minimax import Minimax

#          BG Color,    P1 Color,    P2 Color,    Outline Color
COLORS = ((0, 128, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0))
WIDTH, HEIGHT = (540, 540)

################################################################

game = Reversi()
minimax = Minimax()

screen = None
mouse_held = False


def init_game():
    global screen

    pygame.init()
    pygame.display.set_caption("Reversi")
    pygame.display.set_icon(pygame.image.load("icons/icon.png"))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        handle_events()
        draw_all()


def handle_events():
    global mouse_held

    # Mouse Events, make move on mouseup
    pressed = False
    for button in pygame.mouse.get_pressed():
        if button:
            pressed = True

    if pressed and not mouse_held:
        mouse_held = True

    elif mouse_held and not pressed:    # Mouseup, change to < elif True > for auto-run
        mouse_held = False
        if game.turn == game.P_TURN:
            random_turn()
            # user_turn()
        else:
            minimax_turn()


def draw_all():
    # Draw Board
    pygame.draw.rect(screen, COLORS[0], (0, 0, WIDTH, HEIGHT))
    for i in range(9):
        pygame.draw.line(screen, COLORS[3], (i * WIDTH/game.GRID_W, 0), (i * WIDTH/game.GRID_W, HEIGHT))
        pygame.draw.line(screen, COLORS[3], (0, i * HEIGHT/game.GRID_W), (WIDTH, i * HEIGHT/game.GRID_W))

    # Draw Disks
    for row in range(game.GRID_W):
        for column in range(game.GRID_W):
            cell = game.grid[row][column]
            if cell:
                pygame.draw.circle(screen, COLORS[cell], (int((column + 0.5) * WIDTH/game.GRID_W), int((row + 0.5) * HEIGHT/game.GRID_W)), min(WIDTH, HEIGHT)/(2*game.GRID_W) - 2)

    # Draw Markers
    for move in game.find_moves(game.grid, game.turn):
        column, row = move[0]
        pygame.draw.circle(screen, COLORS[game.turn], (int((column + 0.5) * WIDTH/game.GRID_W), int((row + 0.5) * HEIGHT/game.GRID_W)), min(WIDTH, HEIGHT) / (16*game.GRID_W))

    pygame.display.update()


def user_turn():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = game.GRID_W * mouse_x // WIDTH
    mouse_y = game.GRID_W * mouse_y // HEIGHT
    game.full_turn(mouse_x, mouse_y)


def random_turn():
    move = minimax.random_move(game)[0]
    game.full_turn(move[0], move[1])


def minimax_turn():
    move = minimax.best_move(game)[0]
    game.full_turn(move[0], move[1])


init_game()
