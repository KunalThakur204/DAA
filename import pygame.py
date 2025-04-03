import pygame
import random
import tkinter as tk
from tkinter import messagebox

# Constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 20
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0)

def create_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = [(1, 1)]
    maze[1][1] = 0
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

    while stack:
        r, c = stack[-1]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 < nr < rows - 1 and 0 < nc < cols - 1 and maze[nr][nc] == 1:
                maze[r + dr // 2][c + dc // 2] = 0
                maze[nr][nc] = 0
                stack.append((nr, nc))
                break
        else:
            stack.pop()
    return maze

def find_nearest_open_cell(maze, start_row, start_col):
    for r in range(start_row, 0, -1):
        for c in range(start_col, 0, -1):
            if maze[r][c] == 0:
                return (r, c)
    return (1, 1)

def draw_maze(win, maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            color = BLACK if maze[r][c] == 1 else WHITE
            pygame.draw.rect(win, color, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def confirm_quit():
    return messagebox.askyesno("Quit", "Are you sure you want to quit?")

def game_loop():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    
    quit_button = pygame.Rect(WIDTH - 100, 10, 80, 30)
    
    while True:
        maze = create_maze(ROWS, COLS)
        player_pos = [1, 1]
        target_pos = find_nearest_open_cell(maze, ROWS - 2, COLS - 2)
        running = True
        
        while running:
            win.fill(WHITE)
            draw_maze(win, maze)
            
            pygame.draw.rect(win, GREEN, (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(win, RED, (target_pos[1] * TILE_SIZE, target_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
            pygame.draw.rect(win, BLACK, quit_button)
            font = pygame.font.Font(None, 24)
            text = font.render("Quit", True, WHITE)
            win.blit(text, (WIDTH - 80, 15))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if confirm_quit():
                        pygame.quit()
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(event.pos):
                        if confirm_quit():
                            pygame.quit()
                            return
            
            keys = pygame.key.get_pressed()
            new_pos = list(player_pos)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                new_pos[0] -= 1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                new_pos[0] += 1
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                new_pos[1] -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                new_pos[1] += 1
            
            if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS and maze[new_pos[0]][new_pos[1]] == 0:
                player_pos = new_pos
            
            if player_pos == list(target_pos):
                messagebox.showinfo("Maze Game", "Congratulations! You reached the goal!")
                running = False
                
            pygame.display.update()
            clock.tick(30)
    
def start_game():
    root.destroy()
    game_loop()

def exit_game():
    if confirm_quit():
        root.destroy()

def show_instructions():
    messagebox.showinfo("Instructions", "Use arrow keys or WASD to move. Reach the red square to win!")

def show_about():
    messagebox.showinfo("About", "Maze Game v1.0\nDeveloped using Python, Tkinter, and Pygame.")

def main_menu():
    global root
    root = tk.Tk()
    root.title("Maze Game")
    root.geometry("500x400")
    
    label = tk.Label(root, text="Welcome to the Maze Game!", font=("Arial", 16))
    label.pack(pady=20)
    
    yes_button = tk.Button(root, text="Start Game", command=start_game, width=20, height=2)
    yes_button.pack(pady=10)
    
    instructions_button = tk.Button(root, text="Instructions", command=show_instructions, width=20, height=2)
    instructions_button.pack(pady=10)
    
    about_button = tk.Button(root, text="About", command=show_about, width=20, height=2)
    about_button.pack(pady=10)
    
    no_button = tk.Button(root, text="Exit", command=exit_game, width=20, height=2)
    no_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main_menu()