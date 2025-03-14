import pygame
import sys

pygame.init()

# Screen dimensions and coulors
WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (0, 200, 0)
HOVER_COLOR = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Multiplayer")
font = pygame.font.SysFont(None, 50)

 # Sound effects
pygame.mixer.init()
food_sound = pygame.mixer.Sound('eat.ogg')
catch_sound = pygame.mixer.Sound('Death.ogg')
win_sound = pygame.mixer.Sound('start.ogg')

# Mazes
mazes = [
    [
        "####################",
        "#........#.........#",
        "#.####.#.####.#.####",
        "#.#....#.#....#.#..#",
        "#.#.####.#.####.#.##",
        "#.................##",
        "#####.#####.#####..#",
        "#..................#",
        "#.#####.#######.####",
        "#........#.........#",
        "####################"
    ],
    [
        "####################",
        "#...#.......#......#",
        "#.#.#.#####.#.####.#",
        "#.#........#.#..#..#",
        "#.#.####.#.#.##.#.##",
        "#..#.....#.........#",
        "#####.#######.#.##.#",
        "#..................#",
        "####################"
    ]
]

TILE_SIZE = 40
player1_start = (1, 1)
player2_start = (18, 1)

# Button 
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)

def start_screen():
    """Displays the start screen with instructions and a start button."""
    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        button_color = HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_rect)
        text = font.render("Start Game", True, BLACK)
        screen.blit(text, (button_rect.x + 7, button_rect.y + 15))

        # Instructions
        instructions = [
            "Instructions:",
            "Player 1 (Pac-Man): Arrow Keys",
            "Player 2 (Ghost): WASD Keys",
            "Goal:",
            "Player 1 - Pac-Man eats all food.",
            "Player 2 - Ghost catches Pac-Man."
        ]
        for idx, line in enumerate(instructions):
            instruction_text = font.render(line, True, WHITE)
            screen.blit(instruction_text, (50, 100 + idx * 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(mouse_pos):
                return

        pygame.display.flip()

def choose_map():
    """Display map options and let the player choose."""
    while True:
        screen.fill(BLACK)
        title_text = font.render("Choose Your Map", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        for idx, maze in enumerate(mazes):
            map_button = pygame.Rect(WIDTH // 2 - 100, 200 + idx * 100, 200, 60)
            pygame.draw.rect(screen, BUTTON_COLOR, map_button)
            button_text = font.render(f"Map {idx + 1}", True, BLACK)
            screen.blit(button_text, (map_button.x + 50, map_button.y + 10))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # This is to quit the game properly
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
                mouse_pos = pygame.mouse.get_pos()
                for idx, maze in enumerate(mazes):
                    map_button = pygame.Rect(WIDTH // 2 - 100, 200 + idx * 100, 200, 60)
                    if map_button.collidepoint(mouse_pos):
                        return idx
        
        pygame.display.flip()

start_screen()
selected_map = choose_map()
maze = mazes[selected_map]

def draw_maze(maze, food):
    """Draws the maze with walls and food."""
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            x, y = col_idx * TILE_SIZE, row_idx * TILE_SIZE
            if cell == "#":
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
            elif food[row_idx][col_idx]:
                pygame.draw.circle(screen, WHITE, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 5)

def check_wall_collision(pos, direction, maze):
    """Checks if moving in a direction would hit a wall."""
    x, y = pos
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if maze[new_y][new_x] == "#":
        return True
    return False

def end_screen(winner):
    """Displays the end screen with the winner and options to restart or quit."""
    screen.fill(BLACK)
    if winner == "Player 1 (Pac-Man)":
        text = font.render("Player 1 (Pac-Man) Wins!", True, YELLOW)
    elif winner == "Player 2 (Ghost)":
        text = font.render("Player 2 (Ghost) Wins!", True, RED)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 60)

    pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button)

    restart_text = font.render("Restart", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(restart_text, (restart_button.x + 50, restart_button.y + 10))
    screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

    pygame.display.flip()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(mouse_pos):
                    main()  # Restarts the game
                    return
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def main():

    # Positions and directions
    player1_pos = list(player1_start)
    player2_pos = list(player2_start)
    player1_dir = (0, 0)
    player2_dir = (0, 0)

    # Food grid
    food = [[cell == "." for cell in row] for row in maze]

    food_sound.play(-1)

    clock = pygame.time.Clock()
    while True:
        screen.fill(BLACK)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player 1 (Pac-Man) controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player1_dir = (0, -1)
        elif keys[pygame.K_DOWN]:
            player1_dir = (0, 1)
        elif keys[pygame.K_LEFT]:
            player1_dir = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            player1_dir = (1, 0)

        # Player 2 (Ghost) controls
        if keys[pygame.K_w]:
            player2_dir = (0, -1)
        elif keys[pygame.K_s]:
            player2_dir = (0, 1)
        elif keys[pygame.K_a]:
            player2_dir = (-1, 0)
        elif keys[pygame.K_d]:
            player2_dir = (1, 0)

        # Move Pac-Man
        if not check_wall_collision(player1_pos, player1_dir, maze):
            player1_pos[0] += player1_dir[0]
            player1_pos[1] += player1_dir[1]

        # Move Ghost
        if not check_wall_collision(player2_pos, player2_dir, maze):
            player2_pos[0] += player2_dir[0]
            player2_pos[1] += player2_dir[1]

        # Eating food
        if food[player1_pos[1]][player1_pos[0]]:
            food[player1_pos[1]][player1_pos[0]] = False

        # Winning conditions
        if all(not any(row) for row in food):
            win_sound.play(0)
            food_sound.stop()
            end_screen("Player 1 (Pac-Man)")
            break
        if player1_pos == player2_pos:
            catch_sound.play(0)
            food_sound.stop()
            end_screen("Player 2 (Ghost)")
            break

        # Draw maze, players, and food
        draw_maze(maze, food)
        pygame.draw.circle(screen, YELLOW, (player1_pos[0] * TILE_SIZE + TILE_SIZE // 2,
                                            player1_pos[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)
        pygame.draw.circle(screen, RED, (player2_pos[0] * TILE_SIZE + TILE_SIZE // 2,
                                         player2_pos[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()